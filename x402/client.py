import os
import httpx
from datetime import datetime
from models.budget import PaymentTransaction, PaymentStatus, ServiceType, PaymentDecision
from x402.fx_engine import FXEngine
from x402.token_signer import FiatPaymentSigner
from x402.account import PrepaidUSDAccount


class X402Client:
    """Client for x402 fiat USD micro-payment protocol."""

    def __init__(self):
        self.mode = os.environ.get('PROCUREX_X402_MODE', 'mock')
        self.base_url = os.environ.get('PROCUREX_INTEL_SERVICE_URL', 'http://localhost:8000')
        self.fx_engine = FXEngine()
        self.signer = FiatPaymentSigner()
        self.account = PrepaidUSDAccount()

    async def call_service(self, service_type: ServiceType, request_data: dict, decision: PaymentDecision) -> tuple[dict, PaymentTransaction]:
        """Call intelligence service, handling x402 fiat USD payment flow."""
        endpoint = '/v1/price-intelligence' if service_type == ServiceType.PRICE_INTELLIGENCE else '/v1/supplier-verification'
        
        tx = PaymentTransaction(
            service_type=service_type,
            supplier_id=decision.supplier_id,
            amount=decision.cost,
            currency="USD",
            decision=decision,
        )

        # Compute FX conversion rate and INR equivalent
        tx.fx_rate = self.fx_engine.get_rate()
        tx.amount_inr = self.fx_engine.usd_to_inr(tx.amount)

        if self.mode == 'mock':
            return await self._mock_call(endpoint, request_data, tx)
        else:
            return await self._live_call(endpoint, request_data, tx)

    async def _mock_call(self, endpoint, data, tx):
        """Simulate x402 fiat flow: 402 -> sign -> 200 without real deductions."""
        if not tx.decision.should_purchase:
            tx.status = PaymentStatus.SKIPPED
            return {}, tx

        # Sign mock token proof
        token = self.signer.sign_payment(
            amount_usd=tx.amount,
            currency=tx.currency,
            service_type=tx.service_type.value,
            supplier_id=tx.supplier_id,
        )

        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                headers = {"Authorization": f'x402-fiat token="{token}" amount="{tx.amount}" currency="{tx.currency}"'}
                resp = await client.post(endpoint, json=data, headers=headers, timeout=10)
                if resp.status_code == 200:
                    result = resp.json()
                    tx.status = PaymentStatus.COMPLETED
                    tx.completed_at = datetime.utcnow()
                    tx.response_summary = f"Received {len(result)} fields (Token verified)"
                    return result, tx
                else:
                    # Return mock synthetic intelligence payload if external server not running
                    result = self._get_synthetic_payload(tx.service_type)
                    tx.status = PaymentStatus.COMPLETED
                    tx.completed_at = datetime.utcnow()
                    tx.response_summary = f"Received {len(result)} fields (Mock response)"
                    return result, tx
            except Exception:
                result = self._get_synthetic_payload(tx.service_type)
                tx.status = PaymentStatus.COMPLETED
                tx.completed_at = datetime.utcnow()
                tx.response_summary = f"Received {len(result)} fields (Mock response)"
                return result, tx

    async def _live_call(self, endpoint, data, tx):
        """Real x402 fiat USD payment flow using signed JWT tokens and prepaid USD balance."""
        if not tx.decision.should_purchase:
            tx.status = PaymentStatus.SKIPPED
            return {}, tx

        # 1. Sign JWT payment proof
        token = self.signer.sign_payment(
            amount_usd=tx.amount,
            currency=tx.currency,
            service_type=tx.service_type.value,
            supplier_id=tx.supplier_id,
        )

        # 2. Deduct from prepaid USD balance
        success = self.account.deduct(tx.amount)
        if not success:
            tx.status = PaymentStatus.FAILED
            tx.error_message = "Insufficient prepaid USD balance"
            return {}, tx

        # 3. Call endpoint with Authorization header
        headers = {
            "Authorization": f'x402-fiat token="{token}" amount="{tx.amount}" currency="{tx.currency}"'
        }

        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                # Handle 402 challenge flow if server responds with 402 first
                resp = await client.post(endpoint, json=data, timeout=10)
                if resp.status_code == 402:
                    # Resend with authorization header
                    resp = await client.post(endpoint, json=data, headers=headers, timeout=10)

                if resp.status_code in (200, 201):
                    result = resp.json()
                    tx.status = PaymentStatus.COMPLETED
                    tx.completed_at = datetime.utcnow()
                    tx.response_summary = f"Verified & Paid {len(result)} fields"
                    return result, tx
                else:
                    tx.status = PaymentStatus.FAILED
                    tx.error_message = f"HTTP {resp.status_code}"
                    return {}, tx
            except Exception as e:
                tx.status = PaymentStatus.FAILED
                tx.error_message = str(e)
                return {}, tx

    def _get_synthetic_payload(self, service_type: ServiceType) -> dict:
        """Synthetic mock payload for offline test execution."""
        if service_type == ServiceType.PRICE_INTELLIGENCE:
            return {
                "market_price_inr": 68.50,
                "historical_low_inr": 62.00,
                "historical_high_inr": 78.00,
                "confidence_score": 0.95,
            }
        else:
            return {
                "gstin_verified": True,
                "udyam_category": "Small Enterprise",
                "compliance_rating": "A+",
            }
