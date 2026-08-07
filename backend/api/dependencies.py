from typing import Annotated
from fastapi import Depends
from backend.services.repositories import CurriculumRepository, CandidateRepository
from backend.services.domain.session_manager import SessionManager
from backend.services.ai.ai_service import AIService
from backend.services.ai.gemini_adapter import GeminiAdapter

# Global instances for dependency injection
_curriculum_repo = CurriculumRepository()
_candidate_repo = CandidateRepository()
_session_manager = SessionManager()

import os
from dotenv import load_dotenv

load_dotenv()
# For this milestone, we use the GeminiAdapter which is mocked out internally to not make real calls
if not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "mock_key_for_milestone_5"
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

# Type aliases for dependency injection in route handlers
CurriculumRepoDep = Annotated[CurriculumRepository, Depends(get_curriculum_repo)]
CandidateRepoDep = Annotated[CandidateRepository, Depends(get_candidate_repo)]
SessionManagerDep = Annotated[SessionManager, Depends(get_session_manager)]
AIServiceDep = Annotated[AIService, Depends(get_ai_service)]
