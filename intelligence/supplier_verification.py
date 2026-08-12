"""Extensible stub for supplier verification service."""

class SupplierVerificationService:
    """Extensible stub for supplier verification service (deactivated for presentation build)."""
    def verify(self, supplier_name, gstin='', address='', claimed_type='unknown') -> dict:
        return {
            'status': 'DEACTIVATED',
            'supplier_name': supplier_name,
            'message': 'Supplier verification service is deactivated in current release.',
            'is_mock': True,
        }
