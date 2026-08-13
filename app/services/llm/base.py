from abc import ABC, abstractmethod

class LLMBase(ABC):
    
    @abstractmethod
    def analyze(self, offer_text: str) -> dict:
        """
        Analyzes a job offer and returns a structured assessment.
        """
        pass

    @abstractmethod
    def complete(self, prompt: str) -> dict:
        """
        Generic method for LLM completion with a custom prompt.
        
        Args:
            prompt: Custom prompt string
            
        Returns:
            Parsed JSON response as dict
        """
        pass