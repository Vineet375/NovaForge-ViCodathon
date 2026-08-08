from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.services.ai.exceptions import AIEngineException

app = FastAPI(
    title="NovaForge AI Interview Agent",
    description="Backend API for the NovaForge AI-powered technical interview system.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AIEngineException)
async def ai_engine_exception_handler(request: Request, exc: AIEngineException):
    """Translate all AI engine exceptions into clean JSON error responses."""
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


from backend.api.routers import health, candidate, curriculum, interview, dashboard  # noqa: E402

app.include_router(health.router)
app.include_router(candidate.router)
app.include_router(curriculum.router)
app.include_router(interview.router)
app.include_router(dashboard.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to NovaForge AI Interview Agent API"}
