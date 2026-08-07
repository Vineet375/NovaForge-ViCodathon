class AIEngineException(Exception):
    """Base exception for AI Engine errors."""
    pass

class LLMFailureException(AIEngineException):
    """Raised when the LLM provider API fails."""
    pass
    
class InvalidResponseException(AIEngineException):
    """Raised when the LLM returns a malformed response that cannot be parsed."""
    pass

class LLMTimeoutException(AIEngineException):
    """Raised when the LLM provider API times out."""
    pass

class MissingAPIKeyException(AIEngineException):
    """Raised when the LLM API key is missing from configuration."""
    pass
