from typing import Optional
from backend.models.candidate import Candidate
from backend.models.curriculum import Curriculum
from backend.models.interview import InterviewSession, AskedQuestion, PlannedQuestion, QuestionCategory

from backend.services.domain.evaluation_interface import AnswerEvaluationInterface
from backend.services.ai.llm_provider import LLMProvider
from backend.services.ai.prompt_engine import PromptEngine
from backend.services.ai.context_builder import ContextBuilder
from backend.services.ai.response_parser import ResponseParser

class AIService(AnswerEvaluationInterface):
    """Facade service integrating Domain context with LLM operations."""
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        
    def generate_initial_question(self, session: InterviewSession, candidate: Candidate, curriculum: Curriculum, planned: PlannedQuestion) -> str:
        """Generates the initial question based on the topic and difficulty."""
        context = ContextBuilder.build_full_context(session, candidate, curriculum)
        
        topic = "Unknown"
        if planned.curriculum_day is not None:
            for day in curriculum.days:
                if day.day == planned.curriculum_day:
                    topic = day.title
                    break
                    
        prompt = PromptEngine.build_interview_prompt(context, topic, planned.difficulty.value)
        raw_response = self.provider.generate_question(prompt)
        return ResponseParser.parse_question(raw_response)
        
    def evaluate_answer(self, question: AskedQuestion, candidate_answer: str) -> str:
        """Evaluates the given answer."""
        prompt = PromptEngine.build_evaluation_prompt(context="Evaluation Phase", question=question.question_text, answer=candidate_answer)
        raw_response = self.provider.evaluate_answer(prompt)
        return ResponseParser.parse_evaluation(raw_response)
        
    def generate_follow_up(self, question: AskedQuestion) -> Optional[PlannedQuestion]:
        """Generates a follow-up question."""
        prompt = PromptEngine.build_follow_up_prompt(context="Follow-up Phase", question=question.question_text, answer=question.answer_given or "")
        raw_response = self.provider.generate_follow_up(prompt)
        parsed_q = ResponseParser.parse_question(raw_response)
        
        if not parsed_q:
            return None
            
        return PlannedQuestion(
            category=QuestionCategory.TECHNICAL, 
            difficulty=question.planned_question.difficulty,
            curriculum_day=question.planned_question.curriculum_day
        )
        
    def generate_feedback(self, session_id: str) -> str:
        """Generates session feedback."""
        prompt = PromptEngine.build_feedback_prompt(context="Feedback Phase", history=f"Session: {session_id}")
        raw_response = self.provider.generate_feedback(prompt)
        return ResponseParser.parse_evaluation(raw_response)
