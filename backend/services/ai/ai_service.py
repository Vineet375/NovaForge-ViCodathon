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
import difflib
import re

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
        
        max_attempts = 3
        last_q_text = ""
        
        for attempt in range(max_attempts):
            if attempt > 0:
                prompt += "\n\nCRITICAL: Do NOT repeat any previous questions. The question you just generated was too similar to one already asked."
                
            q_text = self._generate_with_retry(
                prompt=prompt,
                generate_func=self.provider.generate_question,
                parse_func=ResponseParser.parse_question
            )
            last_q_text = q_text
            
            is_duplicate = False
            normalized_q = re.sub(r'[^a-z0-9]', '', q_text.lower())
            
            for past_q in session.questions_asked:
                normalized_past = re.sub(r'[^a-z0-9]', '', past_q.question_text.lower())
                similarity = difflib.SequenceMatcher(None, normalized_q, normalized_past).ratio()
                if similarity > 0.8:
                    is_duplicate = True
                    break
                    
            if not is_duplicate:
                return q_text
                
        # If all attempts yield duplicates, return the last generated one to let failover/safe handling catch it 
        # or rely on normal progression.
        return last_q_text



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
