import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from processing.entity_resolver import EntityResolver
from models.supplier import Supplier

r = EntityResolver()

def test_same_gstin():
    s1 = Supplier(name='ABC Industries Pvt Ltd', gstin='09AAACR5678K1ZH')
    s2 = Supplier(name='ABC Industries', gstin='09AAACR5678K1ZH')
    assert len(r.find_duplicates([s1, s2])) == 1
def test_similar_names():
    s1 = Supplier(name='Gupta Safety Products Pvt Ltd')
    s2 = Supplier(name='Gupta Safety Products Private Limited')
    assert len(r.find_duplicates([s1, s2])) == 1
def test_same_name_diff_city():
    s1 = Supplier(name='Safety First Industries', city='Delhi')
    s2 = Supplier(name='Safety First Industries', city='Chennai')
    assert len(r.find_duplicates([s1, s2])) == 0
def test_same_phone():
    s1 = Supplier(name='Company A', phone='+91-9876543210')
    s2 = Supplier(name='Company B', phone='09876543210')
    assert len(r.find_duplicates([s1, s2])) == 1
def test_different_suppliers():
    s1 = Supplier(name='Alpha Safety Pvt Ltd', city='Mumbai')
    s2 = Supplier(name='Beta Industrial Corp', city='Delhi')
    assert len(r.find_duplicates([s1, s2])) == 0
