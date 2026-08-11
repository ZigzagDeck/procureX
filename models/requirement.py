from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime, date

class ProcurementMode(str, Enum):
    """Modes determining the scoring weights."""
    COST_OPTIMIZED = "cost_optimized"
    BALANCED = "balanced"
    RELIABILITY_FIRST = "reliability_first"

class ProcurementRequirement(BaseModel):
    """The normalized requirements for the procurement operation."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    product_category: str  # e.g., "safety_gloves"
    material: str  # e.g., "nitrile"
    application: str  # e.g., "industrial_safety"
    size: Optional[str] = None  # e.g., "M"
    quantity: int
    maximum_unit_price: Optional[float] = None  # INR per piece
    currency: str = "INR"
    destination: str  # e.g., "Ghaziabad"
    delivery_deadline: Optional[date] = None
    preferred_supplier_type: Optional[str] = None  # e.g., "manufacturer"
    certification_requirements: list[str] = Field(default_factory=list)
    procurement_mode: ProcurementMode = ProcurementMode.BALANCED
    raw_query: str = ""  # Original NL query
    parsed_at: Optional[datetime] = None
