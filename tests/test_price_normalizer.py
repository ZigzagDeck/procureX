import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from processing.price_normalizer import PriceNormalizer, estimate_price_confidence
from models.supplier import PriceBasis, TaxStatus

n = PriceNormalizer()

def test_per_piece(): assert n.normalize_unit_price(75.0, PriceBasis.PER_PIECE, TaxStatus.GST_EXCLUSIVE) == 75.0
def test_per_pair(): assert n.normalize_unit_price(150.0, PriceBasis.PER_PAIR, TaxStatus.GST_EXCLUSIVE) == 75.0
def test_per_box(): assert n.normalize_unit_price(7500.0, PriceBasis.PER_BOX, TaxStatus.GST_EXCLUSIVE, quantity_in_pack=100) == 75.0
def test_gst_inclusive(): assert n.normalize_unit_price(88.50, PriceBasis.PER_PIECE, TaxStatus.GST_INCLUSIVE) == 75.0
def test_total(): assert n.normalize_unit_price(375000.0, PriceBasis.TOTAL, TaxStatus.GST_EXCLUSIVE, total_quantity=5000) == 75.0
def test_zero(): assert n.normalize_unit_price(0.0, PriceBasis.PER_PIECE, TaxStatus.GST_EXCLUSIVE) == 0.0
def test_budget(): assert n.is_within_budget(75.0, 80.0) == True; assert n.is_within_budget(85.0, 80.0) == False
def test_box_and_total_prices_are_low_confidence():
    assert estimate_price_confidence(PriceBasis.PER_BOX) == 0.25
    assert estimate_price_confidence(PriceBasis.TOTAL) == 0.25
    assert estimate_price_confidence(PriceBasis.PER_PIECE) == 0.9
