import os
import httpx
from openai import OpenAI

from backend.services.ai.exceptions import (
    LLMFailureException,
    LLMRateLimitException,
)
from backend.services.ai.providers.base import BaseAIProvider
from backend.utils.logger import logger


class NvidiaProvider(BaseAIProvider):
    """
    Provider for NVIDIA NIM models via OpenAI SDK.
    Supports primary and secondary model failover.
    """

    def __init__(self):
        self.configs = []
        
        key1 = os.getenv("NVIDIA_API_KEY_1")
        model1 = os.getenv("NVIDIA_MODEL_PRIMARY")
        if key1 and model1:
            self.configs.append((key1, model1))
            
        key2 = os.getenv("NVIDIA_API_KEY_2")
        model2 = os.getenv("NVIDIA_MODEL_SECONDARY")
        if key2 and model2:
            self.configs.append((key2, model2))

    @property
    def provider_name(self) -> str:
        return "NVIDIA NIM"

    def _call_nvidia(self, prompt: str) -> str:
        if not self.configs:
            raise LLMRateLimitException("No NVIDIA credentials configured. Skipping NVIDIA provider.")
            
        last_exception = None
        
        for api_key, model in self.configs:
            try:
                logger.info(f"Calling NVIDIA NIM using model {model}...")
                client = OpenAI(
                    base_url="https://integrate.api.nvidia.com/v1",
                    api_key=api_key,
                    timeout=httpx.Timeout(5.0, connect=2.0),
                    max_retries=0
                )
                
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    top_p=0.7,
                    max_tokens=2048,
                    stream=False
                )
                
                content = completion.choices[0].message.content
                if content:
                    # Strip any possible markdown blocks since we need strict JSON
                    content = content.strip()
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.startswith("```"):
                        content = content[3:]
                    if content.endswith("```"):
                        content = content[:-3]
                        
                    return content.strip()
                
            except Exception as e:
                sanitized_error = str(e).replace(api_key, "[REDACTED]") if api_key else str(e)
                logger.warning(f"NVIDIA API Error with model {model}: {sanitized_error}")
                
                # If it's a timeout or server error, failover to MockProvider immediately
                # instead of waiting for the second model to also timeout.
                if "timeout" in str(e).lower() or "50" in str(e):
                    raise LLMFailureException(f"NVIDIA NIM unavailable: {sanitized_error}")
                    
                last_exception = Exception(sanitized_error)
                continue
                
        raise LLMRateLimitException(f"NVIDIA NIM failed on all models. Last error: {str(last_exception)}")

    def generate_question(self, prompt: str) -> str:
        return self._call_nvidia(prompt)


    def generate_feedback(self, prompt: str) -> str:
        return self._call_nvidia(prompt)
