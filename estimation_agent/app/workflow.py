"""
Estimation Workflows

Defines and coordinates workflows for repair estimation.
"""

from typing import Optional
from estimation_agent.app.models.prediction import (
    EstimationPrediction,
    BrandEstimationPrediction
)

from estimation_agent.app.tools.vision_tool import VisionTool
from estimation_agent.app.tools.spare_mapper import SpareMapper
from estimation_agent.app.tools.validation_tool import ValidationTool
from estimation_agent.app.tools.summary_tool import SummaryTool
from estimation_agent.app.tools.confidence_tool import ConfidenceTool
from estimation_agent.app.tools.brand_ocr_tool import BrandOCRTool


class ManualWorkflow:
    """
    Coordinates direct manual entry by a technician.
    Simply passes back a blank structure or accepts direct inputs with No AI.
    """
    def run(self) -> dict:
        return {
            "engineer_observation": "",
            "repair_summary": "",
            "cause_of_damage": "",
            "spares": []
        }


class EstimationWorkflow:
    """
    Coordinates the AI Image Estimation pipeline (6 pre-repair images).
    """

    def __init__(self):
        self.vision_tool = VisionTool()
        self.summary_tool = SummaryTool()
        self.confidence_tool = ConfidenceTool()

    def run(
        self,
        image_urls: list[str],
        available_spares: list[str],
    ) -> EstimationPrediction:
        """
        Complete image-based estimation workflow.
        """
        # Step 1 - Vision Analysis
        prediction = self.vision_tool.analyze(
            image_urls=image_urls,
            available_spares=available_spares,
        )

        # Step 2 - Map Spare Names
        mapper = SpareMapper(
            available_spares=available_spares
        )
        prediction = mapper.map_prediction(prediction)

        # Step 3 - Validate Spare Parts
        validator = ValidationTool(
            available_spares=available_spares
        )
        prediction = validator.process(prediction)

        # Step 4 - Clean Summary
        prediction = self.summary_tool.process(prediction)

        # Step 5 - Confidence Filtering
        prediction = self.confidence_tool.process(prediction)

        return prediction


class BrandEstimationWorkflow:
    """
    Coordinates Brand Document Estimation Extraction (Receipts, PDF estimates, Invoices).
    """

    def __init__(self):
        self.ocr_tool = BrandOCRTool()

    def run(
        self,
        document_path: str,
        brand_hint: Optional[str] = None,
        doc_type_hint: Optional[str] = None,
    ) -> BrandEstimationPrediction:
        """
        Runs full OCR document parser, extracts structured OEM info, 
        and normalizes prices and tables.
        """
        prediction = self.ocr_tool.run(
            document_path=document_path,
            brand_hint=brand_hint,
            doc_type_hint=doc_type_hint,
        )
        return prediction
