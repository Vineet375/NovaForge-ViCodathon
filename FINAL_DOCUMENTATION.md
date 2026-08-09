# NovaForge – Final Project Documentation

## 1. Project Overview
NovaForge is an AI-powered technical interview agent built for the ViCodathon 2026 hackathon. It dynamically generates personalized, context-aware technical interviews based on a candidate's learning journey and experience.

## 2. Problem Statement
Traditional technical screenings are generic. They fail to account for a candidate's specific curriculum progress, learning signals (missions passed, retried, skipped), and appropriate difficulty level based on their seniority. This leads to rigid and uninsightful assessments.

## 3. Proposed Solution
NovaForge resolves this by building a precise learning profile for each candidate. It leverages generative AI (Gemini/Llama) to produce hyper-targeted technical questions and evaluations based strictly on what the candidate has actually studied (e.g., RAG, Vector Databases, Next.js, FastAPI).

## 4. System Architecture
NovaForge uses a strictly decoupled, layered architecture:
- **Client Layer:** Next.js 15 (React 19) frontend providing an interactive, resilient dashboard and interview UI.
- **API Boundary:** FastAPI backend strictly defining REST contracts via Pydantic schemas.
- **Domain Layer:** Pure Python business logic (`SessionManager`, `DifficultyStrategy`) managing the interview state machine.
- **AI Integration Layer:** `AIService` facade orchestrating context builders, prompt engines, LLM adapter chains, and structured JSON parsing.

## 5. Core Features
- Adaptive candidate difficulty calculations.
- Context-aware technical question generation.
- Highly resilient provider failover (Gemini → NVIDIA → MockProvider).
- Idempotent API endpoints preventing duplicate question generation.
- Full interview final report (Score out of 10, Strengths, Weaknesses).

## 6. AI Integration
NovaForge interfaces with both **Google Gemini** and **NVIDIA NIM** (Llama-3.1).
The AI pipeline includes:
- **ContextBuilder:** Flattens candidate profiles and curriculum data into a dense textual context string.
- **PromptEngine:** Injects context into strict instruction templates enforcing JSON outputs.
- **ResponseParser:** Uses defensive regex and bracket-counting algorithms to safely extract JSON payloads from occasionally chatty LLM responses.

## 7. Interview Workflow
1. **Selection:** User selects a Candidate from the Dashboard.
2. **Init:** Backend initializes a 4-question session in memory.
3. **Generate:** The AI generates a personalized technical question via a background task.
4. **Answer:** The candidate submits an answer.
5. **Evaluate:** The backend progresses the state machine. Steps 3-4 repeat until 4 questions are reached.
6. **Report:** The AI generates a final holistic evaluation report.

## 8. Technology Stack
- **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS v4
- **Backend:** Python 3.13, FastAPI, Uvicorn, Pydantic
- **AI Models:** Gemini 2.5 Flash Lite, Llama-3.1 70B/8B (via NVIDIA)

## 9. Deployment Architecture
- **Frontend Hosting:** Vercel
- **Backend Hosting:** Render (Single-replica persistent web service)
- **State:** In-memory dictionary state (designed for demo/hackathon scoping).

## 10. Testing and Validation
NovaForge is hardened through extensive automated and manual testing:
- **100% Backend Unit Tests:** Pytest suites validate the entire AI layer (using mocked providers), the domain logic, and API endpoints.
- **Live Failover Simulation:** Scripts verifying graceful degradation and prompt deduplication during simulated API rate limits.
- **Frontend Builds:** Next.js production builds verify static analyzability and strict type safety.

## 11. Screenshots / Demo
[Demo Video Placeholder](LINK_TO_BE_ADDED)

## 12. Limitations
- **In-memory Sessions:** Active interviews are lost if the Render backend restarts.
- **Static Curriculum:** Curriculum and candidate JSONs are read-only.
- **No Auth:** Open access for demonstration purposes.

## 13. Future Scope
- **Persistent State:** Integrating Redis or PostgreSQL for session storage.
- **Admin Dashboard:** Real-time analytics and LLM performance telemetry.
- **Multimodal Interviews:** Adding voice-to-text input mechanisms.

## 14. Repository and Live Demo
- **Repository:** https://github.com/Vineet375/NovaForge-ViCodathon
- **Live Frontend:** https://novaforge-vicodathon.vercel.app
- **Live Backend API:** https://novaforge-vicodathon.onrender.com
