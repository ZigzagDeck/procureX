import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from extraction.requirement_parser import parse_requirement, _normalize_size

def test_canonical_query():
    r = parse_requirement("Find 5,000 medium-sized nitrile industrial safety gloves under \u20b980 per piece, preferably from manufacturers, deliverable to Ghaziabad within 10 days.")
    assert r.quantity == 5000
    assert r.material == 'nitrile'
    assert r.maximum_unit_price == 80.0
    assert r.destination == 'Ghaziabad'
    assert r.preferred_supplier_type == 'manufacturer'

def test_simple_query():
    r = parse_requirement("I need 1000 nitrile gloves for our Pune factory")
    assert r.quantity == 1000
    assert r.material == 'nitrile'
    assert r.destination == 'Pune'

def test_size_normalization():
    assert _normalize_size('medium') == 'M'
    assert _normalize_size('extra large') == 'XL'
    assert _normalize_size(None) is None

def test_cost_optimized_mode():
    r = parse_requirement("Find cheapest nitrile gloves, 10000 pieces, budget \u20b950/piece, Mumbai")
    assert r.quantity == 10000
    assert r.procurement_mode.value == 'cost_optimized'
    assert r.destination == 'Mumbai'

def test_empty_input():
    r = parse_requirement("")
    assert r.quantity == 0
