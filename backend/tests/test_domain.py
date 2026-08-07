import pytest
from backend.models.candidate import Candidate, Member, Mission, Signals
from backend.models.curriculum import Curriculum, Module, Day
from backend.models.interview import QuestionDifficulty, InterviewState, AskedQuestion, PlannedQuestion, QuestionCategory
from backend.services.domain.strategies import DifficultyStrategy, TopicSelectionStrategy
from backend.services.domain.session_manager import SessionManager

@pytest.fixture
def sample_candidate():
    return Candidate(
        member=Member(id="c1", name="Test", jobRole="Dev", yearsExperience=2, education="BSc", status="COMPLETED"),
        missions=[
            Mission(day=1, title="M1", passed=True, attempts=1),
            Mission(day=2, title="M2", passed=False, attempts=2, skipped=True)
        ],
        signals=Signals(commitDays=10, missionsCompleted=1, missionsFirstTry=1)
    )

@pytest.fixture
def sample_curriculum():
    return Curriculum(
        cohort="V1",
        modules=[],
        days=[
            Day(day=1, title="D1", type="BUILD", tools=[], objectives=[]),
            Day(day=2, title="D2", type="BUILD", tools=[], objectives=[]),
            Day(day=3, title="D3", type="BUILD", tools=[], objectives=[]),
            Day(day=4, title="D4", type="BUILD", tools=[], objectives=[]),
            Day(day=5, title="D5", type="BUILD", tools=[], objectives=[])
        ]
    )

def test_difficulty_strategy(sample_candidate):
    diff = DifficultyStrategy.calculate_difficulty(sample_candidate)
    assert diff == QuestionDifficulty.MEDIUM
    
def test_topic_selection(sample_candidate, sample_curriculum):
    topics = TopicSelectionStrategy.select_topics(sample_candidate, sample_curriculum, num_days=4)
    assert len(topics) == 4
    assert 1 in topics
    
def test_session_manager(sample_candidate, sample_curriculum):
    manager = SessionManager()
    session = manager.create_session(sample_candidate, sample_curriculum)
    
    assert session.status == InterviewState.NOT_STARTED
    assert session.candidate_id == "c1"
    
    started = manager.start_session(session.session_id)
    assert started
    assert session.status == InterviewState.IN_PROGRESS
    
    # Progress
    q = AskedQuestion(
        question_text="Q1",
        planned_question=PlannedQuestion(category=QuestionCategory.TECHNICAL, curriculum_day=1, difficulty=QuestionDifficulty.MEDIUM)
    )
    manager.update_progress(session.session_id, q)
    assert session.current_question_number == 1
    
    for i in range(7):
        manager.update_progress(session.session_id, q)
        
    assert session.current_question_number == 8
    
    # Complete manually as router handles this now
    manager.complete_session(session.session_id)
    assert session.status == InterviewState.COMPLETED
