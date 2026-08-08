import os
from typing import List

from google import genai
from google.genai.errors import APIError

from backend.services.ai.exceptions import (
    ConfigurationException,
    InvalidResponseException,
    LLMFailureException,
    LLMTimeoutException,
    MissingAPIKeyException,
    LLMRateLimitException,
    LLMAuthException,
)
from backend.services.ai.providers.base import BaseAIProvider
from backend.utils.logger import logger


def _sanitize_error(message: str, api_keys: List[str]) -> str:
    """Remove all API keys from error messages before logging."""
    sanitized = message
    for key in api_keys:
        if key and key in sanitized:
            sanitized = sanitized.replace(key, "[REDACTED]")
    return sanitized


class GeminiProvider(BaseAIProvider):
    """
    Provider for Google's Gemini LLM with multi-key rotation support.
    """

    def __init__(self):
        self.api_keys = []
        for i in range(1, 10):
            key = os.getenv(f"GEMINI_API_KEY_{i}")
            if key:
                self.api_keys.append(key)
        
        # Fallback to standard key if numbered keys are missing
        if not self.api_keys:
            key = os.getenv("GEMINI_API_KEY")
            if key:
                self.api_keys.append(key)
                
        if not self.api_keys:
            raise MissingAPIKeyException(
                "No GEMINI_API_KEY variables found. Please set GEMINI_API_KEY_1, GEMINI_API_KEY_2, etc."
            )

        self.model_name = os.getenv("GEMINI_MODEL")
        if not self.model_name:
            raise ConfigurationException(
                "GEMINI_MODEL environment variable is not set."
            )
            
    @property
    def provider_name(self) -> str:
        return "Gemini"

    def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API, rotating through keys on 401, 403, 429."""
        last_exception: Exception = None

        for key_idx, current_key in enumerate(self.api_keys):
            try:
                # Need to instantiate a new client for each key since genai.Client binds the key
                client = genai.Client(api_key=current_key)
                
                logger.info(f"Calling Gemini API using key {key_idx + 1}/{len(self.api_keys)}...")
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        response_mime_type="application/json",
                        max_output_tokens=2048,
                        http_options={"timeout": 10000}
                    ),
                )

                if not response.text:
                    raise InvalidResponseException(
                        "The AI service returned an empty response. Please try again."
                    )

                return response.text

            except APIError as e:
                code = getattr(e, "code", None)
                sanitized = _sanitize_error(str(e), self.api_keys)
                logger.warning(
                    f"Gemini APIError on key {key_idx + 1}: "
                    f"code={code} message={sanitized}"
                )

                if code == 404:
                    raise LLMFailureException(
                        f"The configured Gemini model '{self.model_name}' is unavailable. Fail immediately."
                    )
                elif code in [401, 403, 429]:
                    # Rotate to next key
                    last_exception = LLMRateLimitException("The AI service is temporarily busy.")
                    continue
                else:
                    last_exception = LLMFailureException(
                        "The AI service encountered an error. Please try again."
                    )
                    continue

            except TimeoutError as e:
                logger.warning(
                    f"Gemini API timeout on key {key_idx + 1}: "
                    f"{_sanitize_error(str(e), self.api_keys)}"
                )
                last_exception = LLMTimeoutException(
                    "The AI service took too long to respond. Please try again."
                )
                continue

            except Exception as e:
                logger.error(
                    f"Unexpected Gemini API error on key {key_idx + 1}: "
                    f"{_sanitize_error(str(e), self.api_keys)}"
                )
                last_exception = LLMFailureException(
                    "The AI service is currently unavailable. Please try again."
                )
                continue

        # If all keys failed
        if isinstance(last_exception, LLMRateLimitException):
            raise last_exception
        elif last_exception:
            raise LLMRateLimitException("The AI service is temporarily busy. All keys exhausted.")
        else:
            raise LLMRateLimitException("All keys exhausted.")

    def generate_question(self, prompt: str) -> str:
        return self._call_gemini(prompt)



    def generate_feedback(self, prompt: str) -> str:
        return self._call_gemini(prompt)
