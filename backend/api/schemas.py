from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from backend.models.interview import QuestionDifficulty, InterviewState, AskedQuestion

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: float

class StartInterviewRequest(BaseModel):
    candidate_id: str

class StartInterviewResponse(BaseModel):
    session_id: str
    candidate_id: str
    planned_difficulty: QuestionDifficulty
    current_day: Optional[int] = None

class NextQuestionResponse(BaseModel):
    question_text: str

class AnswerRequest(BaseModel):
    answer_text: str

class AnswerResponse(BaseModel):
    feedback: str
    follow_up_question: Optional[str] = None

class InterviewSessionState(BaseModel):
    session_id: str
    status: InterviewState
    current_question_number: int
    questions_asked: List[AskedQuestion]

class ActiveSessionResponse(BaseModel):
    session_id: str
    candidate_id: str
    candidate_name: str
    status: InterviewState
    current_question_number: int
    created_time: datetime
    last_updated: datetime
