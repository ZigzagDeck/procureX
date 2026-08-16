from models.supplier import Supplier
from datetime import datetime, timezone
import random
from statistics import median


def get_market_price_estimate(reference_prices: list[float]) -> dict:
    """Build an offline market-price estimate from trusted session prices."""
    prices = [price for price in reference_prices if price is not None and price > 0]
    if not prices:
        return {"market_price": None, "sample_size": 0, "basis": "INR per piece"}
    return {
        "market_price": round(float(median(prices)), 2),
        "sample_size": len(prices),
        "basis": "INR per piece",
    }

class PriceIntelligenceService:
    """Generates market price intelligence for a product category."""

    def analyze(self, product_category: str, material: str, application: str, size: str, quantity: int, region: str) -> dict:
        """Generate price intelligence report."""
        # In production: aggregate from multiple real sources (IndiaMART, TradeIndia, commodity APIs)
        # For MVP: generate realistic market data based on domain knowledge

        # Dynamic market price lookup by category (INR, GST-exclusive)
        category_index = {
            'safety_gloves': {'min': 35, 'max': 120, 'median': 65},
            'safety_helmets': {'min': 150, 'max': 650, 'median': 320},
            'safety_shoes': {'min': 450, 'max': 2200, 'median': 950},
            'face_shields': {'min': 40, 'max': 250, 'median': 110},
            'industrial_masks': {'min': 15, 'max': 180, 'median': 60},
        }

        cat_key = product_category.lower().replace(' ', '_')
        base = category_index.get(cat_key, {'min': 100, 'max': 500, 'median': 250})

        # Quantity discount factor
        qty_factor = 0.85 if quantity >= 10000 else 0.92 if quantity >= 5000 else 1.0

        return {
            'product_category': product_category,
            'market_price_range': {
                'min': round(base['min'] * qty_factor, 2),
                'max': round(base['max'] * qty_factor, 2),
                'median': round(base['median'] * qty_factor, 2),
                'currency': 'INR',
            },
            'price_trend': 'stable',
            'quantity_discount_applicable': quantity >= 5000,
            'data_sources_count': 14,
            'confidence': 0.85,
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'is_mock': True,
        }
