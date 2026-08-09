# NovaForge

NovaForge is a production-grade AI-powered technical interview system built for the ViCodathon 2026 hackathon. It analyzes a candidate's curriculum progress, learning signals, and experience profile to dynamically generate 4 personalized technical questions at the appropriate difficulty level, conducting a context-aware technical interview.

## Problem Statement

Traditional technical screenings are generic and one-size-fits-all. They don't account for what a candidate has actually learned during their specific training program, their demonstrated performance (such as missions passed, skipped, or retried), or the difficulty level appropriate for their seniority and track record.

## Solution

NovaForge solves this by building a complete learning profile for each candidate and using it as the primary context for all AI-generated questions, evaluations, and final feedback. Unlike generic interview tools, NovaForge understands exactly what the candidate has studied and tailors every question to their specific curriculum journey—from RAG pipelines and vector databases to full-stack React/FastAPI application development.

## Key Features

- **Candidate management:** Select from a predefined list of candidates with unique learning profiles.
- **Curriculum management:** Track candidate progress through structured curriculum days and modules.
- **AI-generated interview questions:** Gemini and NVIDIA models dynamically generate personalized questions.
- **Adaptive/technical interview flow:** Generates exactly 4 targeted questions based on the candidate's background.
- **Answer submission:** Candidates can submit answers to the generated technical questions.
- **AI-powered evaluation:** Evaluates answers in the background and progresses the interview.
- **Performance summary:** Final evaluation calculating an overall score out of 10.
- **Strengths and growth areas:** Generates a comprehensive final report with strengths and weaknesses.
- **Dashboard statistics:** High-level metrics showing active sessions, total candidates, and curriculum modules.
- **Production deployment:** Fully functional deployed architecture with Vercel and Render.

## How NovaForge Works

1. **Candidate selection**: The user selects a candidate persona from the dashboard.
2. **Interview session creation**: The backend initializes an in-memory interview session tailored to the candidate's curriculum progress and experience.
3. **AI question generation**: The system instructs the AI to generate a highly personalized technical question.
4. **Candidate answer**: The user inputs an answer in the frontend text area.
5. **Answer evaluation**: The backend submits the answer and schedules the next state.
6. **Next question**: The AI generates the next question, avoiding duplicates via local similarity checks.
7. **Final evaluation**: After 4 questions, the AI produces a holistic evaluation.
8. **Performance report**: The final score, strengths, and weaknesses are displayed to the user.

## Architecture

Browser
↓
Next.js Frontend / Vercel
↓
FastAPI Backend / Render
↓
AI provider / model integration (Gemini → NVIDIA → MockProvider fallback)
↓
Curriculum + candidate data (Local JSON state)
↓
Evaluation/report returned to frontend

## Tech Stack

**Frontend:**
- Next.js 15
- React 19
- TypeScript 5
- Tailwind CSS v4
- Vercel

**Backend:**
- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- Google GenAI SDK (Gemini API)
- OpenAI SDK (NVIDIA NIM endpoints)
- Render

## Project Structure

```
NovaForge - ViCodathon/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── PROMPT.md                # AI Development Prompt History
├── AI_USAGE_LOG.md          # AI Usage Log
├── FINAL_DOCUMENTATION.md   # Final Project Documentation
├── pytest.ini
├── requirements.txt
├── backend/
│   ├── main.py              # FastAPI application
│   ├── api/                 # API routers and dependencies
│   ├── data/                # Static JSON data files
│   ├── models/              # Pydantic domain models
│   ├── services/            # Core business logic and AI pipeline
│   ├── tests/               # Backend tests (pytest)
│   └── utils/               # Helpers and constants
├── docs/
│   └── technical-spec.md
└── frontend/
    ├── next.config.ts
    ├── package.json
    └── src/
        ├── app/             # Next.js App Router pages
        ├── components/      # React UI components
        ├── hooks/           # Custom React hooks
        └── lib/             # API client layer
```

## Local Development

### Prerequisites
- Git
- Python 3.13+
- Node.js 20+

### 1. Clone the Repository
```bash
git clone https://github.com/Vineet375/NovaForge-ViCodathon.git
cd "NovaForge - ViCodathon"
```

### 2. Backend Setup
All backend commands must be run from the **project root** directory.

```bash
# Create and activate virtual environment
python -m venv backend/venv
# Windows
backend\venv\Scripts\activate
# macOS/Linux
source backend/venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables template
cp .env.example .env
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cd ..
```

### 4. Running the Application

**Run Backend:**
From the project root:
```bash
uvicorn backend.main:app --reload --port 8000
```
API available at `http://localhost:8000`.

**Run Frontend:**
```bash
cd frontend
npm run dev
```
Frontend available at `http://localhost:3000`.

## Environment Variables

Required environment variables for local development (copy from `.env.example` to `.env`):

```env
# AI Providers
GEMINI_API_KEY_1=your_gemini_key_1
GEMINI_API_KEY_2=your_gemini_key_2
GEMINI_API_KEY_3=your_gemini_key_3
GEMINI_MODEL=gemini-2.5-flash-lite-preview-06-17

NVIDIA_API_KEY_1=your_nvidia_key_1
NVIDIA_MODEL_PRIMARY=meta/llama-3.1-70b-instruct
NVIDIA_API_KEY_2=your_nvidia_key_2
NVIDIA_MODEL_SECONDARY=meta/llama-3.1-8b-instruct

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend overrides
FRONTEND_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ENVIRONMENT=development
PORT=8000
```
*(Note: Real API keys must be securely configured in the hosting provider's dashboard and should never be committed to the repository.)*

## Deployment

**Frontend:**
Deployed on Vercel:
[https://novaforge-vicodathon.vercel.app](https://novaforge-vicodathon.vercel.app)

**Backend:**
Deployed on Render:
[https://novaforge-vicodathon.onrender.com](https://novaforge-vicodathon.onrender.com)

## Live Demo

**[Launch NovaForge Production Demo](https://novaforge-vicodathon.vercel.app)**

## AI Usage

AI was utilized extensively throughout the development of NovaForge:
- **AI-assisted development:** The foundational project structure, boilerplate, routing, styling, and complex state machine logic were heavily assisted and generated via AI prompting.
- **AI-powered interview question generation:** The core product uses Gemini and NVIDIA models to dynamically generate technical interview questions personalized to a candidate's profile.
- **AI-powered answer evaluation/final feedback:** The final assessment report (scores, strengths, weaknesses) is generated entirely by the AI pipeline.

For detailed records of AI-assisted development, please refer to the [AI Usage Log](AI_USAGE_LOG.md) and [Prompt History](PROMPT.md).

## Testing

Production tests performed and verified successfully:
- frontend loads successfully.
- dashboard loads correctly with API integration.
- candidate selector loads successfully.
- interview starts and persists in-memory state.
- AI generates dynamic, personalized questions.
- answers can be submitted and tracked.
- interview progresses up to exactly 4 questions.
- final evaluation and score report appears upon completion.
- comprehensive deterministic backend unit test suite (`pytest -v`) passes 100%.

## Screenshots

*(No screenshots currently available in the repository.)*

## Demo Video

[Demo Video](LINK_TO_BE_ADDED)

## Team

**Team NovaForge** — ViCodathon 2026

## Future Scope

- Persistent session storage (Redis/PostgreSQL) across instance restarts.
- Authentication and role-based access control.
- Voice interview mode (Speech-to-Text + Text-to-Speech).
- Automated scoring calibration based on historical interview data.

## License

MIT License — see [LICENSE](LICENSE) for details.
