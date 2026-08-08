# NovaForge AI Interview Agent

> **ViCodathon 2026** — India's AI-First 48-Hour Vibe Coding Hackathon

A production-grade AI-powered technical interview system that conducts personalized, context-aware interviews based on a candidate's learning journey through the curriculum.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Features](#features)
4. [Architecture Overview](#architecture-overview)
5. [Technology Stack](#technology-stack)
6. [Folder Structure](#folder-structure)
7. [AI Workflow](#ai-workflow)
8. [Backend Architecture](#backend-architecture)
9. [Frontend Architecture](#frontend-architecture)
10. [API Reference](#api-reference)
11. [Environment Variables](#environment-variables)
12. [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Backend Setup](#2-backend-setup)
    - [3. Frontend Setup](#3-frontend-setup)
13. [Running the Application](#running-the-application)
    - [Run Backend](#run-backend)
    - [Run Frontend](#run-frontend)
14. [Running Tests](#running-tests)
15. [Gemini API Configuration](#gemini-api-configuration)
16. [Common Troubleshooting](#common-troubleshooting)
17. [Deployment Notes](#deployment-notes)
18. [Known Limitations](#known-limitations)
19. [Future Improvements](#future-improvements)
20. [Authors](#authors)
21. [License](#license)

---

## Project Overview

**NovaForge** is an AI interview agent built for the ViCodathon 2026 hackathon. It analyzes a candidate's curriculum progress, learning signals (missions completed, commit days, first-try success rate), and experience profile to dynamically generate 4 personalized technical questions at the appropriate difficulty level.

Unlike generic interview tools, NovaForge understands *what the candidate has studied* and tailors every question to their specific curriculum journey — from RAG pipelines and vector databases to full-stack React/FastAPI application development.

---

## Problem Statement

Traditional technical screenings are generic. They don't account for:

- **What the candidate has actually learned** during their training program
- **Their demonstrated performance** (missions passed, skipped, retried)
- **The difficulty level appropriate** for their seniority and track record

NovaForge solves this by building a complete learning profile for each candidate and using it as the primary context for all AI-generated questions, evaluations, and final feedback.

---

## Features

| Feature | Description |
|---|---|
| 🤖 **AI-Powered Questions** | Gemini generates curriculum-specific questions at the right difficulty |
| 📊 **Adaptive Difficulty** | Difficulty calculated from experience, mission success rate, and consistency |
| 🔄 **Dynamic Follow-ups** | LLM generates follow-up questions when answers need more depth |
| 📋 **Full Interview Report** | Comprehensive final report with scores, strengths, weaknesses, and a learning path |
| ↩️ **Resume Interview** | Sessions persist in localStorage so interviews can be resumed after page reload |
| 🌙 **Dark/Light Mode** | Full theme support with system preference detection |
| 📱 **Responsive Design** | Works on desktop and tablet viewports |
| 🔒 **Secure Configuration** | API keys never committed; never logged; never exposed in error responses |

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│                   FRONTEND                  │
│  Next.js 15 + React + TypeScript            │
│  ┌──────────┐  ┌────────┐  ┌─────────────┐ │
│  │Dashboard │  │ Cands  │  │ Interview   │ │
│  │          │  │        │  │ [sessionId] │ │
│  └──────────┘  └────────┘  └─────────────┘ │
└───────────────────┬─────────────────────────┘
                    │ REST (JSON)
                    │ http://localhost:8000
┌───────────────────▼─────────────────────────┐
│                   BACKEND                   │
│  FastAPI + Python 3.13                      │
│  ┌──────────┐  ┌───────────┐               │
│  │  Router  │  │ SessionMgr│               │
│  └────┬─────┘  └───────────┘               │
│       │                                     │
│  ┌────▼──────────────────────────────────┐ │
│  │            AI Pipeline                │ │
│  │  AIService → PromptEngine             │ │
│  │  ContextBuilder → GeminiAdapter       │ │
│  │  ResponseParser                       │ │
│  └───────────────────┬───────────────────┘ │
└───────────────────────┼─────────────────────┘
                        │ google-genai SDK
┌───────────────────────▼─────────────────────┐
│         Google Gemini API                   │
└─────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| Next.js | 15 | React framework with App Router |
| React | 19 | UI library |
| TypeScript | 5 | Type safety |
| Tailwind CSS | v4 | Utility-first styling |
| shadcn/ui | latest | Accessible component library |
| Sonner | latest | Toast notifications |
| Lucide React | latest | Icon library |
| next-themes | latest | Dark/light mode |

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.13+ | Runtime |
| FastAPI | 0.103+ | REST API framework |
| Pydantic | v2 | Data validation and serialization |
| Uvicorn | 0.23+ | ASGI server |
| google-genai | 0.1+ | Official Google Gen AI SDK |
| python-dotenv | 1.0+ | Environment variable loading |

---

## Folder Structure

```
NovaForge - ViCodathon/
├── .env.example              # Environment variable template
├── .gitignore
├── pytest.ini                # Backend test configuration
├── requirements.txt          # Python dependencies
├── README.md
├── PROMPTS.md                # Full milestone engineering journal
│
├── backend/
│   ├── main.py               # FastAPI app factory and middleware
│   ├── api/
│   │   ├── dependencies.py   # FastAPI dependency injection singletons
│   │   ├── schemas.py        # Request/response Pydantic schemas
│   │   └── routers/
│   │       ├── health.py
│   │       ├── candidate.py
│   │       ├── curriculum.py
│   │       ├── interview.py
│   │       └── dashboard.py
│   ├── models/               # Domain model definitions (Pydantic)
│   │   ├── candidate.py
│   │   ├── curriculum.py
│   │   └── interview.py
│   ├── services/
│   │   ├── ai/               # AI pipeline
│   │   │   ├── ai_service.py       # Facade – coordinates the pipeline
│   │   │   ├── prompt_engine.py    # Prompt templates
│   │   │   ├── context_builder.py  # Context assembly from domain models
│   │   │   ├── gemini_adapter.py   # google-genai SDK wrapper
│   │   │   ├── response_parser.py  # JSON extraction and validation
│   │   │   ├── llm_provider.py     # Abstract LLM interface
│   │   │   └── exceptions.py       # AI-specific exception hierarchy
│   │   ├── domain/
│   │   │   ├── session_manager.py  # Interview session state machine
│   │   │   ├── strategies.py       # Difficulty + topic selection strategies
│   │   │   └── evaluation_interface.py
│   │   ├── repositories.py   # Data access (JSON files)
│   │   └── data_loaders.py
│   ├── data/                 # Static JSON data files
│   │   ├── candidates.json
│   │   └── curriculum.json
│   ├── tests/
│   │   ├── test_ai.py        # AI pipeline unit tests
│   │   ├── test_api.py       # API integration tests (mocked LLM)
│   │   └── test_domain.py    # Domain logic unit tests
│   └── utils/
│       ├── logger.py
│       └── constants.py
│
└── frontend/
    ├── package.json
    ├── next.config.ts
    └── src/
        ├── app/
        │   ├── layout.tsx
        │   ├── page.tsx              # Dashboard (home)
        │   ├── globals.css
        │   ├── error.tsx             # Global error boundary
        │   ├── not-found.tsx
        │   ├── candidates/           # Candidate listing page
        │   ├── curriculum/           # Curriculum progress page
        │   ├── interview/
        │   │   └── [sessionId]/      # Active interview session page
        │   └── settings/
        ├── components/
        │   ├── ui/                   # Primitive components
        │   ├── layout/               # Layout shells
        │   ├── dashboard/            # Dashboard-specific components
        │   └── interview/            # Interview-specific components
        ├── hooks/
        │   ├── useInterview.ts       # Interview session state management
        │   ├── useCandidates.ts
        │   ├── useCurriculum.ts
        │   └── useDashboard.ts
        └── lib/
            └── api/                  # Typed API client layer
```

---

## AI Workflow

The following pipeline executes on every LLM interaction:

```
Router endpoint
    │
    ▼
AIService (facade)
    │
    ├── ContextBuilder.build_full_context()
    │       Assembles: candidate profile + curriculum topic +
    │       interview plan + full Q&A history transcript
    │
    ├── PromptEngine.build_*_prompt()
    │       Injects context into role-specific prompt template
    │       Instructs the LLM: "Return ONLY valid JSON. No markdown."
    │
    ├── GeminiAdapter._call_gemini()
    │       Calls google-genai SDK with:
    │         response_mime_type="application/json"
    │         max_output_tokens=2048
    │       Retries on 429 (rate limit) up to 3×
    │       Raises domain exceptions on 401/404/timeout
    │
    └── ResponseParser.parse_*()
            Strips markdown fences if present
            Parses JSON
            Validates required keys
            Raises InvalidResponseException on malformed output
```

### Robust JSON Parser & AI Resilience
The AI Service implements a 9-step resilient parsing pipeline to ensure the system never crashes due to LLM hallucinations:
1. Attempt raw JSON parsing.
2. Strip markdown fences and retry.
3. Use a custom bracket-counting algorithm to isolate the first valid JSON object, ignoring any conversational filler.
4. Validate strict schemas for questions, evaluations, and reports.
5. If parsing fails, the `AIService` automatically intercepts the exception, injects a strict formatting rule into the prompt, and retries the Gemini API once.
6. The frontend maps any remaining errors to user-friendly messages without exposing stack traces.

## 🏗 Backend Architecture

The backend is built on a strict layered architecture. Each layer has one responsibility and depends only on layers below it.

```
Router (HTTP boundary)
  └── FastAPI Dependency Injection (dependencies.py)
        └── AIService (facade – no HTTP knowledge)
              ├── ContextBuilder   (pure functions, no I/O)
              ├── PromptEngine     (pure functions, no I/O)
              ├── GeminiAdapter    (I/O boundary – Gemini API)
              └── ResponseParser   (pure functions, no I/O)
```

**Session Management** (`SessionManager`) runs as an in-memory singleton. Sessions survive for the lifetime of the server process. Each session tracks:
- The candidate ID
- The list of questions asked (with answers, scores, and feedback)
- The current difficulty level and curriculum day
- Session status: `NOT_STARTED → IN_PROGRESS → COMPLETED`

**Error Handling** uses a typed exception hierarchy (`AIEngineException` and subclasses). A global FastAPI exception handler (`@app.exception_handler(AIEngineException)`) converts all AI exceptions to clean `500` JSON responses. No stack traces ever reach the client.

---

## Frontend Architecture

The frontend follows a strict, component-driven design philosophy:

- **API Layer** (`src/lib/api/`): All backend communication is centralized here with typed interfaces per domain (`interview.ts`, `candidate.ts`, `curriculum.ts`, `dashboard.ts`).
- **Custom Hooks** (`src/hooks/`): React hooks wrap the API layer and manage loading, error, and data state. Components only consume hooks — never call `fetch` directly.
- **Components** (`src/components/`): Organized into `ui/` (primitives), `layout/` (shells), `dashboard/`, and `interview/`.
- **Design System**: Centralized in `globals.css` using CSS custom properties for colors, shadows, and typography. Tailwind CSS v4 native CSS variable support.

**Resume Interview**: On session start, `session_id` is written to `localStorage`. The Dashboard reads it on mount and enables a "Resume Interview" button. If the server no longer knows about the session (e.g., after a restart), the hook catches the `404`, clears localStorage, and redirects gracefully to the Dashboard.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/candidates` | List all candidate personas |
| `GET` | `/candidates/{id}` | Get a specific candidate |
| `GET` | `/curriculum` | Get the full curriculum |
| `GET` | `/curriculum/day/{day}` | Get a specific curriculum day |
| `GET` | `/dashboard` | Get dashboard statistics |
| `POST` | `/interview/start` | Start a new interview session |
| `POST` | `/interview/{id}/next` | Generate the next question |
| `POST` | `/interview/{id}/answer` | Submit an answer for evaluation |
| `GET` | `/interview/{id}` | Get current session state |
| `GET` | `/interview/{id}/feedback` | Get final feedback (completed sessions only) |

Full interactive documentation is available at **http://localhost:8000/docs** when the backend is running.

---

## Environment Variables

All configuration is managed through environment variables. Copy `.env.example` to `.env` and fill in the values.

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Your Google Gen AI API key from [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| `GEMINI_MODEL` | ✅ Yes | The Gemini model to use (e.g. `gemini-2.5-flash-lite-preview-06-17`) |
| `NEXT_PUBLIC_API_URL` | ✅ Yes | The backend URL for the frontend (e.g. `http://localhost:8000`) |
| `PORT` | ❌ Optional | Backend port, defaults to `8000` |
| `ENVIRONMENT` | ❌ Optional | `development` or `production` |

> ⚠️ **Never commit your `.env` file.** It is in `.gitignore`. If you accidentally commit a key, revoke it immediately.

---

## Installation

### Prerequisites

- **Git**
- **Python 3.13+** (check: `python --version`)
- **Node.js 20+** (check: `node --version`)
- A **Google Gemini API key** from [aistudio.google.com](https://aistudio.google.com/app/apikey)

---

### 1. Clone the Repository

```bash
git clone https://github.com/Vineet375/NovaForge-ViCodathon.git
cd "NovaForge - ViCodathon"
```

---

### 2. Backend Setup

> **Important**: All backend commands must be run from the **project root** directory (not from inside `backend/`). This is because the Python packages use `backend.*` absolute imports, which require the project root to be on the Python path.

**Create and activate the virtual environment:**

```bash
# Windows (PowerShell)
python -m venv backend/venv
backend\venv\Scripts\activate

# macOS / Linux
python3 -m venv backend/venv
source backend/venv/bin/activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Create your environment file:**

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your `GEMINI_API_KEY` and confirm `GEMINI_MODEL`:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash-lite-preview-06-17
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

---

## Running the Application

Both the backend and frontend must be running simultaneously in separate terminals.

### Run Backend

> Run from the **project root directory**.

```bash
# Windows – activate venv first
backend\venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000

# macOS / Linux
source backend/venv/bin/activate
uvicorn backend.main:app --reload --port 8000
```

The backend will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs

### Run Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at **http://localhost:3000**.

---

## Running Tests

### Backend Tests (pytest)

> Run from the **project root directory** with the venv activated.

```bash
# Activate venv first
backend\venv\Scripts\activate   # Windows
source backend/venv/bin/activate  # macOS/Linux

pytest -v
```

Expected output: **17 tests pass**. The test suite uses mock LLM responses — no real API key is needed.

### Frontend Type Check & Build

```bash
cd frontend
npm run build
```

A successful build validates:
- Zero TypeScript errors
- Zero Next.js compilation errors
- All pages statically analyzable

---

## Gemini API Configuration

NovaForge requires the `GEMINI_API_KEY` and `GEMINI_MODEL` environment variables to be set before starting the backend. The application will **fail to start** if either is missing — this is intentional to prevent silent misconfiguration.

### Choosing a Model

Recommended model: **`gemini-2.5-flash-lite-preview-06-17`**

If you see a `404` error:
```
The configured Gemini model '<model_name>' is unavailable or deprecated.
Please update GEMINI_MODEL in your .env file.
```

Visit the [Gemini API models page](https://ai.google.dev/gemini-api/docs/models) and update `GEMINI_MODEL` in your `.env` with a currently available model name.

> **Policy**: NovaForge never silently falls back to a different model. If the configured model is unavailable, the application raises a clear, user-friendly error. This prevents unpredictable behavior as Google updates or retires models.

### API Key Safety

- `GEMINI_API_KEY` is **never logged**. All error messages are sanitized to replace the key with `[REDACTED]` before being written to logs.
- `GEMINI_API_KEY` is **never returned** in any API response body.
- The `.env` file is gitignored and will never be committed.

---

## Common Troubleshooting

### Backend fails to start: "GEMINI_API_KEY environment variable is not set"

Your `.env` file is missing or the variable is not set. Ensure `.env` exists in the **project root** (not inside `backend/`) and contains `GEMINI_API_KEY=your_key`.

### Backend fails to start: "GEMINI_MODEL environment variable is not set"

Add `GEMINI_MODEL=gemini-2.5-flash-lite-preview-06-17` (or the current recommended model) to your `.env`.

### Interview returns 500: "The configured Gemini model '...' is unavailable or deprecated"

The model in your `.env` is no longer available. Update `GEMINI_MODEL` to a currently available model from the [Gemini API models list](https://ai.google.dev/gemini-api/docs/models).

### Frontend shows "Failed to load session" immediately

The backend is not running or is not reachable at `NEXT_PUBLIC_API_URL`. Ensure the backend is started and the URL in `.env` matches the port.

### `ModuleNotFoundError: No module named 'backend'`

You are running the server from inside the `backend/` directory. **Always run from the project root:**
```bash
# Correct
uvicorn backend.main:app --reload

# Incorrect – do NOT do this
cd backend
uvicorn main:app --reload
```

### pytest: "ModuleNotFoundError"

Same cause as above. Run `pytest` from the **project root**, not from inside `backend/`.

### CORS error in browser

Ensure `NEXT_PUBLIC_API_URL` in `.env` exactly matches the backend address (including port). The backend currently allows all origins (`allow_origins=["*"]`).

---

## Deployment Notes

This project is built for the hackathon demo environment. For production deployment, consider:

- **Sessions**: Replace the in-memory `SessionManager` with a Redis or database-backed store.
- **CORS**: Restrict `allow_origins` to specific frontend domains.
- **Secrets**: Use a secrets manager (AWS Secrets Manager, GCP Secret Manager) instead of `.env` files.
- **Rate Limiting**: Add API rate limiting middleware to protect the Gemini API quota.
- **Frontend**: Run `npm run build` and serve the `.next/` output with a CDN.
- **Backend**: Run Uvicorn behind a reverse proxy (Nginx) with multiple workers.

---

## Known Limitations

- **In-memory sessions**: All interview sessions are lost when the backend server restarts. The frontend detects this and gracefully redirects to the Dashboard.
- **Single-server**: No horizontal scaling support — sessions are not shared across multiple server instances.
- **Curriculum data is static**: The `candidates.json` and `curriculum.json` files are read-only at startup. No admin UI to manage them.
- **No authentication**: Any user can start an interview for any candidate ID. Intended for demo/hackathon use.
- **Model availability**: Gemini model names change. If `GEMINI_MODEL` becomes deprecated, the application will return a clear error with instructions to update `.env`.

---

## Future Improvements

- [ ] Persistent session storage (Redis or PostgreSQL)
- [ ] Authentication and role-based access control
- [ ] Candidate onboarding flow (upload resume, self-assessment)
- [ ] Voice interview mode (Speech-to-Text + Text-to-Speech)
- [ ] Interviewer dashboard with session analytics and PDF export
- [ ] Multi-model support (Claude, GPT-4o) via a provider abstraction layer
- [ ] Streaming responses for real-time question typing animation
- [ ] Automated scoring calibration based on historical interview data

---

## Authors

**Team NovaForge** — ViCodathon 2026

Built with ❤️ for the **AB Talks ViCodathon 2026** hackathon.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

## Milestone 18.3: AI Failover Hardening
- **Test Environment Isolation**: Enforced \pp.dependency_overrides\ in pytest to ensure 100% offline isolation without relying on fragile .env states.
- **Failover Latency Optimization**: Added strict timeouts (\httpx.Timeout(7.0, connect=3.0)\ and \max_retries=0\) to the NVIDIA provider and 10s timeouts to Gemini, guaranteeing bounded failure responses (< 10s per layer).
- **MockProvider Fallback Safety**: Mock fallback deterministically loops through a large pool of unique questions, ensuring UI progression without duplicates during complete API outages.


## Backend Dependencies
- Ensure `openai>=1.0.0` is installed via `requirements.txt` for the NVIDIA provider to function.