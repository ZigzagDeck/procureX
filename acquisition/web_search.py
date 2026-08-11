"""Web search source adapter using DuckDuckGo."""
import asyncio
from urllib.parse import urlparse
import httpx
from acquisition.base import ResearchSource, SearchResult, FetchedContent
from acquisition.rate_limiter import RateLimiter

class WebSearchSource(ResearchSource):
    def __init__(self):
        super().__init__(name='web_search')
        self._rate_limiter = RateLimiter(min_delay=2.0)
        self._client = httpx.AsyncClient(timeout=15.0, headers={'User-Agent': 'Mozilla/5.0 (compatible; ProcureX/1.0)'}, follow_redirects=True)
    async def search(self, query, max_results=10, **kwargs):
        try:
            from duckduckgo_search import DDGS
            await self._rate_limiter.wait('duckduckgo.com')
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(None, lambda: list(DDGS().text(query, max_results=max_results)))
            return [SearchResult(title=r.get('title',''), url=r.get('href',r.get('link','')), snippet=r.get('body',r.get('snippet','')), source_name=self.name) for r in results]
        except Exception: return []
    async def fetch(self, url):
        domain = urlparse(url).netloc
        await self._rate_limiter.wait(domain)
        try:
            resp = await self._client.get(url)
            return FetchedContent(url=url, content=resp.text, status_code=resp.status_code, source_name=self.name)
        except Exception as e:
            return FetchedContent(url=url, content='', status_code=0, source_name=self.name, error=str(e))
    def is_available(self):
        try:
            from duckduckgo_search import DDGS
            return True
        except ImportError: return False
    async def close(self): await self._client.aclose()
