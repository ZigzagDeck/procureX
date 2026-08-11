from datetime import datetime

class SupplierVerificationService:
    def verify(self, supplier_name: str, gstin: str, address: str, claimed_type: str) -> dict:
        # Mock enhanced verification
        # In production: cross-reference multiple government and commercial databases
        return {
            'gstin_status': 'ACTIVE' if gstin else 'NOT_PROVIDED',
            'registered_name': supplier_name.upper() if supplier_name else 'UNKNOWN',
            'business_type': 'Private Limited Company',
            'registration_date': '2019-07-01',
            'principal_place': address or 'Unknown',
            'msme_registered': True,
            'msme_category': 'Small',
            'type_corroboration': claimed_type.lower() if claimed_type else 'unknown',
            'verification_confidence': 0.75,
            'verified_at': datetime.utcnow().isoformat(),
            'is_mock': True,
        }
