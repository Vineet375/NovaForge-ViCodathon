from backend.models.candidate import Candidate
from backend.models.curriculum import Curriculum
from backend.models.interview import InterviewSession

class ContextBuilder:
    """Builds optimized context strings for the LLM based on domain models."""
    
    @staticmethod
    def build_candidate_context(candidate: Candidate) -> str:
        """Extract relevant candidate profile information."""
        return f"Candidate Name: {candidate.member.name}, Role: {candidate.member.jobRole}, Experience: {candidate.member.yearsExperience} years."

    @staticmethod
    def build_curriculum_context(curriculum: Curriculum, day_number: int) -> str:
        """Extract curriculum information for a specific day."""
        for day in curriculum.days:
            if day.day == day_number:
                objectives = ", ".join(day.objectives)
                return f"Curriculum Topic: {day.title} (Day {day.day}). Objectives: {objectives}."
        return "Topic Context: Unknown."

    @staticmethod
    def build_history_context(session: InterviewSession) -> str:
        """Extract previous questions and answers from the session."""
        if not session.questions_asked:
            return "Interview just started. No previous history."
            
        history = []
        for i, q in enumerate(session.questions_asked, 1):
            ans = q.answer_given if q.answer_given else "No answer provided yet."
            history.append(f"Q{i}: {q.question_text}\nA{i}: {ans}")
            
        return "\n\n".join(history)
        
    @staticmethod
    def build_full_context(session: InterviewSession, candidate: Candidate, curriculum: Curriculum) -> str:
        """Combine all context into a single optimized string for the LLM."""
        c_context = ContextBuilder.build_candidate_context(candidate)
        
        curr_context = ""
        if session.current_curriculum_day is not None:
            curr_context = ContextBuilder.build_curriculum_context(curriculum, session.current_curriculum_day)
            
        hist_context = ContextBuilder.build_history_context(session)
        
        return f"""
--- CANDIDATE PROFILE ---
{c_context}

--- CURRENT TOPIC ---
{curr_context}

--- INTERVIEW HISTORY ---
{hist_context}
"""
