import os
from google import genai
from google.genai.errors import APIError
from backend.services.ai.llm_provider import LLMProvider
from backend.services.ai.exceptions import (
    MissingAPIKeyException, 
    ConfigurationException,
    InvalidResponseException,
    LLMFailureException,
    LLMTimeoutException
)
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
            
        self.model_name = os.getenv("GEMINI_MODEL")
        if not self.model_name:
            raise ConfigurationException("GEMINI_MODEL environment variable is not set.")
            
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}", exc_info=True)
            raise LLMFailureException("The AI model is currently unavailable. Please contact the administrator.")
            
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
                        response_mime_type="application/json",
                        max_output_tokens=2048
                    )
                )
                
                if not response.text:
                    logger.error("Empty response from Gemini API.")
                    raise InvalidResponseException("The AI service returned an empty response. Please try again.")
                    
                return response.text
                
            except APIError as e:
                code = getattr(e, 'code', getattr(e, 'status', None))
                # For `google.genai`, if code is None, parse string or just fallback to 500
                if code is None:
                    code = e.code if hasattr(e, 'code') else 500
                    
                logger.error(f"Gemini APIError on attempt {attempt + 1}: code={code} message={str(e)}")
                
                if code == 401:
                    raise LLMFailureException("AI authentication failed.")
                elif code == 404:
                    raise LLMFailureException("The AI model is currently unavailable. Please contact the administrator.")
                elif code == 429:
                    last_exception = LLMFailureException("The AI service is busy. Please try again shortly.")
                    continue # Retry on 429
                else:
                    last_exception = LLMFailureException("The AI service encountered an error. Please try again.")
                    continue
                    
            except TimeoutError as e:
                logger.error(f"Gemini API Timeout on attempt {attempt + 1}: {str(e)}")
                last_exception = LLMTimeoutException("The AI service took too long to respond.")
                continue
                
            except Exception as e:
                logger.error(f"Unexpected Gemini API error on attempt {attempt + 1}: {str(e)}", exc_info=True)
                last_exception = LLMFailureException("The AI service is currently unavailable. Please try again.")
                continue
                
        # If we exhausted retries
        if last_exception:
            raise last_exception
        raise LLMFailureException("The AI service is currently unavailable. Please try again.")
        
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
