class PromptEngine:
    """Builds structured prompts for the AI interview engine."""
    
    _STRICT_JSON_RULE = "Return ONLY a single valid JSON object. Do not include markdown formatting, code blocks, conversational filler, or explanations."

    @staticmethod
    def build_interview_prompt(context: str, topic: str, difficulty: str) -> str:
        """Build a prompt to generate an initial interview question."""
        return f"""
You are an expert technical interviewer.
Context (Candidate Profile & History):
{context}

Generate an interview question for the topic '{topic}' at a '{difficulty}' difficulty level.
Crucially, tailor the question specifically to the candidate's exact role, years of experience, and skills from the profile above.
Ensure it is distinctly different from any questions already asked in the interview history.

{PromptEngine._STRICT_JSON_RULE}
Schema:
{{
  "question_text": "str (the question)"
}}
"""

    @staticmethod
    def build_follow_up_prompt(context: str, question: str, answer: str) -> str:
        """Build a prompt to generate a follow-up question."""
        return f"""
You are an expert technical interviewer.
Context: {context}

Original Question: {question}
Candidate's Answer: {answer}

Based on the answer, generate a single follow-up question to probe deeper or clarify a misconception.
{PromptEngine._STRICT_JSON_RULE}
Schema:
{{
  "question_text": "str (the follow-up question)"
}}
"""

    @staticmethod
    def build_evaluation_prompt(context: str, question: str, answer: str) -> str:
        """Build a prompt to evaluate an answer."""
        return f"""
You are an expert technical interviewer.
Context: {context}

Question: {question}
Candidate's Answer: {answer}

Evaluate the candidate's answer for accuracy and completeness. Provide constructive feedback.
Keep the feedback concise.
{PromptEngine._STRICT_JSON_RULE}
Schema:
{{
  "feedback": "str (concise constructive feedback)",
  "score": "int (0-10)",
  "follow_up_required": "bool",
  "confidence": "str (high, medium, low)"
}}
"""

    @staticmethod
    def build_feedback_prompt(context: str, history: str) -> str:
        """Build a prompt for overall interview feedback."""
        return f"""
You are an expert technical interviewer.
Context: {context}

Interview History:
{history}

Provide a comprehensive summary of the candidate's performance, highlighting strengths and areas for improvement.
{PromptEngine._STRICT_JSON_RULE}
Schema:
{{
  "overall_score": "int (0-100)",
  "strengths": ["str"],
  "weaknesses": ["str"],
  "improvement_topics": ["str"],
  "recommended_learning_path": "str",
  "curriculum_references": ["str"],
  "confidence_level": "str (high, medium, low)",
  "interview_summary": "str"
}}
"""
