from ddgs import DDGS
from app.services.search.base import WebSearchBase


class DuckDuckGoClient(WebSearchBase):

    def search(self, query: str, max_results: int = 5) -> list[dict]:
        results = []
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })
        return results
