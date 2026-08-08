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

    def _get_next_question(self, index: int = 0) -> str:
        return self.QUESTIONS[index % len(self.QUESTIONS)]

    def generate_question(self, prompt: str) -> str:
        """Return a structured JSON question string."""
        logger.info("MockProvider: Generating question")
        
        # We'll extract index if we can, but since prompt is just a string, we might just return random or track externally.
        # Actually, if we want deterministic questions, we can rely on the caller sending the index or we keep a state.
        # Since we can't reliably parse index from prompt easily without breaking other providers, 
        # let's just use random for mock if we want it to be stateless, or parse it if we inject it.
        # The prompt might contain the history. Let's just pick a random one for mock that we haven't picked yet,
        # or since it's a mock, just return a fixed string. 
        # Wait, the instructions say: "Use deterministic indexing based on: len(session.questions_asked)"
        # We don't have session inside generate_question (it takes prompt: str). 
        # Let's extract the number of previous questions from the prompt history if possible.
        count = prompt.count("Candidate Answer:")
        q = self._get_next_question(count)
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
