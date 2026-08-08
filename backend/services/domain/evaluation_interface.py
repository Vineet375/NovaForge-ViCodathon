from abc import ABC, abstractmethod
from typing import Optional
from backend.models.interview import AskedQuestion, PlannedQuestion

class AnswerEvaluationInterface(ABC):
    """Abstract interface for evaluating candidate answers and generating interview content."""
        
    @abstractmethod
    def generate_feedback(self, session_id: str) -> dict:
        """
        Generate overall feedback for the entire interview session.
        Returns a comprehensive feedback dict.
        """
        pass
