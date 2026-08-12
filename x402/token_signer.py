"""JWT Token Signer for fiat x402 payment authorization proofs."""
import os
import time
import uuid
from typing import Optional, Dict, Any
import jwt


class FiatPaymentSigner:
    """Signs and verifies JWT payment authorization tokens for fiat x402 transactions."""

    DEFAULT_SECRET = "procurex-dev-secret-do-not-use-in-prod"

    def __init__(self, secret: Optional[str] = None):
        self.secret = secret or os.environ.get("X402_SIGNING_SECRET", self.DEFAULT_SECRET)

    def sign_payment(
        self,
        amount_usd: float,
        currency: str,
        service_type: str,
        supplier_id: str,
        exp_seconds: int = 60,
    ) -> str:
        """Sign a payment proof token with configurable expiration (default 60s)."""
        now = int(time.time())
        payload = {
            "amount": amount_usd,
            "currency": currency,
            "service": service_type if isinstance(service_type, str) else str(service_type),
            "supplier_id": supplier_id,
            "iat": now,
            "exp": now + exp_seconds,
            "nonce": str(uuid.uuid4()),
        }
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a payment token. Returns payload dict or None if invalid or expired."""
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception):
            return None
