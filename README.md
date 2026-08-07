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
