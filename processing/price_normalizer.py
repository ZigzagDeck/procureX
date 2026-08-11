"""Price normalization for Indian B2B procurement."""
from models.supplier import PriceBasis, TaxStatus

class PriceNormalizer:
    GST_RATE = 0.18
    def normalize_unit_price(self, price_value, price_basis, tax_status, quantity_in_pack=1, total_quantity=1):
        if price_value <= 0: return 0.0
        if price_basis == PriceBasis.PER_PAIR: unit_price = price_value / 2
        elif price_basis in (PriceBasis.PER_BOX, PriceBasis.PER_CARTON): unit_price = price_value / max(quantity_in_pack, 1)
        elif price_basis == PriceBasis.TOTAL: unit_price = price_value / max(total_quantity, 1)
        else: unit_price = price_value
        if tax_status == TaxStatus.GST_INCLUSIVE: unit_price = unit_price / (1 + self.GST_RATE)
        return round(unit_price, 2)
    def is_within_budget(self, normalized_price, max_price):
        if max_price is None: return True
        return normalized_price <= max_price
    def price_competitiveness_score(self, normalized_price, max_price):
        if max_price is None or max_price <= 0: return 0.5
        if normalized_price <= 0: return 0.0
        ratio = normalized_price / max_price
        if ratio <= 0.5: return 1.0
        elif ratio <= 1.0: return 1.0 - (ratio - 0.5) * 1.0
        else: return max(0.0, 0.5 - (ratio - 1.0) * 0.5)
