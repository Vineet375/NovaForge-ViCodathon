from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class InterviewState(str, Enum):
    INITIALIZING = "initializing"
    GENERATING = "generating"
    QUESTION_READY = "question_ready"
    FINAL_EVALUATION = "final_evaluation"
    WAITING_FOR_AI = "waiting_for_ai"
    COMPLETED = "completed"
    FAILED = "failed"

MAX_INTERVIEW_QUESTIONS = 4

class QuestionDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionCategory(str, Enum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    CONCEPTUAL = "conceptual"
    PRACTICAL = "practical"

class PlannedQuestion(BaseModel):
    category: QuestionCategory
    curriculum_day: int
    difficulty: QuestionDifficulty
    follow_up_eligible: bool = True

class AskedQuestion(BaseModel):
    question_text: str
    planned_question: PlannedQuestion
    answer_given: Optional[str] = None
    feedback: Optional[str] = None
    score: Optional[int] = None
    follow_up_required: bool = False
    confidence: Optional[str] = None

class InterviewSession(BaseModel):
    session_id: str
    candidate_id: str
    status: InterviewState = InterviewState.INITIALIZING
    current_question_number: int = 0
    planned_topics: List[int] = Field(default_factory=list)
    current_curriculum_day: Optional[int] = None
    current_topic: Optional[str] = None
    difficulty_level: QuestionDifficulty = QuestionDifficulty.MEDIUM
    questions_asked: List[AskedQuestion] = Field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Milestone 16 Diagnostics & Resilience
    created_time: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    last_error: Optional[str] = None
    retry_after: Optional[datetime] = None
    retry_count: int = 0
    evaluation_report: Optional[dict] = None
    ai_request_in_progress: bool = False
