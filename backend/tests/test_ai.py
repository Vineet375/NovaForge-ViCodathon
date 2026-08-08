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
    prompt = PromptEngine.build_interview_prompt("ctx", "topic_x", "HARD")
    assert "topic_x" in prompt
    assert "HARD" in prompt
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


def test_gemini_adapter_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(MissingAPIKeyException):
        GeminiAdapter()


def test_gemini_adapter_mock_response(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")
    adapter = GeminiAdapter()
    with patch.object(adapter, "_call_gemini", return_value='{"question_text": "MOCK"}'):
        res = adapter.generate_question("test prompt")
        assert "MOCK" in res
