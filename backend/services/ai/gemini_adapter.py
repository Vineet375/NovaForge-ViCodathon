import os
from backend.services.ai.llm_provider import LLMProvider
from backend.services.ai.exceptions import MissingAPIKeyException

class GeminiAdapter(LLMProvider):
    """
    Adapter for Google's Gemini LLM. 
    Implements the LLMProvider interface using environment variables for secrets.
    As per Milestone 4 constraints, actual network calls are stubbed out.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise MissingAPIKeyException("GEMINI_API_KEY environment variable is not set.")
            
    def _simulate_api_call(self, prompt: str) -> str:
        """Stub method to simulate an API call without hitting the network."""
        return f"MOCK_RESPONSE: {prompt[:20]}..."
        
    def generate_question(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate an interview question."""
        return self._simulate_api_call(prompt)
        
    def evaluate_answer(self, prompt: str) -> str:
        """Sends the prompt to the LLM to evaluate an answer."""
        return self._simulate_api_call(prompt)
        
    def generate_follow_up(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate a follow-up question."""
        return self._simulate_api_call(prompt)
        
    def generate_feedback(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate overall feedback."""
        return self._simulate_api_call(prompt)
