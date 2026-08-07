# NovaForge AI Interview Agent
ViCodathon 2026 – India's AI-First 48 Hour Vibe Coding Hackathon! 

An AI Interview Agent that conducts personalized technical interviews based on a candidate's learning journey.

## Hackathon
AB Talks ViCodathon 2026
**Team**: NovaForge

## Tech Stack
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: Python, FastAPI, Pydantic
- **AI**: Google Generative AI (Gemini)

---

## System Architecture

The backend is designed using a clean, modular, and decoupled architecture. The goal is to separate domain logic from the AI engine and the API delivery layer.

- **API (`backend/api/`)**: FastAPI routers exposing REST endpoints (`health`, `candidate`, `curriculum`, `interview`). Uses Dependency Injection to initialize and supply repositories and services.
- **Domain (`backend/services/domain/`)**: Pure business logic that drives the interview process without LLM dependency. Includes `SessionManager`, `DifficultyStrategy`, and `TopicSelectionStrategy`.
- **AI Layer (`backend/services/ai/`)**: Integrates LLMs securely.
  - `LLMProvider`: Abstract interface for dependency inversion.
  - `GeminiAdapter`: Concrete implementation connecting to Google Gen AI with retry policies.
  - `PromptEngine`: Houses string templates designed to force structured JSON outputs.
  - `ContextBuilder`: Serializes complex domain models (like `Candidate` and `Curriculum`) into optimized context strings for the LLM.
  - `ResponseParser`: Cleans and validates incoming LLM text into safe, predictable dictionary formats.
- **Services (`backend/services/`)**: Contains the `DataLoader` which caches the initial state and Repositories (`CandidateRepository`, `CurriculumRepository`) for in-memory reads.
- **Models (`backend/models/`)**: Pydantic models for enforcing strict data validation and typing for entities (`Candidate`, `Curriculum`, `InterviewSession`).
- **Data (`backend/data/`)**: Static JSON data stores provided by the hackathon.

---

## End-to-End Flow

1. **Start Session**: A client requests an interview for a specific Candidate ID via `POST /interview/start`. The `SessionManager` initializes a session, calculates difficulty, and plans 4 topics to cover.
2. **Next Question**: `POST /interview/{session_id}/next`. The `AIService` parses the curriculum and candidate context, then generates a highly targeted question matching the planned topic and difficulty level.
3. **Answer Question**: `POST /interview/{session_id}/answer`. The `AIService` evaluates the answer, generating a score out of 10.
4. **Follow Up (Optional)**: If the LLM determines the answer was incomplete, it flags `follow_up_required`. The backend automatically generates a follow-up question in the same cycle.
5. **Completion**: Once 8 questions are answered successfully, the session is marked as `COMPLETED`.
6. **Feedback**: `GET /interview/{session_id}/feedback` triggers the LLM to generate a comprehensive report of the candidate's performance, strengths, weaknesses, and a recommended learning path.

---

## Environment Setup

### Prerequisites
- Node.js (for Frontend)
- Python 3.9+ (for Backend)

### API Keys
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_google_gen_ai_key_here
```
> **Warning**: Never commit your real API key to version control.

### Installation
#### Backend
```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r ../requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

---

## Testing Instructions

The backend relies heavily on `pytest`. We use the `TestClient` from FastAPI to run end-to-end integration tests entirely in-memory.

To run the complete test suite:
```bash
cd backend
venv\Scripts\activate
pytest
```

The test suite includes:
- **`test_domain.py`**: Validates the core business logic, session state transitions, difficulty calculators, and topic strategies completely isolated from external dependencies.
- **`test_ai.py`**: Verifies that the PromptEngine creates correct templates and the ResponseParser cleanly handles malformed JSON outputs.
- **`test_api.py`**: End-to-end integration tests that simulate a complete 8-question interview flow, checking HTTP response codes, JSON schemas, and invalid state rejections (like attempting to answer a question that hasn't been asked).

---

## API Testing

You can use standard tools like `curl`, Postman, or the built-in Swagger UI.

1. Start the server:
```bash
cd backend
uvicorn main:app --reload
```

2. Visit the interactive Swagger Docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'backend'` when running pytest**
  Ensure you are running `pytest` with the root directory in your PYTHONPATH. The provided `pytest.ini` handles this automatically, but ensure it's in the root of the project.
- **`MissingAPIKeyException` when starting the server**
  Ensure your `.env` file is properly configured with a `GEMINI_API_KEY` and you have `python-dotenv` installed.
- **FastAPI 500 Errors during `/interview/next`**
  Check the application logs. If the Gemini API is timing out or failing due to rate limits, the `GeminiAdapter` will retry 3 times before bubbling up the exception.
- **Next.js Hydration Errors**
  If accessing the frontend over a local network, ensure your IP is whitelisted in `next.config.ts` under `allowedDevOrigins`. Browser extensions injecting scripts into the body tag may also cause hydration mismatches.
