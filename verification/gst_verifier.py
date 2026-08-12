"""Pluggable GST verification."""
class GSTVerifier:
    def __init__(self, mode='mock'): self.mode = mode

    async def verify(self, gstin):
        import os, httpx
        if not gstin or len(gstin) != 15:
            return {'status': 'INVALID', 'error': 'Invalid GSTIN format'}

        api_key = os.environ.get('SANDBOX_API_KEY', '')
        if self.mode == 'live' and api_key:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        f"https://api.sandbox.co.in/gstin/{gstin}",
                        headers={"Authorization": api_key, "x-api-key": api_key},
                        timeout=8.0
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        return {
                            'gstin': gstin,
                            'status': data.get('sts', 'ACTIVE'),
                            'state': data.get('stj', 'Unknown'),
                            'legal_name': data.get('lrgName', 'Verified Business'),
                            'registration_date': data.get('rgdt', '2020-01-01'),
                            'business_type': data.get('ctb', 'Private Limited Company'),
                            'is_mock': False
                        }
            except Exception:
                pass

        return self._mock_verify(gstin)

    def _mock_verify(self, gstin):
        states = {
            '09': 'Uttar Pradesh', '07': 'Delhi', '27': 'Maharashtra',
            '29': 'Karnataka', '33': 'Tamil Nadu', '06': 'Haryana',
            '24': 'Gujarat', '32': 'Kerala', '08': 'Rajasthan',
            '21': 'Odisha'
        }
        return {
            'gstin': gstin,
            'status': 'ACTIVE',
            'state': states.get(gstin[:2], 'Unknown'),
            'legal_name': f'Mock Business {gstin[2:7]}',
            'registration_date': '2020-01-01',
            'business_type': 'Private Limited Company',
            'is_mock': True
        }