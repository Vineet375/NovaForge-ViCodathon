# NovaForge AI Interview Agent
ViCodathon 2026 – India's AI-First 48 Hour Vibe Coding Hackathon! 

An AI Interview Agent that conducts personalized technical interviews based on a candidate's learning journey.

## Hackathon
AB Talks ViCodathon 2026
**Team**: NovaForge

## Tech Stack
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: Python, FastAPI, Pydantic

## Project Structure
- `frontend/`: Next.js application
- `backend/`: FastAPI backend
- `docs/`: Technical specifications and documentation

## Backend Architecture
The backend is designed using a clean, modular architecture:
- **Models (`backend/models/`)**: Pydantic models for enforcing strict data validation and typing for entities like `Candidate` and `Curriculum`, as well as `InterviewSession` and domain logic states.
- **Services (`backend/services/`)**: Contains the `DataLoader` and Repositories (`CandidateRepository`, `CurriculumRepository`).
- **Domain (`backend/services/domain/`)**: Pure business logic (e.g., `SessionManager`, `DifficultyStrategy`, `TopicSelectionStrategy`) that drives the interview process without LLM dependency.
- **AI Layer (`backend/services/ai/`)**: Integrates LLMs via an abstraction layer (`LLMProvider`). Includes the `PromptEngine` for templating, `ContextBuilder` for stringifying domain models, and `ResponseParser` for cleaning outputs.
- **Utils (`backend/utils/`)**: Helper modules for centralized file loading, structured logging, and constants.
- **API (`backend/api/`)**: FastAPI routers (`health`, `candidate`, `curriculum`, `interview`) exposing REST endpoints with Dependency Injection for scaling.
- **Data (`backend/data/`)**: Static JSON data stores.

## Installation

### Prerequisites
- Node.js
- Python 3.9+

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r ../requirements.txt
uvicorn main:app --reload
```
