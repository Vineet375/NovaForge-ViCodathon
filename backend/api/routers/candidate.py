from fastapi import APIRouter, HTTPException
from typing import List
from backend.api.dependencies import CandidateRepoDep
from backend.models.candidate import Candidate

router = APIRouter(prefix="/candidates", tags=["candidates"])

@router.get("", response_model=List[Candidate])
def get_all_candidates(repo: CandidateRepoDep):
    return repo.get_all_candidates()

@router.get("/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: str, repo: CandidateRepoDep):
    candidate = repo.get_candidate_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")
    return candidate
