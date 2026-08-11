from models.supplier import Supplier
from datetime import datetime
import random

class PriceIntelligenceService:
    """Generates market price intelligence for a product category."""
    
    def analyze(self, product_category: str, material: str, application: str, size: str, quantity: int, region: str) -> dict:
        """Generate price intelligence report."""
        # In production: aggregate from multiple real sources
        # For MVP: generate realistic market data based on domain knowledge
        
        # Nitrile safety gloves market prices (realistic range for India)
        base_prices = {
            'nitrile': {'min': 35, 'max': 120, 'median': 65},
            'latex': {'min': 20, 'max': 80, 'median': 45},
            'vinyl': {'min': 15, 'max': 60, 'median': 35},
        }
        
        prices = base_prices.get(material.lower(), base_prices['nitrile'])
        
        # Adjust for quantity discounts
        qty_factor = 1.0
        if quantity >= 10000: qty_factor = 0.9
        elif quantity >= 5000: qty_factor = 0.95
        
        return {
            'market_price_range': {
                'min': round(prices['min'] * qty_factor, 2),
                'max': round(prices['max'] * qty_factor, 2),
                'median': round(prices['median'] * qty_factor, 2),
                'currency': 'INR',
            },
            'price_trend': 'stable',
            'quantity_discount_applicable': quantity >= 5000,
            'data_sources_count': 12,
            'confidence': 0.82,
            'generated_at': datetime.utcnow().isoformat(),
            'is_mock': True,  # Flag for transparency
        }
