"""
Pydantic models used by the AI Estimation Agent.

These models define the contract between:
    Azure OpenAI GPT-4o
            ↓
      Vision Tool
            ↓
      Workflow
            ↓
       Django Application
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class SparePrediction(BaseModel):
    """
    AI suggested spare part.
    """

    name: str = Field(
        ...,
        description="Existing spare part name from the database"
    )

    qty: int = Field(
        default=1,
        ge=1,
        description="Suggested quantity"
    )

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Confidence score"
    )


class DamagePrediction(BaseModel):
    """
    Individual visible damage detected by GPT-4o Vision.
    """

    damage: str

    location: Optional[str] = None

    confidence: Optional[float] = None


class EstimationPrediction(BaseModel):
    """
    Final AI prediction returned to Django.
    """

    engineer_observation: str

    repair_summary: str

    cause_of_damage: str

    damages: List[DamagePrediction] = Field(default_factory=list)

    spares: List[SparePrediction] = Field(default_factory=list)

    overall_confidence: Optional[float] = None


class BrandSpareItem(BaseModel):
    """
    Spare part item extracted from brand estimation documents.
    """
    name: str = Field(..., description="Spare part name or description")
    part_code: Optional[str] = Field(default=None, description="Part / Material Code")
    qty: int = Field(default=1, ge=1, description="Quantity")
    unit_price: float = Field(default=0.0, ge=0.0, description="Price per unit without GST")
    total: float = Field(default=0.0, ge=0.0, description="Total amount for this spare part")


class BrandEstimationPrediction(BaseModel):
    """
    Detailed structured extraction from brand documents.
    """
    brand: str = Field(..., description="OEM Brand name (e.g. Vivo, Oppo, etc.)")
    customer_complaint: Optional[str] = Field(default=None, description="Fault description / complaint as described by user")
    remarks: Optional[str] = Field(default=None, description="Internal remarks/comments")
    spares: List[BrandSpareItem] = Field(default_factory=list, description="Extracted spare parts table rows")
    labour: float = Field(default=0.0, ge=0.0, description="Labour costs/fees")
    confidence_score: float = Field(default=0.95, ge=0.0, le=1.0, description="Confidence score")
    document_type: Optional[str] = Field(default="Estimate Receipt", description="Type of document analyzed")
    extraction_time: Optional[float] = Field(default=0.0, description="Extraction duration in seconds")
    ai_model: Optional[str] = Field(default="GPT-4o", description="AI model used")
    status: Optional[str] = Field(default="success", description="Status code of extraction")
