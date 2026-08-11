from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional, Any
from datetime import datetime

class EvidenceStatus(str, Enum):
    """Status of the evidence."""
    UNKNOWN = "unknown"
    CLAIMED = "claimed"
    DOCUMENTED = "documented"
    CORROBORATED = "corroborated"
    VERIFIED = "verified"
    CONFLICTING = "conflicting"

class EvidenceRecord(BaseModel):
    """A record of evidence for a specific field."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    field_name: str  # which field this evidence is about
    value: Any
    source: str  # source adapter name
    url: Optional[str] = None
    retrieved_at: Optional[datetime] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_status: EvidenceStatus = EvidenceStatus.UNKNOWN
    raw_snippet: Optional[str] = None  # relevant raw text

class Contradiction(BaseModel):
    """Represents a contradiction found in the evidence."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    field_name: str
    values: list[Any]  # conflicting values
    sources: list[str]  # which sources disagree
    description: str
    detected_at: datetime = Field(default_factory=datetime.utcnow)

class EvidenceGraph(BaseModel):
    """Collection of evidence for a supplier."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    supplier_id: str
    claims: dict[str, list[EvidenceRecord]] = Field(default_factory=dict)
    # key = field_name like 'gstin', 'supplier_type', 'price', 'certification'
    contradictions: list[Contradiction] = Field(default_factory=list)
