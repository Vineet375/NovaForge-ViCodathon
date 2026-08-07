from abc import ABC, abstractmethod
from typing import Optional
from backend.models.interview import AskedQuestion, PlannedQuestion

class AnswerEvaluationInterface(ABC):
    """Abstract interface for evaluating candidate answers and generating interview content."""
    
    @abstractmethod
    def evaluate_answer(self, question: AskedQuestion, candidate_answer: str) -> dict:
        """
        Evaluate the candidate's answer.
        Returns evaluation dict.
        """
        pass
        
    @abstractmethod
    def generate_follow_up(self, question: AskedQuestion) -> Optional[AskedQuestion]:
        """
        Generate a follow-up question based on the candidate's previous answer.
        Returns an AskedQuestion if a follow-up is needed, else None.
        """
        pass
        
    @abstractmethod
    def generate_feedback(self, session_id: str) -> dict:
        """
        Generate overall feedback for the entire interview session.
        Returns a comprehensive feedback dict.
        """
        pass
