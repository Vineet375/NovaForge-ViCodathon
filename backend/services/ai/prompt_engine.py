class PromptEngine:
    """Builds structured prompts for the AI interview engine."""
    
    @staticmethod
    def build_interview_prompt(context: str, topic: str, difficulty: str) -> str:
        """Build a prompt to generate an initial interview question."""
        return f"""
You are an expert technical interviewer.
Context: {context}

Generate an interview question for the topic '{topic}' at a '{difficulty}' difficulty level.
Return ONLY the question text. Do not include any greetings or extraneous formatting.
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
Return ONLY the question text. Do not include any greetings or extraneous formatting.
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
"""
