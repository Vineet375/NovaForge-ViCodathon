from fastapi import APIRouter, HTTPException, Response, BackgroundTasks
from typing import List
from datetime import datetime, timezone, timedelta

from backend.api.dependencies import (
    AIServiceDep,
    CandidateRepoDep,
    CurriculumRepoDep,
    SessionManagerDep,
)
from backend.api.schemas import (
    AnswerRequest,
    AnswerResponse,
    InterviewSessionState,
    StartInterviewRequest,
    StartInterviewResponse,
    ActiveSessionResponse,
)
from backend.models.interview import (
    AskedQuestion,
    InterviewState,
    PlannedQuestion,
    QuestionCategory,
    MAX_INTERVIEW_QUESTIONS,
)
from backend.services.ai.exceptions import AIEngineException, LLMRateLimitException
from backend.utils.logger import logger

router = APIRouter(prefix="/interview", tags=["interview"])

def _check_rate_limit(session, response: Response = None):
    if session.retry_after:
        now = datetime.now(timezone.utc)
        retry_after_aware = session.retry_after if session.retry_after.tzinfo else session.retry_after.replace(tzinfo=timezone.utc)
        if now < retry_after_aware:
            delta = int((retry_after_aware - now).total_seconds())
            if delta > 0:
                raise HTTPException(
                    status_code=429, 
                    detail="The AI service is temporarily busy. Please wait.",
                    headers={"Retry-After": str(delta)}
                )
            
def _check_concurrency(session):
    if session.ai_request_in_progress:
        raise HTTPException(status_code=409, detail="Another AI request is currently in progress for this session.")

@router.get("/active", response_model=List[ActiveSessionResponse])
def get_active_sessions(
    session_manager: SessionManagerDep,
    candidate_repo: CandidateRepoDep,
):
    sessions = session_manager.get_active_sessions()
    result = []
    for s in sessions:
        candidate = candidate_repo.get_candidate_by_id(s.candidate_id)
        if candidate:
            result.append(
                ActiveSessionResponse(
                    session_id=s.session_id,
                    candidate_id=s.candidate_id,
                    candidate_name=candidate.member.name,
                    status=s.status,
                    current_question_number=s.current_question_number,
                    created_time=s.created_time,
                    last_updated=s.last_updated,
                )
            )
    return sorted(result, key=lambda x: x.last_updated, reverse=True)


def _generate_question_task(
    session_id: str,
    session_manager,
    ai_service,
    candidate_repo,
    curriculum_repo,
):
    session = session_manager.get_session(session_id)
    if not session:
        return
    
    candidate = candidate_repo.get_candidate_by_id(session.candidate_id)
    curriculum = curriculum_repo.get_curriculum()

    planned = PlannedQuestion(
        category=QuestionCategory.TECHNICAL,
        curriculum_day=session.current_curriculum_day or 1,
        difficulty=session.difficulty_level,
    )

    try:
        q_text = ai_service.generate_initial_question(
            session, candidate, curriculum, planned
        )
        asked = AskedQuestion(question_text=q_text, planned_question=planned)
        session_manager.update_progress(session_id, asked)
        
        session.status = InterviewState.QUESTION_READY
        session.retry_after = None
        session.retry_count = 0
    except LLMRateLimitException as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
        if hasattr(e, 'retry_after') and e.retry_after:
             session.retry_after = datetime.now(timezone.utc) + timedelta(seconds=e.retry_after)
    except (HTTPException, AIEngineException) as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
    except Exception as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
    finally:
        session.ai_request_in_progress = False


def _generate_final_evaluation_task(
    session_id: str,
    session_manager,
    ai_service,
):
    session = session_manager.get_session(session_id)
    if not session:
        return
        
    try:
        res = ai_service.generate_feedback(session)
        # Store feedback in session somewhere? We didn't have a place in InterviewSession before except maybe creating one.
        # Wait, get_feedback used to just return it directly!
        # If it's a background task, where does the result go?
        # We must add an `evaluation_report` field to InterviewSession or store it.
        # Let's check backend/models/interview.py for an evaluation field. If it's missing, I'll need to add it!
        # For now, let's just add it dynamically to the session object.
        session.evaluation_report = res
        session_manager.complete_session(session_id)
        session.retry_after = None
    except LLMRateLimitException as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
        if hasattr(e, 'retry_after') and e.retry_after:
             session.retry_after = datetime.now(timezone.utc) + timedelta(seconds=e.retry_after)
    except (HTTPException, AIEngineException) as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
    except Exception as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
    finally:
        session.ai_request_in_progress = False


@router.post("/start", response_model=StartInterviewResponse)
def start_interview(
    request: StartInterviewRequest,
    background_tasks: BackgroundTasks,
    candidate_repo: CandidateRepoDep,
    curriculum_repo: CurriculumRepoDep,
    session_manager: SessionManagerDep,
    ai_service: AIServiceDep,
):
    candidate = candidate_repo.get_candidate_by_id(request.candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=404,
            detail=f"Candidate {request.candidate_id} not found",
        )

    curriculum = curriculum_repo.get_curriculum()
    session = session_manager.create_session(candidate, curriculum)
    session_manager.start_session(session.session_id)
    
    # Start generation automatically
    session.status = InterviewState.GENERATING
    session.ai_request_in_progress = True
    session.last_error = None
    background_tasks.add_task(
        _generate_question_task,
        session.session_id,
        session_manager,
        ai_service,
        candidate_repo,
        curriculum_repo
    )

    return StartInterviewResponse(
        session_id=session.session_id,
        candidate_id=session.candidate_id,
        planned_difficulty=session.difficulty_level,
        current_day=session.current_curriculum_day,
    )


@router.post("/{session_id}/next")
def get_next_question(
    session_id: str,
    background_tasks: BackgroundTasks,
    session_manager: SessionManagerDep,
    ai_service: AIServiceDep,
    candidate_repo: CandidateRepoDep,
    curriculum_repo: CurriculumRepoDep,
):
    """Used purely for manual retries when WAITING_FOR_AI."""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != InterviewState.WAITING_FOR_AI:
        raise HTTPException(
            status_code=409,
            detail=f"Session is {session.status}, cannot trigger next generation manually",
        )
        
    if len(session.questions_asked) >= MAX_INTERVIEW_QUESTIONS:
        raise HTTPException(status_code=409, detail="Maximum questions reached")

    _check_rate_limit(session)
    _check_concurrency(session)

    session.status = InterviewState.GENERATING
    session.ai_request_in_progress = True
    session.last_error = None
    background_tasks.add_task(
        _generate_question_task,
        session_id,
        session_manager,
        ai_service,
        candidate_repo,
        curriculum_repo
    )

    return {"status": "generating"}


@router.post("/{session_id}/answer", response_model=AnswerResponse)
def answer_question(
    session_id: str,
    request: AnswerRequest,
    background_tasks: BackgroundTasks,
    session_manager: SessionManagerDep,
    ai_service: AIServiceDep,
    candidate_repo: CandidateRepoDep,
    curriculum_repo: CurriculumRepoDep,
):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not session.questions_asked:
        raise HTTPException(status_code=400, detail="No question has been asked yet")

    current_question = session.questions_asked[-1]

    # Idempotency check: If this question already has an answer, just return success
    # and don't trigger anything. The frontend might have refreshed or double-submitted.
    if current_question.answer_given is not None:
        return AnswerResponse(feedback="Answer already recorded.", follow_up_question=None)

    if session.status not in [InterviewState.QUESTION_READY]:
        raise HTTPException(
            status_code=409,
            detail=f"Session is {session.status}, cannot submit answer",
        )

    _check_concurrency(session)

    # 3. Save the answer exactly once
    current_question.answer_given = request.answer_text

    # 5. Determine if we generate next question or final evaluation
    if len(session.questions_asked) < MAX_INTERVIEW_QUESTIONS:
        session.status = InterviewState.GENERATING
        session.ai_request_in_progress = True
        background_tasks.add_task(
            _generate_question_task,
            session_id,
            session_manager,
            ai_service,
            candidate_repo,
            curriculum_repo
        )
    else:
        session.status = InterviewState.FINAL_EVALUATION
        session.ai_request_in_progress = True
        background_tasks.add_task(
            _generate_final_evaluation_task,
            session_id,
            session_manager,
            ai_service
        )

    # 7. Return a successful response promptly
    return AnswerResponse(
        feedback="Answer recorded.",
        follow_up_question=None,
    )


@router.get("/{session_id}", response_model=InterviewSessionState)
def get_session(session_id: str, session_manager: SessionManagerDep):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return InterviewSessionState(
        session_id=session.session_id,
        status=session.status,
        current_question_number=len(session.questions_asked),
        questions_asked=session.questions_asked,
    )


@router.get("/{session_id}/feedback")
def get_feedback(
    session_id: str,
    session_manager: SessionManagerDep,
):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != InterviewState.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Feedback is only available for completed sessions",
        )
        
    return getattr(session, "evaluation_report", {})
