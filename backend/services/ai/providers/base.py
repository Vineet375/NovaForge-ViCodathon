from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    """Abstract interface for AI providers."""
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the provider (for logging)."""
        pass

    @abstractmethod
    def generate_question(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate an interview question."""
        pass
        

        
    @abstractmethod
    def generate_feedback(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate overall feedback."""
        pass
