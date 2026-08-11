"""Orchestrates evidence gathering for suppliers."""
from models.evidence import EvidenceGraph, EvidenceStatus
from verification.evidence_graph import EvidenceGraphManager
from verification.gst_verifier import GSTVerifier
from verification.udyam_verifier import UdyamVerifier
from extraction.provenance import create_evidence_record

class EvidenceCollector:
    def __init__(self):
        self.gst_verifier = GSTVerifier(mode='mock')
        self.udyam_verifier = UdyamVerifier(mode='mock')
        self.graph_manager = EvidenceGraphManager()
    async def collect_evidence(self, supplier):
        graph = supplier.evidence or EvidenceGraph(supplier_id=supplier.id)
        if supplier.gstin:
            result = await self.gst_verifier.verify(supplier.gstin)
            if result.get('status') == 'ACTIVE':
                self.graph_manager.add_evidence(graph, 'gstin', create_evidence_record('gstin', supplier.gstin, 'gst_portal', confidence=0.9, status=EvidenceStatus.DOCUMENTED))
                if result.get('legal_name'):
                    self.graph_manager.add_evidence(graph, 'name', create_evidence_record('name', result['legal_name'], 'gst_portal', confidence=0.9, status=EvidenceStatus.DOCUMENTED))
                if result.get('state'):
                    self.graph_manager.add_evidence(graph, 'address', create_evidence_record('address', result['state'], 'gst_portal', confidence=0.8, status=EvidenceStatus.DOCUMENTED))
        if supplier.udyam_number:
            result = await self.udyam_verifier.verify(supplier.udyam_number)
            if result.get('category'):
                self.graph_manager.add_evidence(graph, 'supplier_type', create_evidence_record('supplier_type', result['category'], 'udyam_portal', confidence=0.8, status=EvidenceStatus.DOCUMENTED))
        return graph
