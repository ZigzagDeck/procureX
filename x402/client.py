import os
import httpx
from models.budget import PaymentTransaction, PaymentStatus, ServiceType, PaymentDecision
from datetime import datetime

class X402Client:
    def __init__(self):
        self.mode = os.environ.get('PROCUREX_X402_MODE', 'mock')
        self.base_url = os.environ.get('PROCUREX_INTEL_SERVICE_URL', 'http://localhost:8000')
    
    async def call_service(self, service_type: ServiceType, request_data: dict, decision: PaymentDecision) -> tuple[dict, PaymentTransaction]:
        """Call intelligence service, handling x402 payment flow."""
        endpoint = '/v1/price-intelligence' if service_type == ServiceType.PRICE_INTELLIGENCE else '/v1/supplier-verification'
        
        tx = PaymentTransaction(
            service_type=service_type, supplier_id=decision.supplier_id,
            amount=decision.cost, decision=decision,
        )
        
        if self.mode == 'mock':
            return await self._mock_call(endpoint, request_data, tx)
        else:
            return await self._live_call(endpoint, request_data, tx)
    
    async def _mock_call(self, endpoint, data, tx):
        """Simulate x402 flow: 402 -> sign -> 200."""
        # Simulate the 402 challenge-response
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                resp = await client.post(endpoint, json=data, timeout=10)
                if resp.status_code == 200:
                    result = resp.json()
                    tx.status = PaymentStatus.COMPLETED
                    tx.completed_at = datetime.utcnow()
                    tx.response_summary = f"Received {len(result)} fields"
                    return result, tx
                else:
                    tx.status = PaymentStatus.FAILED
                    tx.error_message = f"HTTP {resp.status_code}"
                    return {}, tx
            except Exception as e:
                tx.status = PaymentStatus.FAILED
                tx.error_message = str(e)
                return {}, tx
    
    async def _live_call(self, endpoint, data, tx):
        """Real x402 payment flow using official SDK."""
        # In production: use x402 SDK to handle 402 challenge
        tx.status = PaymentStatus.FAILED
        tx.error_message = 'Live x402 not configured for MVP'
        return {}, tx
