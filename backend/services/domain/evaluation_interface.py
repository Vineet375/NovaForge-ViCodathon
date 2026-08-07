from abc import ABC, abstractmethod
from typing import Optional
from backend.models.interview import AskedQuestion, PlannedQuestion

class AnswerEvaluationInterface(ABC):
    """Abstract interface for evaluating candidate answers and generating interview content."""
    
    @abstractmethod
    def evaluate_answer(self, question: AskedQuestion, candidate_answer: str) -> str:
        """
        Evaluate the candidate's answer.
        Returns feedback text.
        """
        pass
        
    @abstractmethod
    def generate_follow_up(self, question: AskedQuestion) -> Optional[PlannedQuestion]:
        """
        Generate a follow-up question based on the candidate's previous answer.
        Returns a PlannedQuestion if a follow-up is needed, else None.
        """
        pass
        
    @abstractmethod
    def generate_feedback(self, session_id: str) -> str:
        """
        Generate overall feedback for the entire interview session.
        Returns a comprehensive feedback string.
        """
        pass
