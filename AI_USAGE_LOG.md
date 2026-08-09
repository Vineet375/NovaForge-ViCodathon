# NovaForge – AI Usage Log

This document records how AI tools were utilized during the development of NovaForge for the ViCodathon 2026 hackathon.

## AI Tools Used
- **Google Antigravity (Agentic AI):** Extensively used for scaffolding, writing boilerplate, configuring systems, implementing complex state machines, optimizing algorithms, and debugging issues throughout the hackathon.
- **Google Gen AI (Gemini APIs):** Integrated into the production application to generate dynamic interview questions and final evaluations.
- **NVIDIA NIM (Llama-3.1 APIs):** Integrated into the production application as part of a high-availability fallback provider chain.

## Major Development Areas with AI Assistance
*Note: The actual step-by-step prompt history and architectural decisions are preserved in detail within [PROMPT.md](PROMPT.md).*

### 1. Project Planning & Scaffolding
**What AI contributed:** Generated the initial Next.js + FastAPI folder structure, configurations (Tailwind, TypeScript), standard utility modules (logging, JSON loading), and established the initial Data Models using Pydantic.
**Developer verification:** Verified build success, syntax correctness, and architectural consistency.

### 2. Core Domain & Interview State Machine
**What AI contributed:** Implemented the in-memory `SessionManager`, `DifficultyStrategy`, and `TopicSelectionStrategy`. It defined the interfaces for LLM providers and established the core constraints of the interview lifecycle (4 questions, deduplication, state transitions).
**Developer verification:** Wrote and executed comprehensive end-to-end Python scripts and Pytest suites to validate state transitions and prevent logical regressions.

### 3. API Layer and Integration
**What AI contributed:** Created FastAPI routers, dependency injection frameworks, structured prompt engines, JSON parsing safeguards, and robust error handling boundaries.
**Developer verification:** Tested endpoints locally, verified schema validation, and confirmed correct error mapping (500/400) without leaking stack traces.

### 4. Frontend Implementation
**What AI contributed:** Scaffolded React components with shadcn/ui and Tailwind CSS. Implemented complex client-side React hooks (`useInterviewSession`) to manage loading states, API calls, error handling, and localStorage persistence for session recovery.
**Developer verification:** Manually verified UI responsiveness, state synchronization, browser console logs, and UX flow.

### 5. AI Provider Chain & Latency Optimization (Milestone 18)
**What AI contributed:** Engineered a resilient failover chain (Gemini → NVIDIA Primary → NVIDIA Secondary → MockProvider). Implemented background task generation (`FastAPI BackgroundTasks`), bounded API timeouts (5-10s), lightweight question deduplication (`difflib`), and prompt contextualization.
**Developer verification:** Extensive live simulation scripts and manual end-to-end browser testing to ensure exact 4-question sequences, zero duplicates, and sub-20-second failovers during complete API outages.

## References
For the exact chronological log of AI prompts, engineering decisions, and iterative milestones, please read the genuine historical transcript preserved in **[PROMPT.md](PROMPT.md)** (Prompt / transcript evidence available).
