import json
import re
from backend.services.ai.exceptions import InvalidResponseException

class ResponseParser:
    """Parses and normalizes raw JSON responses from the LLM."""
    
    @staticmethod
    def _extract_json(raw_response: str) -> dict:
        if not raw_response or not raw_response.strip():
            raise InvalidResponseException("LLM returned an empty response.")
            
        cleaned = raw_response.strip()
        
        # Remove markdown code fences if present
        if cleaned.startswith("```"):
            # strip first line
            cleaned = re.sub(r"^```(?:json)?\n?", "", cleaned)
            # strip last line
            cleaned = re.sub(r"\n?```$", "", cleaned)
            
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise InvalidResponseException(f"Failed to parse JSON: {str(e)}\nRaw Response: {raw_response}")

    @staticmethod
    def parse_question(raw_response: str) -> str:
        """
        Extracts the question_text from the structured JSON response.
        """
        data = ResponseParser._extract_json(raw_response)
        if "question_text" not in data:
            raise InvalidResponseException("Parsed JSON missing 'question_text' field.")
        return data["question_text"]

    @staticmethod
    def parse_evaluation(raw_response: str) -> str:
        """
        Extracts the feedback from the structured JSON response.
        For this simplified parser, we just return the feedback string.
        A more advanced implementation would return a structured domain object.
        """
        data = ResponseParser._extract_json(raw_response)
        if "feedback" not in data:
            raise InvalidResponseException("Parsed JSON missing 'feedback' field.")
        return data["feedback"]
        
    @staticmethod
    def parse_full_evaluation(raw_response: str) -> dict:
        """
        Extracts the full evaluation object for internal use.
        """
        return ResponseParser._extract_json(raw_response)
        
    @staticmethod
    def parse_final_feedback(raw_response: str) -> dict:
        """
        Extracts the structured final feedback object.
        """
        return ResponseParser._extract_json(raw_response)
