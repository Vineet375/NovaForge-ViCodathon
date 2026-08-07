from fastapi import APIRouter
import time
from backend.api.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])

start_time = time.time()

@router.get("", response_model=HealthResponse)
def get_health():
    uptime = time.time() - start_time
    return HealthResponse(status="ok", version="1.0.0", uptime=uptime)
