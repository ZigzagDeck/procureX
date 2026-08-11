"""Pluggable Udyam/MSME verification."""
class UdyamVerifier:
    def __init__(self, mode='mock'): self.mode = mode
    async def verify(self, udyam_number):
        if not udyam_number: return {'status':'NOT_PROVIDED'}
        if self.mode == 'mock': return self._mock_verify(udyam_number)
        return {'status':'UNAVAILABLE','error':'Live Udyam API not configured'}
    def _mock_verify(self, udyam_number):
        return {'udyam_number':udyam_number,'enterprise_name':f'Mock Enterprise {udyam_number[-4:]}','category':'Small','activity':'Manufacturing','state':'Unknown','date_of_registration':'2021-03-15','is_mock':True}
