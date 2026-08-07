from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class InterviewState(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

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

class InterviewSession(BaseModel):
    session_id: str
    candidate_id: str
    status: InterviewState = InterviewState.NOT_STARTED
    current_question_number: int = 0
    current_curriculum_day: Optional[int] = None
    current_topic: Optional[str] = None
    difficulty_level: QuestionDifficulty = QuestionDifficulty.MEDIUM
    questions_asked: List[AskedQuestion] = Field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
