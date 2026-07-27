from abc import ABC, abstractmethod

class LLMBase(ABC):
    
    @abstractmethod
    def analyze(self, offer_text: str) -> dict:
        """
        Analyzes a job offer and returns a structured assessment.
        
        Args:
            offer_text: Raw text of the job offer
            
        Returns:
            dict with keys: should_apply (bool), reasons (list), summary (str)
        """
        pass