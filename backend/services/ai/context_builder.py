from backend.models.candidate import Candidate
from backend.models.curriculum import Curriculum
from backend.models.interview import InterviewSession

class ContextBuilder:
    """Builds optimized context strings for the LLM based on domain models."""
    
    @staticmethod
    def build_candidate_context(candidate: Candidate) -> str:
        """Extract relevant candidate profile information."""
        return f"""Name: {candidate.member.name}
Role: {candidate.member.jobRole}
Experience: {candidate.member.yearsExperience} years"""

    @staticmethod
    def build_curriculum_context(curriculum: Curriculum, day_number: int) -> str:
        """Extract curriculum information for a specific day."""
        for day in curriculum.days:
            if day.day == day_number:
                objectives = ", ".join(day.objectives)
                tools = ", ".join(day.tools) if hasattr(day, 'tools') and day.tools else "N/A"
                return f"Topic: {day.title} (Day {day.day})\nObjectives: {objectives}\nTools Learned: {tools}"
        return "Topic Context: Unknown."

    @staticmethod
    def build_history_context(session: InterviewSession) -> str:
        """Extract previous questions and answers from the session."""
        if not session.questions_asked:
            return "Interview just started. No previous history."
            
        history = []
        for i, q in enumerate(session.questions_asked, 1):
            ans = q.answer_given if q.answer_given else "No answer provided yet."
            score = ""
            # If we started storing structured feedback score
            if q.feedback and "score" in q.feedback.lower():
                pass
            history.append(f"Q{i} (Day {q.planned_question.curriculum_day}): {q.question_text}\nA{i}: {ans}")
            
        return "\n\n".join(history)
        
    @staticmethod
    def build_full_context(session: InterviewSession, candidate: Candidate, curriculum: Curriculum) -> str:
        """Combine all context into a single optimized string for the LLM."""
        c_context = ContextBuilder.build_candidate_context(candidate)
        
        curr_context = ""
        if session.current_curriculum_day is not None:
            curr_context = ContextBuilder.build_curriculum_context(curriculum, session.current_curriculum_day)
            
        hist_context = ContextBuilder.build_history_context(session)
        
        # Calculate remaining plan
        total_questions = 8  # Milestone 6 requirement
        asked = len(session.questions_asked)
        remaining = max(0, total_questions - asked)
        
        plan_context = f"Total Questions Planned: {total_questions}. Asked: {asked}. Remaining: {remaining}."
        
        return f"""
--- CANDIDATE PROFILE ---
{c_context}

--- INTERVIEW PLAN ---
{plan_context}
Target Difficulty: {session.difficulty_level.value}

--- CURRENT TOPIC ---
{curr_context}

--- INTERVIEW HISTORY ---
{hist_context}
"""
