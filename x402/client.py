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
        """Simulate true HTTP 402 handshake: 402 Challenge -> Micro-Payment Sign -> 200 OK Response."""
        from intelligence.price_intelligence import PriceIntelligenceService
        from intelligence.supplier_verification import SupplierVerificationService
        
        # Step 1: Simulate 402 Payment Required Challenge
        challenge_spec = {
            'status': 402,
            'cost_usd': tx.amount,
            'currency': 'USDC',
            'pay_to': '0x71C7656EC7ab88b098defB751B7401B5f6d8976F',
            'network': 'base-sepolia'
        }
        
        # Step 2: Sign micro-payment proof
        tx.response_summary = f"x402 Signed {challenge_spec['currency']} {challenge_spec['cost_usd']} to {challenge_spec['pay_to'][:8]}..."
        
        # Step 3: Resolve requested intelligence service payload
        if tx.service_type == ServiceType.PRICE_INTELLIGENCE:
            service = PriceIntelligenceService()
            result = service.analyze(
                product_category=data.get('product_category', 'safety_gloves'),
                material=data.get('material', 'nitrile'),
                application='industrial',
                size='M',
                quantity=data.get('quantity', 5000),
                region=data.get('region', 'India')
            )
        else:
            service = SupplierVerificationService()
            result = service.verify(
                supplier_name=data.get('supplier_name', ''),
                gstin=data.get('gstin', ''),
                address=data.get('address', ''),
                claimed_type='manufacturer'
            )
            
        tx.status = PaymentStatus.COMPLETED
        tx.completed_at = datetime.utcnow()
        return result, tx

    async def _live_call(self, endpoint, data, tx):
        """Live x402 protocol handler using HTTP 402 authorization headers."""
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                # Step 1: Initial Unauthenticated Request
                resp = await client.post(endpoint, json=data, timeout=10)
                
                # Step 2: Handle 402 Payment Required Challenge
                if resp.status_code == 402:
                    challenge_header = resp.headers.get("WWW-Authenticate", "")
                    pay_header = f"X402-Payment proof_tx_id={tx.id}"
                    
                    # Step 3: Re-issue request with payment proof
                    resp = await client.post(endpoint, json=data, headers={"Authorization": pay_header}, timeout=10)
                    
                if resp.status_code == 200:
                    result = resp.json()
                    tx.status = PaymentStatus.COMPLETED
                    tx.completed_at = datetime.utcnow()
                    tx.response_summary = f"Settled via live x402 gateway"
                    return result, tx
                else:
                    tx.status = PaymentStatus.FAILED
                    tx.error_message = f"HTTP {resp.status_code}"
                    return {}, tx
            except Exception as e:
                tx.status = PaymentStatus.FAILED
                tx.error_message = str(e)
                return {}, tx
