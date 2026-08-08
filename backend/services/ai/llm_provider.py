from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Abstract interface for LLM providers."""
    
    @abstractmethod
    def generate_question(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate an interview question."""
        pass
        
    @abstractmethod
    def generate_feedback(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate overall feedback."""
        pass
