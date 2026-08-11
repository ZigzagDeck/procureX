class MockPaymentProvider:
    """Simulates x402 payment for development."""
    def simulate_402_flow(self, amount, service_type):
        return {'status': 'completed', 'amount': amount, 'is_mock': True}
