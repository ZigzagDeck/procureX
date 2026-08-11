import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from processing.scoring import ScoringEngine
from models.supplier import Supplier, Product, PriceBasis, TaxStatus
from models.requirement import ProcurementRequirement, ProcurementMode
from models.evidence import EvidenceGraph

engine = ScoringEngine()

def test_score_with_matching_supplier():
    req = ProcurementRequirement(product_category='safety_gloves', material='nitrile', application='industrial_safety', quantity=5000, destination='Ghaziabad', maximum_unit_price=80.0)
    supplier = Supplier(name='Test Corp', gstin='09AAACR5678K1ZH', phone='9876543210', email='test@test.com',
        products=[Product(product_name='Nitrile Gloves', material='nitrile', application='industrial', size='M', price_value=65.0, price_basis=PriceBasis.PER_PIECE, tax_status=TaxStatus.GST_EXCLUSIVE, moq=1000)])
    score = engine.score_supplier(supplier, req)
    assert score.total_score > 0
    assert len(score.dimensions) == 6
    assert score.supplier_id == supplier.id

def test_score_with_no_products():
    req = ProcurementRequirement(product_category='safety_gloves', material='nitrile', application='industrial_safety', quantity=5000, destination='Ghaziabad')
    supplier = Supplier(name='Empty Corp')
    score = engine.score_supplier(supplier, req)
    assert score.total_score > 0
    assert score.total_score < 50

def test_cost_optimized_weights():
    req = ProcurementRequirement(product_category='safety_gloves', material='nitrile', application='industrial_safety', quantity=5000, destination='Mumbai', procurement_mode=ProcurementMode.COST_OPTIMIZED, maximum_unit_price=80.0)
    supplier = Supplier(name='Cheap Corp', products=[Product(price_value=40.0, price_basis=PriceBasis.PER_PIECE, tax_status=TaxStatus.GST_EXCLUSIVE, material='nitrile', application='industrial')])
    score = engine.score_supplier(supplier, req)
    price_dim = next(d for d in score.dimensions if d.name == 'Price Competitiveness')
    assert price_dim.weight == 30
