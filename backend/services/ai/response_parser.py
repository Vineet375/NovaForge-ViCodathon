import re
from backend.services.ai.exceptions import InvalidResponseException

class ResponseParser:
    """Parses and normalizes raw text responses from the LLM."""
    
    @staticmethod
    def parse_question(raw_response: str) -> str:
        """
        Cleans the LLM response to extract just the question text.
        Strips quotes, introductory phrases, and whitespace.
        """
        if not raw_response or not raw_response.strip():
            raise InvalidResponseException("LLM returned an empty response.")
            
        cleaned = raw_response.strip()
        
        # Remove common chatty prefixes
        prefixes_to_remove = [
            r"^here is your question:?",
            r"^the question is:?",
            r"^question:?"
        ]
        
        for pattern in prefixes_to_remove:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()
            
        # Remove surrounding quotes
        if cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = cleaned[1:-1].strip()
            
        if not cleaned:
            raise InvalidResponseException("Parsed response resulted in empty string.")
            
        return cleaned

    @staticmethod
    def parse_evaluation(raw_response: str) -> str:
        """
        Cleans the evaluation feedback.
        """
        if not raw_response or not raw_response.strip():
            raise InvalidResponseException("LLM returned empty evaluation.")
            
        return raw_response.strip()
