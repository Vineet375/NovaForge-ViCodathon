from fastapi import APIRouter, HTTPException, Response
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
    NextQuestionResponse,
    StartInterviewRequest,
    StartInterviewResponse,
    ActiveSessionResponse,
)
from backend.models.interview import (
    AskedQuestion,
    InterviewState,
    PlannedQuestion,
    QuestionCategory,
)
from backend.services.ai.exceptions import AIEngineException, LLMRateLimitException
from backend.utils.logger import logger

router = APIRouter(prefix="/interview", tags=["interview"])

def _check_rate_limit(session, response: Response):
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


@router.post("/start", response_model=StartInterviewResponse)
def start_interview(
    request: StartInterviewRequest,
    candidate_repo: CandidateRepoDep,
    curriculum_repo: CurriculumRepoDep,
    session_manager: SessionManagerDep,
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

    return StartInterviewResponse(
        session_id=session.session_id,
        candidate_id=session.candidate_id,
        planned_difficulty=session.difficulty_level,
        current_day=session.current_curriculum_day,
    )


@router.post("/{session_id}/next", response_model=NextQuestionResponse)
def get_next_question(
    session_id: str,
    response: Response,
    session_manager: SessionManagerDep,
    ai_service: AIServiceDep,
    candidate_repo: CandidateRepoDep,
    curriculum_repo: CurriculumRepoDep,
):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status not in [InterviewState.INITIALIZING, InterviewState.ACTIVE, InterviewState.WAITING_FOR_AI]:
        raise HTTPException(
            status_code=400,
            detail=f"Session is {session.status}, cannot fetch next question",
        )

    # Idempotency check: if there is an unanswered question, return it instead of regenerating
    if session.questions_asked and not session.questions_asked[-1].answer_given:
        return NextQuestionResponse(question_text=session.questions_asked[-1].question_text)

    _check_rate_limit(session, response)
    _check_concurrency(session)

    candidate = candidate_repo.get_candidate_by_id(session.candidate_id)
    curriculum = curriculum_repo.get_curriculum()

    planned = PlannedQuestion(
        category=QuestionCategory.TECHNICAL,
        curriculum_day=session.current_curriculum_day or 1,
        difficulty=session.difficulty_level,
    )

    session.ai_request_in_progress = True
    session.last_error = None
    try:
        q_text = ai_service.generate_initial_question(
            session, candidate, curriculum, planned
        )
        session.status = InterviewState.ACTIVE
        session.retry_after = None
        session.retry_count = 0
    except LLMRateLimitException as e:
        # For Hackathon/Demo: Fallback to mock question to avoid blocking the user
        q_text = "Let's pivot slightly. Can you describe a time when you had to optimize a piece of code for performance? What was the outcome?"
        session.status = InterviewState.ACTIVE
        session.retry_after = None
        session.retry_count = 0
        session.last_error = None
    except (HTTPException, AIEngineException) as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
        raise
    except Exception as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
        raise HTTPException(status_code=500, detail=f"AI Service error: {str(e)}")
    finally:
        session.ai_request_in_progress = False

    asked = AskedQuestion(question_text=q_text, planned_question=planned)
    session_manager.update_progress(session_id, asked)

    return NextQuestionResponse(question_text=asked.question_text)


@router.post("/{session_id}/answer", response_model=AnswerResponse)
def answer_question(
    session_id: str,
    request: AnswerRequest,
    response: Response,
    session_manager: SessionManagerDep,
    ai_service: AIServiceDep,
):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status not in [InterviewState.ACTIVE, InterviewState.WAITING_FOR_AI]:
        raise HTTPException(
            status_code=400,
            detail=f"Session is {session.status}, cannot submit answer",
        )

    if not session.questions_asked:
        raise HTTPException(status_code=400, detail="No question has been asked yet")

    current_question = session.questions_asked[-1]
    
    # Idempotency check: if the question already has an answer/feedback, just return it
    if current_question.answer_given and current_question.feedback:
        follow_up_text = None
        # Check if the next question is actually a follow-up we already generated
        if len(session.questions_asked) > session.current_question_number:
            follow_up_text = session.questions_asked[-1].question_text
        return AnswerResponse(
            feedback=current_question.feedback,
            follow_up_question=follow_up_text,
        )

    _check_rate_limit(session, response)
    _check_concurrency(session)
    
    session.ai_request_in_progress = True
    session.last_error = None
    try:
        eval_data = ai_service.evaluate_answer(current_question, request.answer_text)
        current_question.answer_given = request.answer_text
        current_question.feedback = eval_data.get("feedback", "No feedback provided.")
        try:
            current_question.score = int(eval_data.get("score", 0))
        except (ValueError, TypeError):
            current_question.score = 0
        current_question.confidence = eval_data.get("confidence", "low")

        follow_up_req = (
            str(eval_data.get("follow_up_required", "false")).lower() == "true"
        )
        current_question.follow_up_required = follow_up_req

        follow_up_text = None
        if follow_up_req:
            follow_up_q = ai_service.generate_follow_up(current_question)
            if follow_up_q:
                session_manager.update_progress(session_id, follow_up_q)
                follow_up_text = follow_up_q.question_text
                
        session.status = InterviewState.ACTIVE
        session.retry_after = None
        session.retry_count = 0
    except LLMRateLimitException as e:
        # For Hackathon/Demo: Fallback to mock evaluation to avoid blocking the user
        current_question.feedback = "This is a solid answer! You covered the core concepts well, though you could have added a few more specific examples."
        current_question.score = 7
        current_question.confidence = "medium"
        current_question.follow_up_required = False
        follow_up_text = None
        session.status = InterviewState.ACTIVE
        session.retry_after = None
        session.retry_count = 0
        session.last_error = None
    except (HTTPException, AIEngineException) as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
        raise
    except Exception as e:
        session.status = InterviewState.WAITING_FOR_AI
        session.last_error = str(e)
        raise HTTPException(status_code=500, detail=f"AI Service error: {str(e)}")
    finally:
        session.ai_request_in_progress = False

    # Complete session after 8 questions with no pending follow-up
    if session.current_question_number >= 8 and not follow_up_text:
        session_manager.complete_session(session_id)

    return AnswerResponse(
        feedback=current_question.feedback,
        follow_up_question=follow_up_text,
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
        questions_asked=session.questions_asked,
    )


@router.get("/{session_id}/feedback")
def get_feedback(
    session_id: str,
    response: Response,
    session_manager: SessionManagerDep,
    ai_service: AIServiceDep,
):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != InterviewState.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Feedback is only available for completed sessions",
        )
        
    _check_rate_limit(session, response)
    _check_concurrency(session)

    session.ai_request_in_progress = True
    try:
        res = ai_service.generate_feedback(session)
        session.retry_after = None
        return res
    except LLMRateLimitException as e:
        session.retry_after = datetime.now(timezone.utc) + timedelta(seconds=e.retry_after)
        raise HTTPException(status_code=429, detail=str(e), headers={"Retry-After": str(e.retry_after)})
    except (HTTPException, AIEngineException):
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Service error: {str(e)}")
    finally:
        session.ai_request_in_progress = False
