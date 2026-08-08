import json
import random

from backend.services.ai.providers.base import BaseAIProvider
from backend.utils.logger import logger


class MockProvider(BaseAIProvider):
    """
    Mock AI Provider serving as the ultimate fallback.
    Returns structured JSON mimicking the real AI responses.
    """

    def __init__(self):
        pass
    _call_count = 0

    QUESTIONS = [
        "How does the Event Loop work in Node.js and why is it important for asynchronous programming?",
        "Explain the differences between SQL and NoSQL databases. When would you choose one over the other?",
        "Describe the concept of Virtual DOM in React and how it optimizes rendering.",
        "What are microservices, and what are the main trade-offs compared to a monolithic architecture?",
        "How do you secure a REST API? Describe standard authentication and authorization patterns.",
        "Explain the SOLID principles of object-oriented design with brief examples.",
        "What is the difference between a process and a thread in an operating system?",
        "How does garbage collection work in modern high-level languages like Python or JavaScript?",
        "Describe how indexing works in a relational database and how it affects read/write performance.",
        "What is a memory leak, and how would you go about debugging one in your application?"
    ]
        
    @property
    def provider_name(self) -> str:
        return "Mock Provider"

    def _get_next_question(self) -> str:
        MockProvider._call_count += 1
        return self.QUESTIONS[MockProvider._call_count % len(self.QUESTIONS)]

    def generate_question(self, prompt: str) -> str:
        """Return a structured JSON question string."""
        logger.info("MockProvider: Generating question")
        q = self._get_next_question()
        return json.dumps({"question_text": q})

    def evaluate_answer(self, prompt: str) -> str:
        """Return a structured JSON evaluation string."""
        logger.info("MockProvider: Evaluating answer")
        return json.dumps({
            "feedback": "This is a solid answer! You covered the core concepts well, though you could have added a few more specific examples from industry practices.",
            "score": 7,
            "confidence": "medium",
            "follow_up_required": False
        })

    def generate_follow_up(self, prompt: str) -> str:
        """Return a structured JSON follow-up question string."""
        logger.info("MockProvider: Generating follow-up")
        q = self._get_next_question()
        return json.dumps({"question_text": q})

    def generate_feedback(self, prompt: str) -> str:
        """Return a structured JSON final feedback report."""
        logger.info("MockProvider: Generating final feedback")
        return json.dumps({
            "interview_summary": "You demonstrated a strong understanding of core technical concepts.",
            "strengths": ["Clear communication", "Good foundational knowledge", "Structured answers"],
            "weaknesses": ["Provide more concrete examples", "Dive deeper into system architecture"],
            "improvement_topics": ["System Design", "Scalability"],
            "overall_score": 8,
            "recommended_learning_path": "Focus on advanced system design patterns.",
            "curriculum_references": [],
            "confidence_level": "high"
        })
