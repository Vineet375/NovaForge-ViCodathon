import json
import re
from typing import Any, Dict

from backend.services.ai.exceptions import InvalidResponseException, ParserRecoveryFailedException


class ResponseParser:
    """Robust parser for LLM JSON responses with a 9-step recovery pipeline."""

    @staticmethod
    def _extract_first_json_object(text: str) -> str:
        """Finds and extracts the first balanced JSON object {...} in a string."""
        start_idx = text.find("{")
        if start_idx == -1:
            raise ParserRecoveryFailedException("No JSON object found in response.")

        brace_count = 0
        in_string = False
        escape = False

        for i in range(start_idx, len(text)):
            char = text[i]

            if escape:
                escape = False
                continue

            if char == "\\":
                escape = True
                continue

            if char == '"':
                in_string = not in_string
                continue

            if not in_string:
                if char == "{":
                    brace_count += 1
                elif char == "}":
                    brace_count -= 1

                    if brace_count == 0:
                        return text[start_idx : i + 1]

        raise ParserRecoveryFailedException("Could not find a balanced JSON object.")

    @staticmethod
    def _extract_json(raw_response: str) -> dict:
        """
        Attempts to parse raw LLM output into a JSON dictionary with multiple recovery steps.
        """
        if not raw_response or not raw_response.strip():
            raise ParserRecoveryFailedException("LLM returned an empty response.")

        cleaned = raw_response.strip()

        # Step 1: Attempt raw parsing
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Step 2: Strip markdown fences and retry
        if cleaned.startswith("```"):
            stripped = re.sub(r"^```(?:json)?\n?", "", cleaned)
            stripped = re.sub(r"\n?```$", "", stripped)
            stripped = stripped.strip()
            try:
                return json.loads(stripped)
            except json.JSONDecodeError:
                pass

        # Steps 3, 4, 5, 6: Extract first balanced JSON object
        # (This naturally trims leading/trailing explanations and ignores duplicate objects)
        isolated_json = ResponseParser._extract_first_json_object(cleaned)
        try:
            return json.loads(isolated_json)
        except json.JSONDecodeError as e:
            raise ParserRecoveryFailedException(f"Failed to parse extracted JSON: {str(e)}")

    @staticmethod
    def parse_question(raw_response: str) -> str:
        """Extracts and validates the question_text from the response."""
        data = ResponseParser._extract_json(raw_response)
        
        # Step 7: Validate Schema
        if not isinstance(data, dict) or "question_text" not in data:
            raise ParserRecoveryFailedException("Parsed JSON missing 'question_text' field.")
            
        return data["question_text"]

    @staticmethod
    def parse_evaluation(raw_response: str) -> str:
        """Extracts the feedback from the structured JSON response."""
        data = ResponseParser._extract_json(raw_response)
        
        if not isinstance(data, dict) or "feedback" not in data:
            raise ParserRecoveryFailedException("Parsed JSON missing 'feedback' field.")
            
        return data["feedback"]

    @staticmethod
    def parse_full_evaluation(raw_response: str) -> dict:
        """Extracts and validates the full evaluation object."""
        data = ResponseParser._extract_json(raw_response)
        
        required_keys = {"feedback", "score", "follow_up_required", "confidence"}
        if not isinstance(data, dict) or not required_keys.issubset(data.keys()):
            raise ParserRecoveryFailedException(
                f"Parsed JSON missing required evaluation fields. Expected: {required_keys}"
            )
            
        return data

    @staticmethod
    def parse_final_feedback(raw_response: str) -> dict:
        """Extracts and validates the structured final feedback object."""
        data = ResponseParser._extract_json(raw_response)
        
        required_keys = {
            "interview_summary",
            "strengths",
            "weaknesses",
            "improvement_topics",
            "overall_score",
            "recommended_learning_path",
            "curriculum_references",
            "confidence_level"
        }
        if not isinstance(data, dict) or not required_keys.issubset(data.keys()):
            raise ParserRecoveryFailedException(
                f"Parsed JSON missing required feedback fields. Expected: {required_keys}"
            )
            
        return data
