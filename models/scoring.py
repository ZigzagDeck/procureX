from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from .requirement import ProcurementMode

class ScoreDimension(BaseModel):
    """A single scoring dimension."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    name: str
    weight: int  # out of 100
    raw_score: float = 0.0  # 0.0 to 1.0
    weighted_score: float = 0.0  # raw_score * weight
    explanation: str = ""

class SupplierScore(BaseModel):
    """Overall score for a supplier."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    supplier_id: str
    total_score: float = 0.0  # out of 100
    dimensions: list[ScoreDimension] = Field(default_factory=list)
    confidence: float = 0.0  # 0.0 to 1.0, separate from score
    confidence_explanation: str = ""
    procurement_mode: ProcurementMode = ProcurementMode.BALANCED
    scored_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ScoringWeights(BaseModel):
    """Weights for the different scoring dimensions."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    product_fit: int = 25
    price_competitiveness: int = 20
    business_verification: int = 20
    delivery_feasibility: int = 15
    moq_compatibility: int = 10
    evidence_quality: int = 10
    
    @classmethod
    def for_mode(cls, mode: ProcurementMode) -> "ScoringWeights":
        if mode == ProcurementMode.COST_OPTIMIZED:
            return cls(product_fit=20, price_competitiveness=30, business_verification=15, delivery_feasibility=15, moq_compatibility=10, evidence_quality=10)
        elif mode == ProcurementMode.RELIABILITY_FIRST:
            return cls(product_fit=20, price_competitiveness=15, business_verification=30, delivery_feasibility=15, moq_compatibility=10, evidence_quality=10)
        return cls()  # BALANCED defaults
