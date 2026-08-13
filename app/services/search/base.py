from abc import ABC, abstractmethod

class WebSearchBase(ABC):
    
    @abstractmethod
    def search(self, query: str, max_results: int = 5) -> list[dict]:
        """
        Searches the web for information.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of dicts with keys: title, url, snippet
        """
        pass