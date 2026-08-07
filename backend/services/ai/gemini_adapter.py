import os
from google import genai
from backend.services.ai.llm_provider import LLMProvider
from backend.services.ai.exceptions import MissingAPIKeyException, InvalidResponseException
from backend.utils.logger import logger

class GeminiAdapter(LLMProvider):
    """
    Adapter for Google's Gemini LLM using the official google-genai SDK. 
    Implements the LLMProvider interface securely.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise MissingAPIKeyException("GEMINI_API_KEY environment variable is not set.")
            
        try:
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = "gemini-2.5-flash"
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
            
    def _call_gemini(self, prompt: str, max_retries: int = 3) -> str:
        """Helper to call Gemini API with error handling and retries."""
        last_exception = None
        for attempt in range(max_retries):
            try:
                logger.info(f"Calling Gemini API (Attempt {attempt + 1}/{max_retries})...")
                # We explicitly ask Gemini to respond in JSON format
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                
                if not response.text:
                    raise InvalidResponseException("Empty response from Gemini API.")
                    
                return response.text
            except Exception as e:
                logger.error(f"Gemini API call failed on attempt {attempt + 1}: {str(e)}")
                last_exception = e
                
        raise InvalidResponseException(f"Gemini API error after {max_retries} retries: {str(last_exception)}")
        
    def generate_question(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate an interview question."""
        return self._call_gemini(prompt)
        
    def evaluate_answer(self, prompt: str) -> str:
        """Sends the prompt to the LLM to evaluate an answer."""
        return self._call_gemini(prompt)
        
    def generate_follow_up(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate a follow-up question."""
        return self._call_gemini(prompt)
        
    def generate_feedback(self, prompt: str) -> str:
        """Sends the prompt to the LLM to generate overall feedback."""
        return self._call_gemini(prompt)
