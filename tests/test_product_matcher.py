import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from processing.product_matcher import ProductMatcher

m = ProductMatcher()

def test_nitrile_matches_nitrile_rubber():
    match, _ = m.match_material('nitrile', 'Nitrile Rubber')
    assert match == True
def test_nitrile_not_latex():
    match, _ = m.match_material('nitrile', 'latex')
    assert match == False
def test_nbr_matches_nitrile():
    match, _ = m.match_material('nitrile', 'NBR')
    assert match == True
def test_size_m_matches_medium():
    match, _ = m.match_size('M', 'medium')
    assert match == True
def test_industrial_matches():
    match, _ = m.match_application('industrial_safety', 'industrial')
    assert match == True
def test_industrial_not_medical():
    match, _ = m.match_application('industrial_safety', 'medical examination')
    assert match == False
def test_no_size_req():
    match, _ = m.match_size(None, 'L')
    assert match == True
