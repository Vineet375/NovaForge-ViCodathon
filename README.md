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
- **Models (`backend/models/`)**: Pydantic models for enforcing strict data validation and typing for entities like `Candidate` and `Curriculum`.
- **Services (`backend/services/`)**: Contains the `DataLoader` for securely reading and parsing JSON files, and Repositories (`CandidateRepository`, `CurriculumRepository`) for exposing the data via clean methods.
- **Utils (`backend/utils/`)**: Helper modules for centralized file loading, structured logging, and constants.
- **API (`backend/api/`)**: (Future) FastAPI routers for exposing endpoints to the frontend.
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
