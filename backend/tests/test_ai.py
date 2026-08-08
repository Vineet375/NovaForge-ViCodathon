from unittest.mock import patch
import pytest

from backend.models.candidate import Candidate, Member, Signals
from backend.models.curriculum import Curriculum, Day
from backend.models.interview import InterviewSession
from backend.services.ai.context_builder import ContextBuilder
from backend.services.ai.exceptions import MissingAPIKeyException, ParserRecoveryFailedException
from backend.services.ai.gemini_adapter import GeminiAdapter
from backend.services.ai.prompt_engine import PromptEngine
from backend.services.ai.response_parser import ResponseParser


@pytest.fixture
def sample_candidate():
    return Candidate(
        member=Member(
            id="c1",
            name="Test User",
            jobRole="Dev",
            yearsExperience=2,
            education="BSc",
            status="COMPLETED",
        ),
        missions=[],
        signals=Signals(commitDays=10, missionsCompleted=1, missionsFirstTry=1),
    )


@pytest.fixture
def sample_curriculum():
    return Curriculum(
        cohort="V1",
        modules=[],
        days=[
            Day(
                day=1,
                title="Python Basics",
                type="BUILD",
                tools=[],
                objectives=["Learn lists", "Learn dicts"],
            )
        ],
    )


@pytest.fixture
def sample_session():
    return InterviewSession(
        session_id="test-session",
        candidate_id="c1",
        current_curriculum_day=1,
    )


def test_prompt_engine():
    prompt = PromptEngine.build_interview_prompt("ctx_candidate", "topic_x", "HARD")
    assert "topic_x" in prompt
    assert "HARD" in prompt
    assert "ctx_candidate" in prompt
    assert "specifically to the candidate's exact role" in prompt
    assert "ONLY a single valid JSON object" in prompt


def test_context_builder(sample_candidate, sample_curriculum, sample_session):
    context = ContextBuilder.build_full_context(
        sample_session, sample_candidate, sample_curriculum
    )
    assert "Test User" in context
    assert "Python Basics" in context


def test_response_parser_clean():
    raw = '```json\n{"question_text": "What is Python?"}\n```'
    parsed = ResponseParser.parse_question(raw)
    assert parsed == "What is Python?"


def test_response_parser_empty():
    with pytest.raises(ParserRecoveryFailedException):
        ResponseParser.parse_question("   ")


def test_response_parser_malformed_with_recovery():
    # Test step 3: Extract first balanced JSON object ignoring leading/trailing filler
    raw = '''
Here is the question you asked for:
```json
{
  "question_text": "How does React work?"
}
```
Good luck!
'''
    parsed = ResponseParser.parse_question(raw)
    assert parsed == "How does React work?"

    
def test_response_parser_schema_validation():
    # Missing 'feedback' key
    raw = '{"score": 8, "follow_up_required": false, "confidence": "high"}'
    with pytest.raises(ParserRecoveryFailedException):
        ResponseParser.parse_full_evaluation(raw)


def test_mock_provider_unique():
    from backend.services.ai.providers.mock import MockProvider
    provider = MockProvider()
    q1 = provider.generate_question("p")
    q2 = provider.generate_question("Candidate Answer: p")
    assert q1 != q2

def test_deduplication_logic(sample_candidate, sample_curriculum, sample_session):
    from backend.services.ai.ai_service import AIService
    from backend.services.ai.engine import AIEngine
    from backend.models.interview import AskedQuestion, PlannedQuestion, QuestionCategory, QuestionDifficulty
    
    mock_engine = AIEngine(test_mode=True)
    service = AIService(mock_engine)
    
    # Pre-populate session with a question
    planned = PlannedQuestion(
        category=QuestionCategory.TECHNICAL,
        curriculum_day=1,
        difficulty=QuestionDifficulty.MEDIUM,
    )
    sample_session.questions_asked.append(
        AskedQuestion(question_text="What is Python?", planned_question=planned)
    )
    
    # Mock _generate_with_retry to return a duplicate first, then a unique one
    responses = ["What is Python?", "What are decorators in Python?"]
    
    def mock_generate(*args, **kwargs):
        return responses.pop(0)
        
    with patch.object(service, '_generate_with_retry', side_effect=mock_generate):
        q_text = service.generate_initial_question(sample_session, sample_candidate, sample_curriculum, planned)
        assert q_text == "What are decorators in Python?"
        
    # Verify similarity check catches punctuation/case differences
    sample_session.questions_asked.clear()
    sample_session.questions_asked.append(
        AskedQuestion(question_text="How does the Event Loop work in Node.js and why is it important for asynchronous programming?", planned_question=planned)
    )
    responses_sim = [
        "How does the event loop work in node js, and why is it important for asynchronous programming?", 
        "Explain promises in JS"
    ]
    def mock_generate_sim(*args, **kwargs):
        return responses_sim.pop(0)
        
    with patch.object(service, '_generate_with_retry', side_effect=mock_generate_sim):
        q_text = service.generate_initial_question(sample_session, sample_candidate, sample_curriculum, planned)
        assert q_text == "Explain promises in JS"
