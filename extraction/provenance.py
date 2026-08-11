"""Provenance tracking for extracted fields."""
from datetime import datetime
from models.evidence import EvidenceRecord, EvidenceStatus

def create_evidence_record(field_name, value, source, url='', confidence=0.5, status=EvidenceStatus.CLAIMED, raw_snippet=''):
    return EvidenceRecord(field_name=field_name, value=value, source=source, url=url,
                          retrieved_at=datetime.utcnow(), confidence=confidence,
                          evidence_status=status, raw_snippet=raw_snippet)
