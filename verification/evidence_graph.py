"""Evidence graph management."""
from models.evidence import EvidenceRecord, EvidenceStatus, EvidenceGraph, Contradiction

STATUS_RANK = {EvidenceStatus.UNKNOWN:0, EvidenceStatus.CLAIMED:1, EvidenceStatus.DOCUMENTED:2, EvidenceStatus.CORROBORATED:3, EvidenceStatus.VERIFIED:4, EvidenceStatus.CONFLICTING:-1}

class EvidenceGraphManager:
    def add_evidence(self, graph, field, record):
        if field not in graph.claims: graph.claims[field] = []
        graph.claims[field].append(record)
        self._check_contradictions(graph, field)
    def _check_contradictions(self, graph, field):
        records = graph.claims.get(field, [])
        if len(records) < 2: return
        values = [r.value for r in records]
        sources = [r.source for r in records]
        if field == 'price':
            nums = [float(v) for v in values if v is not None]
            if len(nums) >= 2 and max(nums) > 0:
                if (max(nums) - min(nums)) / max(nums) > 0.10:
                    c = Contradiction(field_name=field, values=list(set(str(n) for n in nums)), sources=list(set(sources)), description=f'Price discrepancy >10%: {min(nums)} vs {max(nums)}')
                    if not any(x.field_name == field for x in graph.contradictions): graph.contradictions.append(c)
        else:
            unique = set(str(v).lower().strip() for v in values)
            if len(unique) > 1:
                c = Contradiction(field_name=field, values=list(unique), sources=list(set(sources)), description=f'Conflicting values for {field}')
                if not any(x.field_name == field for x in graph.contradictions): graph.contradictions.append(c)
    def get_overall_status(self, graph):
        if graph.contradictions: return EvidenceStatus.CONFLICTING
        all_statuses = [r.evidence_status for rs in graph.claims.values() for r in rs]
        if not all_statuses: return EvidenceStatus.UNKNOWN
        return max(all_statuses, key=lambda s: STATUS_RANK.get(s, 0))
    def calculate_confidence(self, graph):
        key_fields = ['name','gstin','supplier_type','price','address','phone']
        covered = sum(1 for f in key_fields if f in graph.claims and graph.claims[f])
        completeness = covered / len(key_fields)
        consistency = 0.7 if graph.contradictions else 1.0
        return round(completeness * consistency, 2)
