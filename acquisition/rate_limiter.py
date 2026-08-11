"""Rate limiter for respectful web access."""
import asyncio, time
from collections import defaultdict

class RateLimiter:
    def __init__(self, min_delay: float = 2.0):
        self._last_request = defaultdict(float)
        self._min_delay = min_delay
    async def wait(self, domain: str) -> None:
        now = time.time()
        elapsed = now - self._last_request[domain]
        if elapsed < self._min_delay:
            await asyncio.sleep(self._min_delay - elapsed)
        self._last_request[domain] = time.time()
    def reset(self, domain=None):
        if domain: self._last_request.pop(domain, None)
        else: self._last_request.clear()
