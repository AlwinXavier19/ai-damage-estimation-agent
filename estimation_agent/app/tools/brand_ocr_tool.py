"""
Brand OCR Tool

Extracts structured information from brand documents (images/PDFs) 
using Azure OpenAI GPT-4o or GPT-4o Vision.
"""

import os
import re
import time
from typing import Optional
from pypdf import PdfReader

from estimation_agent.app.services.azure_openai import AzureOpenAIService
from estimation_agent.app.models.prediction import BrandEstimationPrediction, BrandSpareItem


class BrandOCRTool:
    """
    Tool responsible for parsing brand documents (invoices, receipts, estimate PDFs/images)
    and outputting structured BrandEstimationPrediction JSON data.
    """

    def __init__(self):
        self.openai_service = AzureOpenAIService()

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Reads and extracts plain text from all pages of a digital PDF.
        """
        try:
            reader = PdfReader(pdf_path)
            full_text = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    full_text.append(text)
            return "\n--- PAGE BREAK ---\n".join(full_text)
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def run(
        self,
        document_path: str,
        brand_hint: Optional[str] = None,
        doc_type_hint: Optional[str] = None,
    ) -> BrandEstimationPrediction:
        """
        Runs document parsing by routing to PDF textual extraction or vision-based GPT-4o.
        """
        start_time = time.time()
        
        is_pdf = document_path.lower().endswith(".pdf")
        extracted_text = ""
        
        if is_pdf:
            extracted_text = self.extract_text_from_pdf(document_path)
            
        system_prompt = self._build_extraction_prompt(brand_hint, doc_type_hint)

        if is_pdf and extracted_text.strip():
            # Textual Extraction via standard Azure OpenAI Chat completions
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Here is the text extracted from the PDF document. "
                        f"Please extract all details and return the JSON:\n\n{extracted_text}"
                    )
                }
            ]
        else:
            # Vision Extraction: If it's a PDF without selectable text or a standard image
            # Note: For PDF vision fallback, we can use the Azure Blob URL or if it's an image path,
            # we send its Azure Blob Storage URL to Azure OpenAI.
            # In Django, we will upload the image/PDF file to Azure Blob first, then pass the public URL.
            document_url = document_path
            
            content = [
                {
                    "type": "text",
                    "text": "Extract all fields from this brand document image and return as structured JSON."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": document_url
                    }
                }
            ]
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ]

        response = self.openai_service.chat_completion(messages)
        prediction_dict = self.openai_service.extract_json(response)
        
        # Calculate duration
        extraction_time = time.time() - start_time
        prediction_dict["extraction_time"] = round(extraction_time, 2)
        prediction_dict["ai_model"] = "Azure GPT-4o"
        
        # Override hints if missing
        if not prediction_dict.get("brand") and brand_hint:
            prediction_dict["brand"] = brand_hint
        if not prediction_dict.get("document_type") and doc_type_hint:
            prediction_dict["document_type"] = doc_type_hint

        # Format and validate the spares price/totals
        spares_formatted = []
        for spare in prediction_dict.get("spares", []):
            # Strip currency symbols and parse floats
            unit_price = self._clean_price(spare.get("unit_price") or spare.get("price") or 0.0)
            qty = int(spare.get("qty") or spare.get("quantity") or 1)
            total = self._clean_price(spare.get("total") or (unit_price * qty))
            
            spares_formatted.append(
                BrandSpareItem(
                    name=spare.get("name") or spare.get("sparepart") or "Unknown Part",
                    part_code=spare.get("part_code") or spare.get("code"),
                    qty=qty,
                    unit_price=unit_price,
                    total=total
                )
            )
            
        prediction_dict["spares"] = spares_formatted
        prediction_dict["labour"] = self._clean_price(prediction_dict.get("labour") or prediction_dict.get("labor") or 0.0)
        prediction_dict["discount"] = self._clean_price(prediction_dict.get("discount") or 0.0)
        prediction_dict["tax"] = self._clean_price(prediction_dict.get("tax") or prediction_dict.get("gst") or 0.0)
        prediction_dict["grand_total"] = self._clean_price(prediction_dict.get("grand_total") or prediction_dict.get("totalamount") or 0.0)

        return BrandEstimationPrediction(**prediction_dict)

    def _clean_price(self, price_val) -> float:
        """Helper to sanitize currency symbols and return clean floats."""
        if isinstance(price_val, (int, float)):
            return float(price_val)
        if not price_val:
            return 0.0
        try:
            cleaned = re.sub(r"[^\d\.]", "", str(price_val))
            return float(cleaned) if cleaned else 0.0
        except ValueError:
            return 0.0

    def _build_extraction_prompt(self, brand_hint: Optional[str], doc_type_hint: Optional[str]) -> str:
        """
        Builds the detailed system prompt with extraction rules and JSON structure.
        """
        brand_info = f"Hint: The brand is likely {brand_hint}." if brand_hint else ""
        doc_type_info = f"Hint: The document type is likely {doc_type_hint}." if doc_type_hint else ""
        
        return f"""You are a professional Enterprise OCR Document Extractor agent specializing in mobile/electronics repair estimation documents.
Your goal is to parse brand receipts, repair cost estimates, and invoice documents from multiple manufacturers (including Vivo, Oppo, Samsung, Xiaomi, Apple, etc.) into a single structured schema.

{brand_info}
{doc_type_info}

### Core Rules:
1. **Identify Brand**: Search the document for brand headers or logos (e.g. Vivo, Oppo, Samsung). If identified, populate the "brand" field exactly (e.g., "Vivo", "Oppo").
2. **Data Normalization**: Clean and normalize text:
   - Strip all currency symbols (e.g., ₹, INR, Rs., $) and commas from prices/totals, converting them to clean numeric decimal floats.
3. **Itemization**: Ensure every spare part item in any table is captured:
   - "name": The descriptive name of the part (e.g., "Display Assembly V60 Blue", "Battery Cover").
   - "part_code": The part/material code if visible (e.g., "5437870", "PD2503EF/GF").
   - "qty": Quantity (default to 1 if not specified).
   - "unit_price": Unit price before tax.
   - "total": The product of unit_price * qty.
4. **Charges**:
   - Extract "labour" charges or labor costs.
5. **Return Structured JSON Only**: Your output MUST match the schema below. Do not wrap in markdown other than json code block, and do not add any extra text or conversational filler.

### Output JSON Schema:
{{
  "brand": "Vivo or Oppo or Samsung or OnePlus etc.",
  "customer_complaint": "Customer description of issue or fault phenomenon/appearance/engineer findings",
  "remarks": "Any internal comments, insurer details, or additional notes from engineer",
  "spares": [
    {{
      "name": "Display Assembly",
      "part_code": "5437870",
      "qty": 1,
      "unit_price": 9000.0,
      "total": 9000.0
    }}
  ],
  "labour": 250.0,
  "confidence_score": 0.98,
  "document_type": "Estimate Receipt"
}}
"""
