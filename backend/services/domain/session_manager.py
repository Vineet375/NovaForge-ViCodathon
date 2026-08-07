import uuid
from datetime import datetime, timezone
from typing import Dict, Optional
from backend.models.interview import InterviewSession, InterviewState, AskedQuestion
from backend.models.candidate import Candidate
from backend.models.curriculum import Curriculum
from backend.services.domain.strategies import DifficultyStrategy, TopicSelectionStrategy
from backend.utils.logger import logger

class SessionManager:
    """Manages the lifecycle of interview sessions in memory."""
    
    def __init__(self):
        self._sessions: Dict[str, InterviewSession] = {}
        
    def create_session(self, candidate: Candidate, curriculum: Curriculum) -> InterviewSession:
        """Initialize a new interview session for a candidate."""
        
        # Check for active session
        for session in self._sessions.values():
            if session.candidate_id == candidate.member.id and session.status in [InterviewState.NOT_STARTED, InterviewState.IN_PROGRESS]:
                logger.info(f"Returning existing active session for candidate {candidate.member.id}")
                return session
                
        session_id = str(uuid.uuid4())
        
        # Determine starting difficulty
        difficulty = DifficultyStrategy.calculate_difficulty(candidate)
        
        # Determine topics to cover
        topics = TopicSelectionStrategy.select_topics(candidate, curriculum)
        
        # Default start to the first selected topic if available
        start_day = topics[0] if topics else None
        
        session = InterviewSession(
            session_id=session_id,
            candidate_id=candidate.member.id,
            status=InterviewState.NOT_STARTED,
            difficulty_level=difficulty,
            planned_topics=topics,
            current_curriculum_day=start_day
        )
        
        self._sessions[session_id] = session
        logger.info(f"Created new interview session {session_id} for candidate {candidate.member.id}")
        return session
        
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """Retrieve an existing session."""
        return self._sessions.get(session_id)
        
    def start_session(self, session_id: str) -> bool:
        """Mark a session as in progress."""
        session = self.get_session(session_id)
        if session and session.status == InterviewState.NOT_STARTED:
            session.status = InterviewState.IN_PROGRESS
            session.start_time = datetime.now(timezone.utc)
            return True
        return False
        
    def update_progress(self, session_id: str, asked_question: AskedQuestion) -> Optional[InterviewSession]:
        """Update session progress with a new question and detect completion."""
        session = self.get_session(session_id)
        if not session or session.status != InterviewState.IN_PROGRESS:
            return None
            
        session.questions_asked.append(asked_question)
        session.current_question_number += 1
        
        # Advance topic
        if session.planned_topics:
            idx = session.current_question_number % len(session.planned_topics)
            session.current_curriculum_day = session.planned_topics[idx]
        
        # Heuristic completion logic: if they've answered 8 questions
        if session.current_question_number >= 8:
            self.complete_session(session_id)
            
        return session
        
    def complete_session(self, session_id: str) -> bool:
        """Mark a session as completed."""
        session = self.get_session(session_id)
        if session and session.status == InterviewState.IN_PROGRESS:
            session.status = InterviewState.COMPLETED
            session.end_time = datetime.now(timezone.utc)
            logger.info(f"Interview session {session_id} completed.")
            return True
        return False
