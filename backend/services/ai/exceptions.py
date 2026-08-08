class AIEngineException(Exception):
    """Base exception for AI Engine errors."""
    pass

class LLMAuthException(AIEngineException):
    """Raised when the AI provider authentication fails."""
    pass


class LLMRateLimitException(AIEngineException):
    """Raised when the AI provider rate limit is exceeded."""
    def __init__(self, message: str = "AI rate limit exceeded.", retry_after: int = 60):
        super().__init__(message)
        self.retry_after = retry_after


class LLMFailureException(AIEngineException):
    """Raised when the LLM provider API fails."""
    pass
    
class InvalidResponseException(AIEngineException):
    """Raised when the LLM returns a malformed response that cannot be parsed."""
    pass

class ParserRecoveryFailedException(AIEngineException):
    """Raised when the robust JSON parser exhausts all recovery attempts."""
    def __init__(self, message="The AI returned an unexpected response format. Please try again."):
        super().__init__(message)

class LLMTimeoutException(AIEngineException):
    """Raised when the LLM provider API times out."""
    pass

class MissingAPIKeyException(AIEngineException):
    """Raised when the LLM API key is missing from configuration."""
    pass

class ConfigurationException(AIEngineException):
    """Raised when the application configuration is invalid."""
    pass
