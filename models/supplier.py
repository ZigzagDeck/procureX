from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional, Generic, TypeVar, Any
from datetime import datetime
from uuid import uuid4
from .evidence import EvidenceGraph, EvidenceStatus

T = TypeVar('T')

class SupplierType(str, Enum):
    """Type of the supplier."""
    MANUFACTURER = "manufacturer"
    DISTRIBUTOR = "distributor"
    WHOLESALER = "wholesaler"
    TRADER = "trader"
    UNKNOWN = "unknown"

class EvidencedField(BaseModel, Generic[T]):
    """A field value with attached provenance."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    value: T
    source: str = ""
    url: str = ""
    retrieved_at: Optional[datetime] = None
    confidence: float = 0.0
    evidence_status: EvidenceStatus = EvidenceStatus.UNKNOWN

class PriceBasis(str, Enum):
    """Basis for pricing."""
    PER_PIECE = "per_piece"
    PER_PAIR = "per_pair"
    PER_BOX = "per_box"
    PER_CARTON = "per_carton"
    TOTAL = "total"
    UNKNOWN = "unknown"

class TaxStatus(str, Enum):
    """Tax inclusion status for pricing."""
    GST_INCLUSIVE = "gst_inclusive"
    GST_EXCLUSIVE = "gst_exclusive"
    UNKNOWN = "unknown"

class Product(BaseModel):
    """A product offered by a supplier."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    product_name: str = ""
    material: str = ""
    application: str = ""
    size: str = ""
    price_value: Optional[float] = None
    price_basis: PriceBasis = PriceBasis.UNKNOWN
    tax_status: TaxStatus = TaxStatus.UNKNOWN
    currency: str = "INR"
    normalized_unit_price: Optional[float] = None  # INR per piece, GST-exclusive
    price_confidence: Optional[float] = None
    price_correction_note: str = ""
    moq: Optional[int] = None
    packaging: str = ""
    specifications: dict[str, str] = Field(default_factory=dict)
    source_url: str = ""
    retrieved_at: Optional[datetime] = None

class Supplier(BaseModel):
    """A supplier entity."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    supplier_type: SupplierType = SupplierType.UNKNOWN
    supplier_type_evidence: EvidenceStatus = EvidenceStatus.UNKNOWN
    address: str = ""
    city: str = ""
    state: str = ""
    pincode: str = ""
    phone: str = ""
    email: str = ""
    website: str = ""
    gstin: str = ""
    udyam_number: str = ""
    certifications: list[str] = Field(default_factory=list)
    claims: list[str] = Field(default_factory=list)  # Self-reported claims
    products: list[Product] = Field(default_factory=list)
    source_urls: list[str] = Field(default_factory=list)
    discovered_at: Optional[datetime] = None
    evidence: Optional[EvidenceGraph] = None  # forward ref resolved
    is_duplicate_of: Optional[str] = None  # ID of canonical supplier if merged
