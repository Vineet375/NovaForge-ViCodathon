import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends

from backend.services.ai.ai_service import AIService
from backend.services.ai.gemini_adapter import GeminiAdapter
from backend.services.domain.session_manager import SessionManager
from backend.services.repositories import CandidateRepository, CurriculumRepository

load_dotenv()

# Global singletons – one instance per server process
_curriculum_repo = CurriculumRepository()
_candidate_repo = CandidateRepository()
_session_manager = SessionManager()
_llm_provider = GeminiAdapter()
_ai_service = AIService(_llm_provider)


def get_curriculum_repo() -> CurriculumRepository:
    return _curriculum_repo


def get_candidate_repo() -> CandidateRepository:
    return _candidate_repo


def get_session_manager() -> SessionManager:
    return _session_manager


def get_ai_service() -> AIService:
    return _ai_service


# FastAPI dependency type aliases for route handlers
CurriculumRepoDep = Annotated[CurriculumRepository, Depends(get_curriculum_repo)]
CandidateRepoDep = Annotated[CandidateRepository, Depends(get_candidate_repo)]
SessionManagerDep = Annotated[SessionManager, Depends(get_session_manager)]
AIServiceDep = Annotated[AIService, Depends(get_ai_service)]
