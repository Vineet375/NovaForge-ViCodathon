from typing import Callable, Optional, TypeVar

from backend.models.candidate import Candidate
from backend.models.curriculum import Curriculum
from backend.models.interview import (
    AskedQuestion,
    InterviewSession,
    PlannedQuestion,
    QuestionCategory,
)
from backend.services.ai.context_builder import ContextBuilder
from backend.services.ai.exceptions import ParserRecoveryFailedException
from backend.services.ai.llm_provider import LLMProvider
from backend.services.ai.prompt_engine import PromptEngine
from backend.services.ai.response_parser import ResponseParser
from backend.services.domain.evaluation_interface import AnswerEvaluationInterface

T = TypeVar('T')

class AIService(AnswerEvaluationInterface):
    """Facade service integrating domain context with LLM operations."""

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def _generate_with_retry(
        self, 
        prompt: str, 
        generate_func: Callable[[str], str], 
        parse_func: Callable[[str], T]
    ) -> T:
        """
        Executes an LLM generation and parses it.
        If parsing fails, appends a strict JSON constraint and retries ONCE.
        """
        raw_response = generate_func(prompt)
        try:
            return parse_func(raw_response)
        except ParserRecoveryFailedException:
            # Step 8: Retry Gemini ONCE using a stricter prompt
            strict_constraint = (
                "\n\nCRITICAL SYSTEM INSTRUCTION: "
                "Your previous response was malformed. You MUST return ONLY a single, valid JSON object. "
                "DO NOT include markdown, code fences, introductory text, conversational filler, or trailing explanations. "
                "Output RAW JSON ONLY."
            )
            strict_prompt = prompt + strict_constraint
            raw_response_retry = generate_func(strict_prompt)
            # If this fails, it naturally raises ParserRecoveryFailedException (Step 9)
            return parse_func(raw_response_retry)

    def generate_initial_question(
        self,
        session: InterviewSession,
        candidate: Candidate,
        curriculum: Curriculum,
        planned: PlannedQuestion,
    ) -> str:
        """Generate the opening question for the given topic and difficulty."""
        context = ContextBuilder.build_full_context(session, candidate, curriculum)

        topic = "General AI/ML"
        if planned.curriculum_day is not None:
            for day in curriculum.days:
                if day.day == planned.curriculum_day:
                    topic = day.title
                    break

        prompt = PromptEngine.build_interview_prompt(
            context, topic, planned.difficulty.value
        )
        
        return self._generate_with_retry(
            prompt=prompt,
            generate_func=self.provider.generate_question,
            parse_func=ResponseParser.parse_question
        )

    def evaluate_answer(
        self, question: AskedQuestion, candidate_answer: str
    ) -> dict:
        """Evaluate a candidate's answer and return structured feedback."""
        context = ContextBuilder.build_history_context_for_question(question)
        prompt = PromptEngine.build_evaluation_prompt(
            context=context,
            question=question.question_text,
            answer=candidate_answer,
        )
        
        return self._generate_with_retry(
            prompt=prompt,
            generate_func=self.provider.evaluate_answer,
            parse_func=ResponseParser.parse_full_evaluation
        )

    def generate_follow_up(self, question: AskedQuestion) -> Optional[AskedQuestion]:
        """Generate a targeted follow-up question based on the candidate's answer."""
        context = ContextBuilder.build_history_context_for_question(question)
        prompt = PromptEngine.build_follow_up_prompt(
            context=context,
            question=question.question_text,
            answer=question.answer_given or "",
        )
        
        try:
            parsed_q = self._generate_with_retry(
                prompt=prompt,
                generate_func=self.provider.generate_follow_up,
                parse_func=ResponseParser.parse_question
            )
        except ParserRecoveryFailedException:
            return None

        planned = PlannedQuestion(
            category=QuestionCategory.TECHNICAL,
            difficulty=question.planned_question.difficulty,
            curriculum_day=question.planned_question.curriculum_day,
        )
        return AskedQuestion(question_text=parsed_q, planned_question=planned)

    def generate_feedback(self, session: InterviewSession) -> dict:
        """Generate a comprehensive final feedback report from the full interview history."""
        context = ContextBuilder.build_candidate_summary_context(session)
        history = ContextBuilder.build_history_context(session)
        prompt = PromptEngine.build_feedback_prompt(context=context, history=history)
        
        return self._generate_with_retry(
            prompt=prompt,
            generate_func=self.provider.generate_feedback,
            parse_func=ResponseParser.parse_final_feedback
        )
