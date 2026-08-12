import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from x402.token_signer import FiatPaymentSigner


def test_sign_and_verify():
    """Sign a payment proof token and verify it returns correct payload."""
    signer = FiatPaymentSigner(secret="test-secret-key")
    token = signer.sign_payment(
        amount_usd=0.002,
        currency="USD",
        service_type="price_intelligence",
        supplier_id="supp-123",
        exp_seconds=60,
    )
    assert token is not None
    payload = signer.verify_token(token)
    assert payload is not None
    assert payload["amount"] == 0.002
    assert payload["currency"] == "USD"
    assert payload["service"] == "price_intelligence"
    assert payload["supplier_id"] == "supp-123"
    assert "nonce" in payload


def test_expired_token():
    """Sign with exp=1s, sleep 2 seconds, verify returns None."""
    signer = FiatPaymentSigner(secret="test-secret-key")
    token = signer.sign_payment(
        amount_usd=0.002,
        currency="USD",
        service_type="price_intelligence",
        supplier_id="supp-123",
        exp_seconds=1,
    )
    time.sleep(2)
    payload = signer.verify_token(token)
    assert payload is None
