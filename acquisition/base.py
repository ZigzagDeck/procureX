"""ResearchSource abstract interface for pluggable data sources."""
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from datetime import datetime

class SearchResult(BaseModel):
    title: str = ''
    url: str = ''
    snippet: str = ''
    source_name: str = ''
    metadata: dict = Field(default_factory=dict)
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)

class FetchedContent(BaseModel):
    url: str
    content: str = ''
    status_code: int = 200
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    source_name: str = ''
    error: str = ''

class ResearchSource(ABC):
    def __init__(self, name: str): self.name = name
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> list[SearchResult]: ...
    @abstractmethod
    async def fetch(self, url: str) -> FetchedContent: ...
    def is_available(self) -> bool: return True
