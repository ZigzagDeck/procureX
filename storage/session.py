from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from uuid import uuid4

# Import models (assume these will be defined elsewhere)
from models.requirement import ProcurementRequirement
from models.supplier import Supplier
from models.scoring import SupplierScore
from models.budget import ResearchBudget
from models.evidence import EvidenceGraph
from models.geographic import DeliveryFeasibility

class ResearchPhase(str, Enum):
    NOT_STARTED = "not_started"
    PARSING = "parsing"
    PLANNING = "planning"
    SEARCHING = "searching"
    EXTRACTING = "extracting"
    NORMALIZING = "normalizing"
    DEDUPLICATING = "deduplicating"
    MATCHING = "matching"
    VERIFYING = "verifying"
    GEO_ANALYZING = "geo_analyzing"
    SCORING = "scoring"
    INTELLIGENCE = "intelligence"
    RE_RANKING = "re_ranking"
    REPORTING = "reporting"
    COMPLETED = "completed"
    FAILED = "failed"

class ResearchLogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    phase: ResearchPhase
    message: str
    details: dict = Field(default_factory=dict)

class ResearchSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    requirement: Optional[ProcurementRequirement] = None
    phase: ResearchPhase = ResearchPhase.NOT_STARTED
    suppliers: list[Supplier] = Field(default_factory=list)
    scores: list[SupplierScore] = Field(default_factory=list)
    budget: ResearchBudget = Field(default_factory=ResearchBudget)
    delivery_analyses: list[DeliveryFeasibility] = Field(default_factory=list)
    log: list[ResearchLogEntry] = Field(default_factory=list)
    sources_consulted: list[str] = Field(default_factory=list)
    error_message: str = ""
    
    def add_log(self, phase: ResearchPhase, message: str, **details):
        self.log.append(ResearchLogEntry(phase=phase, message=message, details=details))
    
    def get_ranked_suppliers(self) -> list[tuple[Supplier, SupplierScore]]:
        score_map = {s.supplier_id: s for s in self.scores}
        ranked = []
        for supplier in self.suppliers:
            if supplier.id in score_map and getattr(supplier, "is_duplicate_of", None) is None:
                ranked.append((supplier, score_map[supplier.id]))
        ranked.sort(key=lambda x: x[1].total_score, reverse=True)
        return ranked
