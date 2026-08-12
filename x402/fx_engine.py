"""FX Engine for USD/INR currency conversion with rate caching and fallback support."""
import time
from typing import Optional
import httpx


class FXEngine:
    """FX Engine providing live or cached exchange rates and dual currency formatting."""

    DEFAULT_FALLBACK_RATE: float = 83.50
    CACHE_TTL_SECONDS: int = 3600

    def __init__(self, fallback_rate: float = DEFAULT_FALLBACK_RATE):
        self.fallback_rate = fallback_rate
        self._cached_rate: Optional[float] = None
        self._last_fetch_time: float = 0.0

    def get_rate(self) -> float:
        """Fetch current USD to INR exchange rate with 1-hour cache and fallback on error."""
        now = time.time()
        if self._cached_rate is not None and (now - self._last_fetch_time) < self.CACHE_TTL_SECONDS:
            return self._cached_rate

        try:
            resp = httpx.get("https://open.er-api.com/v6/latest/USD", timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                rates = data.get("rates", {})
                if "INR" in rates and isinstance(rates["INR"], (int, float)):
                    rate = float(rates["INR"])
                    if rate > 0:
                        self._cached_rate = rate
                        self._last_fetch_time = now
                        return rate
        except Exception:
            pass

        if self._cached_rate is not None:
            return self._cached_rate
        return self.fallback_rate

    def usd_to_inr(self, amount_usd: float) -> float:
        """Convert USD amount to INR rounded to 2 decimal places."""
        rate = self.get_rate()
        return round(amount_usd * rate, 2)

    def inr_to_usd(self, amount_inr: float) -> float:
        """Convert INR amount to USD rounded to 6 decimal places."""
        rate = self.get_rate()
        if rate <= 0:
            return 0.0
        return round(amount_inr / rate, 6)

    def format_dual(self, amount_usd: float) -> str:
        """Format USD amount with dual currency representation e.g. '$0.002 (₹0.17)'."""
        inr_amount = self.usd_to_inr(amount_usd)
        return f"${amount_usd:.3f} (₹{inr_amount:.2f})"
