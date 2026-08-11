"""Pluggable GST verification."""
class GSTVerifier:
    def __init__(self, mode='mock'): self.mode = mode
    async def verify(self, gstin):
        if not gstin or len(gstin) != 15: return {'status':'INVALID','error':'Invalid GSTIN format'}
        if self.mode == 'mock': return self._mock_verify(gstin)
        return {'status':'UNAVAILABLE','error':'Live GST API not configured'}
    def _mock_verify(self, gstin):
        states = {'09':'Uttar Pradesh','07':'Delhi','27':'Maharashtra','29':'Karnataka','33':'Tamil Nadu','06':'Haryana','24':'Gujarat','32':'Kerala','08':'Rajasthan','21':'Odisha'}
        return {'gstin':gstin,'status':'ACTIVE','state':states.get(gstin[:2],'Unknown'),'legal_name':f'Mock Business {gstin[2:7]}','registration_date':'2020-01-01','business_type':'Private Limited Company','is_mock':True}
