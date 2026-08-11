"""
Research audit trace functionality.
"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Dict

class AuditTraceEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action: str
    actor: str = "system"
    details: Dict[str, Any] = Field(default_factory=dict)

class AuditTrace(BaseModel):
    session_id: str
    entries: list[AuditTraceEntry] = Field(default_factory=list)

    def log_action(self, action: str, details: Dict[str, Any] = None, actor: str = "system"):
        if details is None:
            details = {}
        self.entries.append(
            AuditTraceEntry(action=action, actor=actor, details=details)
        )
