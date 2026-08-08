from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.api.dependencies import CandidateRepoDep, CurriculumRepoDep, SessionManagerDep

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

class StatCard(BaseModel):
    title: str
    value: str
    subtitle: str

class ActivityItem(BaseModel):
    id: str
    title: str
    description: str
    time: str
    type: str  # e.g., "success", "info", "warning"

class DashboardResponse(BaseModel):
    stats: List[StatCard]
    activities: List[ActivityItem]

@router.get("", response_model=DashboardResponse)
def get_dashboard_data(
    candidate_repo: CandidateRepoDep,
    curriculum_repo: CurriculumRepoDep,
    session_manager: SessionManagerDep
):
    candidates = candidate_repo.get_all_candidates()
    curriculum = curriculum_repo.get_curriculum()
    
    total_candidates = len(candidates)
    total_modules = len(curriculum.modules)
    
    active_sessions = len(session_manager._sessions)
    completed_sessions = sum(1 for s in session_manager._sessions.values() if s.status.value == "completed")
    
    # Calculate questions answered across all sessions
    total_questions = sum(len(s.questions_asked) for s in session_manager._sessions.values())
    
    # Calculate average score across completed questions
    all_scores = [
        q.score for s in session_manager._sessions.values() 
        for q in s.questions_asked 
        if getattr(q, 'score', None) is not None
    ]
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
    
    # Generate dynamic activities based on recent sessions
    activities = []
    for s_id, session in list(session_manager._sessions.items())[-3:]:
        candidate = candidate_repo.get_candidate_by_id(session.candidate_id)
        name = candidate.member.name if candidate else "Unknown"
        
        if session.status.value == "completed":
            activities.append(ActivityItem(
                id=f"act_{s_id}_comp",
                title=f"Interview Completed: {name}",
                description=f"Answered {len(session.questions_asked)} questions.",
                time="Recently",
                type="success"
            ))
        elif session.status.value == "in_progress":
            activities.append(ActivityItem(
                id=f"act_{s_id}_prog",
                title=f"Active Interview: {name}",
                description=f"Currently on question {session.current_question_number}.",
                time="Just now",
                type="warning"
            ))

    if not activities:
        activities.append(ActivityItem(
            id="a_sys_1",
            title="System Online",
            description="Ready to start new interviews.",
            time="Just now",
            type="info"
        ))

    return DashboardResponse(
        stats=[
            StatCard(title="Registered Candidates", value=str(total_candidates), subtitle="Ready for interview"),
            StatCard(title="Curriculum Modules", value=str(total_modules), subtitle="Topics available"),
            StatCard(title="Active Sessions", value=str(active_sessions), subtitle=f"{completed_sessions} completed"),
            StatCard(title="Average Score", value=f"{avg_score:.1f}/10", subtitle=f"Across {total_questions} questions"),
        ],
        activities=activities[::-1]  # Reverse to show newest first
    )
