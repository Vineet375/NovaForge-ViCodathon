from fastapi import APIRouter, HTTPException
from backend.api.dependencies import CurriculumRepoDep
from backend.models.curriculum import Curriculum, Day

router = APIRouter(prefix="/curriculum", tags=["curriculum"])

@router.get("", response_model=Curriculum)
def get_curriculum(repo: CurriculumRepoDep):
    return repo.get_curriculum()

@router.get("/day/{day_num}", response_model=Day)
def get_day(day_num: int, repo: CurriculumRepoDep):
    day = repo.get_day(day_num)
    if not day:
        raise HTTPException(status_code=404, detail=f"Curriculum day {day_num} not found")
    return day
