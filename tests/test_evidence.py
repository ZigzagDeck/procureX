import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from verification.evidence_graph import EvidenceGraphManager
from models.evidence import EvidenceStatus, EvidenceGraph
from extraction.provenance import create_evidence_record

mgr = EvidenceGraphManager()

def test_add_evidence():
    g = EvidenceGraph(supplier_id='test')
    rec = create_evidence_record('name', 'Test Corp', 'web', confidence=0.5)
    mgr.add_evidence(g, 'name', rec)
    assert 'name' in g.claims
    assert len(g.claims['name']) == 1

def test_no_contradiction_same_values():
    g = EvidenceGraph(supplier_id='test')
    mgr.add_evidence(g, 'name', create_evidence_record('name', 'Test Corp', 'source1'))
    mgr.add_evidence(g, 'name', create_evidence_record('name', 'Test Corp', 'source2'))
    assert len(g.contradictions) == 0

def test_contradiction_different_values():
    g = EvidenceGraph(supplier_id='test')
    mgr.add_evidence(g, 'supplier_type', create_evidence_record('supplier_type', 'manufacturer', 'source1'))
    mgr.add_evidence(g, 'supplier_type', create_evidence_record('supplier_type', 'trader', 'source2'))
    assert len(g.contradictions) == 1

def test_price_contradiction():
    g = EvidenceGraph(supplier_id='test')
    mgr.add_evidence(g, 'price', create_evidence_record('price', 50.0, 'source1'))
    mgr.add_evidence(g, 'price', create_evidence_record('price', 80.0, 'source2'))
    assert len(g.contradictions) == 1

def test_confidence_calculation():
    g = EvidenceGraph(supplier_id='test')
    mgr.add_evidence(g, 'name', create_evidence_record('name', 'Test', 'web'))
    mgr.add_evidence(g, 'price', create_evidence_record('price', 50, 'web'))
    mgr.add_evidence(g, 'phone', create_evidence_record('phone', '9876543210', 'web'))
    conf = mgr.calculate_confidence(g)
    assert conf == 0.5

def test_conflicting_overall_status():
    g = EvidenceGraph(supplier_id='test')
    mgr.add_evidence(g, 'price', create_evidence_record('price', 50, 'a'))
    mgr.add_evidence(g, 'price', create_evidence_record('price', 80, 'b'))
    assert mgr.get_overall_status(g) == EvidenceStatus.CONFLICTING
