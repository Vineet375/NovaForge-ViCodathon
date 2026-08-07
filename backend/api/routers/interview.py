from fastapi import APIRouter, HTTPException
from backend.api.schemas import (
    StartInterviewRequest, StartInterviewResponse,
    NextQuestionResponse, AnswerRequest, AnswerResponse, InterviewSessionState
)
from backend.api.dependencies import CandidateRepoDep, CurriculumRepoDep, SessionManagerDep, AIServiceDep
from backend.models.interview import InterviewState, PlannedQuestion, QuestionCategory, AskedQuestion

router = APIRouter(prefix="/interview", tags=["interview"])

@router.post("/start", response_model=StartInterviewResponse)
def start_interview(
    request: StartInterviewRequest,
    candidate_repo: CandidateRepoDep,
    curriculum_repo: CurriculumRepoDep,
    session_manager: SessionManagerDep
):
    candidate = candidate_repo.get_candidate_by_id(request.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate {request.candidate_id} not found")
        
    curriculum = curriculum_repo.get_curriculum()
    
    session = session_manager.create_session(candidate, curriculum)
    session_manager.start_session(session.session_id)
    
    return StartInterviewResponse(
        session_id=session.session_id,
        candidate_id=session.candidate_id,
        planned_difficulty=session.difficulty_level,
        current_day=session.current_curriculum_day
    )

@router.post("/{session_id}/next", response_model=NextQuestionResponse)
def get_next_question(
    session_id: str,
    session_manager: SessionManagerDep,
    ai_service: AIServiceDep,
    candidate_repo: CandidateRepoDep,
    curriculum_repo: CurriculumRepoDep
):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    if session.status != InterviewState.IN_PROGRESS:
        raise HTTPException(status_code=400, detail=f"Session is {session.status}, cannot fetch next question")
        
    candidate = candidate_repo.get_candidate_by_id(session.candidate_id)
    curriculum = curriculum_repo.get_curriculum()
    
    planned = PlannedQuestion(
        category=QuestionCategory.TECHNICAL,
        curriculum_day=session.current_curriculum_day or 1,
        difficulty=session.difficulty_level
    )
    
    try:
        q_text = ai_service.generate_initial_question(session, candidate, curriculum, planned)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Service error: {str(e)}")
        
    asked = AskedQuestion(
        question_text=q_text,
        planned_question=planned
    )
    
    # update_progress auto completes the session after 5 questions
    session_manager.update_progress(session_id, asked)
    
    return NextQuestionResponse(question_text=asked.question_text)

@router.post("/{session_id}/answer", response_model=AnswerResponse)
def answer_question(
    session_id: str,
    request: AnswerRequest,
    session_manager: SessionManagerDep,
    ai_service: AIServiceDep
):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    if session.status != InterviewState.IN_PROGRESS:
        raise HTTPException(status_code=400, detail=f"Session is {session.status}, cannot submit answer")
        
    if not session.questions_asked:
        raise HTTPException(status_code=400, detail="No question has been asked yet")
        
    current_question = session.questions_asked[-1]
    if current_question.answer_given:
        raise HTTPException(status_code=400, detail="Question already answered")
        
    current_question.answer_given = request.answer_text
    
    try:
        feedback = ai_service.evaluate_answer(current_question, request.answer_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Service error: {str(e)}")
        
    current_question.feedback = feedback
    
    # Simple heuristic for testing without real AI
    passed = "fail" not in feedback.lower()
    
    return AnswerResponse(
        feedback=feedback,
        follow_up_question=None
    )

@router.get("/{session_id}", response_model=InterviewSessionState)
def get_session(session_id: str, session_manager: SessionManagerDep):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    return InterviewSessionState(
        session_id=session.session_id,
        status=session.status,
        current_question_number=session.current_question_number,
        questions_asked=session.questions_asked
    )
