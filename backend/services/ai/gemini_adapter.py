import os

from google import genai
from google.genai.errors import APIError

from backend.services.ai.exceptions import (
    ConfigurationException,
    InvalidResponseException,
    LLMFailureException,
    LLMTimeoutException,
    MissingAPIKeyException,
)
from backend.services.ai.llm_provider import LLMProvider
from backend.utils.logger import logger


def _sanitize_error(message: str, api_key: str) -> str:
    """Remove the API key from error messages before logging."""
    if api_key and api_key in message:
        return message.replace(api_key, "[REDACTED]")
    return message


class GeminiAdapter(LLMProvider):
    """
    Adapter for Google's Gemini LLM using the official google-genai SDK.
    Reads model name from the GEMINI_MODEL environment variable.
    Raises ConfigurationException on startup if either variable is missing.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise MissingAPIKeyException(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.model_name = os.getenv("GEMINI_MODEL")
        if not self.model_name:
            raise ConfigurationException(
                "GEMINI_MODEL environment variable is not set."
            )

        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            logger.error(
                f"Failed to initialize Gemini client: "
                f"{_sanitize_error(str(e), self.api_key)}"
            )
            raise LLMFailureException(
                "The AI model is currently unavailable. Please contact the administrator."
            )

    def _call_gemini(self, prompt: str, max_retries: int = 3) -> str:
        """Call the Gemini API with retry logic for transient failures."""
        last_exception: Exception = LLMFailureException(
            "The AI service is currently unavailable. Please try again."
        )

        for attempt in range(max_retries):
            try:
                logger.info(f"Calling Gemini API (Attempt {attempt + 1}/{max_retries})...")
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        response_mime_type="application/json",
                        max_output_tokens=2048,
                    ),
                )

                if not response.text:
                    raise InvalidResponseException(
                        "The AI service returned an empty response. Please try again."
                    )

                return response.text

            except APIError as e:
                code = getattr(e, "code", None)
                sanitized = _sanitize_error(str(e), self.api_key)
                logger.error(
                    f"Gemini APIError on attempt {attempt + 1}: "
                    f"code={code} message={sanitized}"
                )

                if code == 401:
                    raise LLMFailureException("AI authentication failed. Check your GEMINI_API_KEY.")
                elif code == 404:
                    raise LLMFailureException(
                        f"The configured Gemini model '{self.model_name}' is unavailable or "
                        "deprecated. Please update GEMINI_MODEL in your .env file."
                    )
                elif code == 429:
                    last_exception = LLMFailureException(
                        "The AI service is busy. Please try again shortly."
                    )
                    continue
                else:
                    last_exception = LLMFailureException(
                        "The AI service encountered an error. Please try again."
                    )
                    continue

            except TimeoutError as e:
                logger.error(
                    f"Gemini API timeout on attempt {attempt + 1}: "
                    f"{_sanitize_error(str(e), self.api_key)}"
                )
                last_exception = LLMTimeoutException(
                    "The AI service took too long to respond. Please try again."
                )
                continue

            except Exception as e:
                logger.error(
                    f"Unexpected Gemini API error on attempt {attempt + 1}: "
                    f"{_sanitize_error(str(e), self.api_key)}",
                    exc_info=True,
                )
                last_exception = LLMFailureException(
                    "The AI service is currently unavailable. Please try again."
                )
                continue

        raise last_exception

    def generate_question(self, prompt: str) -> str:
        """Send the prompt to the LLM to generate an interview question."""
        return self._call_gemini(prompt)

    def evaluate_answer(self, prompt: str) -> str:
        """Send the prompt to the LLM to evaluate a candidate's answer."""
        return self._call_gemini(prompt)

    def generate_follow_up(self, prompt: str) -> str:
        """Send the prompt to the LLM to generate a follow-up question."""
        return self._call_gemini(prompt)

    def generate_feedback(self, prompt: str) -> str:
        """Send the prompt to the LLM to generate the final feedback report."""
        return self._call_gemini(prompt)
