from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='ProcureX Intelligence Services')

class PriceIntelRequest(BaseModel):
    product_category: str
    material: str
    application: str = ''
    size: str = ''
    quantity: int = 1000
    region: str = ''

@app.post('/v1/price-intelligence')
def price_intel(req: PriceIntelRequest):
    from intelligence.price_intelligence import PriceIntelligenceService
    svc = PriceIntelligenceService()
    return svc.analyze(req.product_category, req.material, req.application, req.size, req.quantity, req.region)
