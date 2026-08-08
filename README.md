# NovaForge AI Interview Agent
ViCodathon 2026 – India's AI-First 48 Hour Vibe Coding Hackathon! 

An AI Interview Agent that conducts personalized technical interviews based on a candidate's learning journey.

## Hackathon
AB Talks ViCodathon 2026
**Team**: NovaForge

## Tech Stack
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS (v4), shadcn/ui
- **Backend**: Python, FastAPI, Pydantic
- **AI**: Google Generative AI (Gemini)

---

## Frontend Architecture & Design System (Milestone 8)

The frontend for NovaForge follows a strict, highly reusable design philosophy inspired by modern SaaS products (e.g., Vercel, Linear, Stripe). The design communicates a premium, AI-first, fast, and accessible enterprise experience.

### Design Tokens
Our core design tokens are centralized in `frontend/src/app/globals.css`, leveraging Tailwind CSS v4's native CSS variable support:
- **Typography Scale**: Built natively using the `Geist` and `Geist Mono` font families for maximum legibility and modern aesthetics.
- **Color Palette**: A curated semantic color scale featuring deep indigo/navy as the primary brand color, combined with monochromatic grays for structure, allowing content to breathe.
- **Shadows & Elevation**: Custom `--shadow-premium` variables provide a subtle depth layered look for cards, dropdowns, and interactive elements.
- **Theme Support**: Seamless native dark mode integration with full persistence using `next-themes`. Variables gracefully switch from a clean white light theme to a deep, OLED-friendly dark theme.

### Reusable UI Foundations
Instead of building monolithic pages, the frontend is assembled using tightly-scoped, reusable components located in `frontend/src/components`:
- **Layout System (`layout-foundation.tsx`)**: Exposes wrappers like `PageContainer`, `Section`, `SectionHeader`, and `SectionTitle` that instantly align margins, paddings, and widths identically across all future pages.
- **Navigation (`navbar.tsx`, `sidebar.tsx`)**: Reusable shells for top and side navigation that integrate seamlessly with the Layout foundation.
- **Cards (`card.tsx`)**: Premium bounding boxes with integrated hover animations and shadow drops.
- **Buttons (`button.tsx`)**: Extends primitive buttons to include a `LoadingButton` variant with integrated spinners and disabled states.
- **Skeletons (`skeleton.tsx`)**: Reusable loading placeholder blocks (`CardSkeleton`, `PageHeaderSkeleton`) to prevent layout shifts during asynchronous state transitions.
- **Theme Toggle (`theme-toggle.tsx`)**: Accessible toggle that triggers rapid UI recoloring with subtle icon animations.

All components adhere strictly to accessibility standards (ARIA roles, robust focus rings, high contrast text).

---

## Backend Architecture

The backend is strictly decoupled into layers:
- **API (`backend/api/`)**: FastAPI routing layer exposing REST resources.
- **Domain (`backend/services/domain/`)**: Pure state machine driving logic without external AI dependency (`SessionManager`).
- **AI Layer (`backend/services/ai/`)**: Specialized handlers (`PromptEngine`, `ContextBuilder`, `ResponseParser`, `GeminiAdapter`) that safely constrain unpredictable LLM outputs into structured JSON.

---

## Environment Setup

### Prerequisites
- Node.js (for Frontend)
- Python 3.13+ (for Backend)

### API Keys
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_google_gen_ai_key_here
GEMINI_MODEL=gemini-3.5-flash
```
> **Warning**: Never commit your real API key to version control.

### Installation

#### Backend
```bash
python -m venv backend/venv
# On Windows
backend\venv\Scripts\activate
# On macOS/Linux
source backend/venv/bin/activate

pip install -r requirements.txt
```

#### Running the Backend Server
```bash
# On Windows
backend\venv\Scripts\activate
uvicorn backend.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
```

---

## Testing

### Backend
The backend utilizes `pytest` with the FastAPI `TestClient` for 100% in-memory validation of domain logic and API routes.
```bash
cd backend
venv\Scripts\activate
pytest
```

### Frontend
The frontend codebase enforces extreme strictness via TypeScript and Next.js builds.
```bash
cd frontend
npm run build
```
The build process statically analyzes, typchecks, and compiles all SCSS and TS modules, guaranteeing deployment readiness.

## Frontend API Integration

NovaForge features a strictly typed, centralized API layer inside \src/lib/api\.
All communication with the backend REST API is localized here to avoid duplicate logic across components.
The integration consists of:
1. **API Client (\pi.ts\)**: Handles base HTTP fetching, header injection, and centralized error handling via the custom \ApiError\ class.
2. **Domain Clients**: Separated out by domain (e.g. \candidate.ts\, \curriculum.ts\, \interview.ts\, \dashboard.ts\) providing typed endpoints.
3. **Custom Hooks (\src/hooks\)**: Reusable React hooks wrapping API clients for state management (loading, error, data).
   - \useCandidates\: Fetches available candidate personas.
   - \useCurriculum\: Loads dynamic curriculum progress.
   - \useDashboard\: Aggregates statistics and timeline events.
   - \useInterview\ & \useInterviewSession\: Complex state management for active AI interviews.

## Interview Experience

The core interview flow exists under \/interview/[sessionId]\ and implements an active connection to the backend Gemini AI agent.
Features include:
- Real-time AI generated questions based on the candidate persona and curriculum difficulty.
- Interactive text areas with disabled loading states during evaluation.
- Live progress bars indicating session status.
- Immediate localized feedback per answer using the \AI Feedback\ panel.
- Dynamic follow-up questions generated by the LLM based on specific responses.
- Complete final evaluation reporting generated upon finishing all 8 questions.

## Milestone 11: Premium Product Experience
- Fully polished Dashboard with Analytics Chart
- Candidate Detail Profiles in Modals
- Premium Interview Feedback Report layout
- Comprehensive Error Boundary & Missing States UI
- Complete Accessibility review & ARIA labels

## Milestone 12: Stability and API Hardening
- Dynamic Gemini API configuration via `.env`.
- Hardened Gemini API layer with exponential backoff retries and explicit `max_output_tokens` JSON constraints.
- Complete domain-specific exception handling via `AIEngineException`.
- Graceful degradation through global FastAPI exception handlers to prevent raw tracebacks.
- New "Resume Interview" capability via frontend `localStorage` persistence, recovering safely from server reloads or API exhaustion.