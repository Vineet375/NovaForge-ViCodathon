from backend.models.candidate import Candidate
from backend.models.curriculum import Curriculum
from backend.models.interview import AskedQuestion, InterviewSession


class ContextBuilder:
    """Builds optimized context strings for the LLM based on domain models."""

    @staticmethod
    def build_candidate_context(candidate: Candidate) -> str:
        """Extract a concise candidate profile for prompt context."""
        return (
            f"Name: {candidate.member.name}\n"
            f"Role: {candidate.member.jobRole}\n"
            f"Experience: {candidate.member.yearsExperience} years\n"
            f"Education: {candidate.member.education}"
        )

    @staticmethod
    def build_curriculum_context(curriculum: Curriculum, day_number: int) -> str:
        """Extract curriculum information for a specific day."""
        for day in curriculum.days:
            if day.day == day_number:
                objectives = ", ".join(day.objectives)
                tools = (
                    ", ".join(day.tools)
                    if hasattr(day, "tools") and day.tools
                    else "N/A"
                )
                return (
                    f"Topic: {day.title} (Day {day.day})\n"
                    f"Objectives: {objectives}\n"
                    f"Tools Learned: {tools}"
                )
        return "Topic Context: Unknown."

    @staticmethod
    def build_history_context(session: InterviewSession) -> str:
        """Build a full Q&A transcript from the session history."""
        if not session.questions_asked:
            return "Interview just started. No previous history."

        history = []
        for i, q in enumerate(session.questions_asked, 1):
            ans = q.answer_given if q.answer_given else "No answer provided yet."
            history.append(
                f"Q{i} (Day {q.planned_question.curriculum_day}): {q.question_text}\n"
                f"A{i}: {ans}"
            )
        return "\n\n".join(history)

    @staticmethod
    def build_history_context_for_question(question: AskedQuestion) -> str:
        """Build a minimal context string for a single question/answer pair."""
        ans = question.answer_given or "No answer yet."
        return (
            f"Question: {question.question_text}\n"
            f"Candidate Answer: {ans}"
        )

    @staticmethod
    def build_candidate_summary_context(session: InterviewSession) -> str:
        """Build a high-level summary context for the feedback prompt."""
        total = session.current_question_number
        scores = [
            q.score
            for q in session.questions_asked
            if getattr(q, "score", None) is not None
        ]
        avg = sum(scores) / len(scores) if scores else 0
        return (
            f"Session ID: {session.session_id}\n"
            f"Difficulty: {session.difficulty_level.value}\n"
            f"Total Questions: {total}\n"
            f"Average Score: {avg:.1f}/10"
        )

    @staticmethod
    def build_full_context(
        session: InterviewSession,
        candidate: Candidate,
        curriculum: Curriculum,
    ) -> str:
        """Combine all context into a single optimized string for question generation."""
        c_context = ContextBuilder.build_candidate_context(candidate)

        curr_context = ""
        if session.current_curriculum_day is not None:
            curr_context = ContextBuilder.build_curriculum_context(
                curriculum, session.current_curriculum_day
            )

        hist_context = ContextBuilder.build_history_context(session)

        total_questions = 4
        asked = len(session.questions_asked)
        remaining = max(0, total_questions - asked)
        plan_context = (
            f"Total Questions Planned: {total_questions}. "
            f"Asked: {asked}. Remaining: {remaining}."
        )

        return (
            f"--- CANDIDATE PROFILE ---\n{c_context}\n\n"
            f"--- INTERVIEW PLAN ---\n{plan_context}\n"
            f"Target Difficulty: {session.difficulty_level.value}\n\n"
            f"--- CURRENT TOPIC ---\n{curr_context}\n\n"
            f"--- INTERVIEW HISTORY ---\n{hist_context}"
        )
