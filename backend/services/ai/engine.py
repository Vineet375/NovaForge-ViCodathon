import json
import logging
import os
from typing import List

from backend.services.ai.exceptions import LLMRateLimitException, LLMFailureException
from backend.services.ai.llm_provider import LLMProvider
from backend.services.ai.providers.base import BaseAIProvider
from backend.services.ai.providers.gemini import GeminiProvider
from backend.services.ai.providers.nvidia import NvidiaProvider
from backend.services.ai.providers.mock import MockProvider
from backend.utils.logger import logger


class AIEngine(LLMProvider):
    """
    Chain of Responsibility orchestrator for AI providers.
    Falls back gracefully across providers.
    """

    def __init__(self, test_mode: bool = False):
        env = os.getenv("ENVIRONMENT", "development")
        if test_mode or env == "test":
            logger.info("AIEngine: Running in explicit TEST mode. Using MockProvider only.")
            self.providers = [MockProvider()]
        else:
            self.providers = [
                GeminiProvider(),
                NvidiaProvider(),
                MockProvider(),
            ]

    def _execute_with_failover(self, action_name: str, method_name: str, prompt: str) -> str:
        last_exception = None
        
        for provider in self.providers:
            try:
                method = getattr(provider, method_name)
                logger.info(f"AIEngine: Attempting {action_name} with {provider.provider_name}...")
                return method(prompt)
            except LLMRateLimitException as e:
                logger.warning(f"AIEngine: {provider.provider_name} failed with Rate Limit: {str(e)}")
                last_exception = e
                continue
            except LLMFailureException as e:
                logger.warning(f"AIEngine: {provider.provider_name} failed: {str(e)}")
                last_exception = e
                continue
            except Exception as e:
                logger.error(f"AIEngine: {provider.provider_name} encountered unexpected error: {str(e)}")
                last_exception = e
                continue
                
        raise Exception(f"All AI providers exhausted for {action_name}. Last error: {str(last_exception)}")

    def generate_question(self, prompt: str) -> str:
        return self._execute_with_failover("generate_question", "generate_question", prompt)

    def evaluate_answer(self, prompt: str) -> str:
        return self._execute_with_failover("evaluate_answer", "evaluate_answer", prompt)

    def generate_follow_up(self, prompt: str) -> str:
        return self._execute_with_failover("generate_follow_up", "generate_follow_up", prompt)

    def generate_feedback(self, prompt: str) -> str:
        return self._execute_with_failover("generate_feedback", "generate_feedback", prompt)
