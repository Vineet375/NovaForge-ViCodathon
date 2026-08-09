import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.services.ai.exceptions import AIEngineException

app = FastAPI(
    title="NovaForge AI Interview Agent",
    description="Backend API for the NovaForge AI-powered technical interview system.",
    version="1.0.0"
)

# Comma-separated browser origins allowed to call this API. Keep local origins
# available by default so the existing development workflow continues to work.
DEFAULT_CORS_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"
cors_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv("FRONTEND_ORIGINS", DEFAULT_CORS_ORIGINS).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Retry-After"],
)


@app.exception_handler(AIEngineException)
async def ai_engine_exception_handler(request: Request, exc: AIEngineException):
    """Translate all AI engine exceptions into clean JSON error responses."""
    from backend.services.ai.exceptions import (
        ParserRecoveryFailedException,
        LLMRateLimitException,
        LLMAuthException,
    )
    
    if isinstance(exc, LLMRateLimitException):
        return JSONResponse(
            status_code=429,
            content={"detail": str(exc)},
            headers={"Retry-After": str(exc.retry_after)},
        )
        
    if isinstance(exc, LLMAuthException):
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
        )

    detail = str(exc)
    if isinstance(exc, ParserRecoveryFailedException):
        detail = "The AI returned an unexpected response format. Please try again."
    elif isinstance(exc, AIEngineException):
        detail = "The AI is temporarily unavailable. Please try again."
        
    return JSONResponse(
        status_code=500,
        content={"detail": detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch any unhandled exception to prevent stack trace leakage in production."""
    # We could log exc here for internal tracking
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong. Please try again."},
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
