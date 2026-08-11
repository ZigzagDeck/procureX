from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI(title='ProcureX Intelligence Services')

class PriceIntelRequest(BaseModel):
    product_category: str
    material: str
    application: str = ''
    size: str = ''
    quantity: int = 1000
    region: str = ''

class SupplierVerifyRequest(BaseModel):
    supplier_name: str
    gstin: str = ''
    address: str = ''
    claimed_type: str = 'unknown'

@app.post('/v1/price-intelligence')
def price_intel(req: PriceIntelRequest):
    from intelligence.price_intelligence import PriceIntelligenceService
    svc = PriceIntelligenceService()
    return svc.analyze(req.product_category, req.material, req.application, req.size, req.quantity, req.region)

@app.post('/v1/supplier-verification')
def supplier_verify(req: SupplierVerifyRequest):
    from intelligence.supplier_verification import SupplierVerificationService
    svc = SupplierVerificationService()
    return svc.verify(req.supplier_name, req.gstin, req.address, req.claimed_type)
