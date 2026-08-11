import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from x402.mock import MockPaymentProvider

def test_mock_payment_completes():
    provider = MockPaymentProvider()
    result = provider.simulate_402_flow(0.002, 'price_intelligence')
    assert result['status'] == 'completed'
    assert result['is_mock'] == True
    assert result['amount'] == 0.002

def test_mock_payment_different_amounts():
    provider = MockPaymentProvider()
    r1 = provider.simulate_402_flow(0.001, 'supplier_verification')
    r2 = provider.simulate_402_flow(0.002, 'price_intelligence')
    assert r1['amount'] == 0.001
    assert r2['amount'] == 0.002
