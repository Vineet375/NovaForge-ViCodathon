from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="NovaForge AI Interview Agent",
    description="Backend API for NovaForge AI Interview Agent",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.api.routers import health, candidate, curriculum, interview, dashboard

app.include_router(health.router)
app.include_router(candidate.router)
app.include_router(curriculum.router)
app.include_router(interview.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to NovaForge AI Interview Agent API"}
