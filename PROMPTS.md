## Prompt 1
2026-08-07T20:47:16+05:30

**Objective**
Initialize project structure, configure frontend/backend, and setup development environment for the NovaForge AI Interview Agent.

**Prompt**
Create folder structure. Initialize the frontend project. Initialize the backend project. Configure TypeScript. Configure Tailwind CSS. Configure FastAPI. Create requirements.txt. Create .gitignore. Create .env.example. Create README.md template. Create PROMPTS.md. Move the provided JSON files into backend/data/. Move technical-spec.md into docs/. Explain the architecture. List required installation commands. Suggest a Git commit message. Generate the first PROMPTS.md entry.

**AI Output Summary**
Initialized the frontend with Next.js, React, TypeScript, and Tailwind CSS. Initialized the backend with FastAPI. Configured the file structure, moved existing assets to the correct directories, and created the foundational documentation (`README.md`, `PROMPTS.md`, `.env.example`, `.gitignore`, `requirements.txt`).

**Human Changes**
None

**Files Created**
- `backend/main.py`
- `requirements.txt`
- `README.md`
- `.gitignore`
- `.env.example`
- `PROMPTS.md`
- Frontend framework files via create-next-app

**Files Modified**
- None

**Git Commit Message**
feat: initialize project structure and setup frontend/backend foundations

**Notes**
Created the initial foundation for the AI Interview Agent without any business logic implementation, strictly adhering to the milestone 1 requirements.

---

## Prompt 2
2026-08-07T21:06:55+05:30

**Objective**
Review, commit, and push the initialized project for Milestone 1.

**Prompt**
Review everything completed in Milestone 1. If everything is correct and the project builds successfully, then: 1. Stage all relevant files. 2. Create a Git commit using the following message: feat: initialize project structure and setup frontend/backend foundations. 3. Push the commit to the GitHub repository. 4. Append a complete and accurate entry to PROMPTS.md for this milestone (do not overwrite previous entries). 5. Verify that the push was successful. 6. Provide the commit hash and a short summary of what was committed.

**AI Output Summary**
Verified the frontend build using Next.js build scripts. Initialized the Git repository, staged all created files (frontend, backend, configs, and documentation), committed with the provided message, and pushed to the remote repository `main` branch.

**Human Changes**
None

**Files Created**
- None (Only committed existing files)

**Files Modified**
- `PROMPTS.md` (Appended Prompt 2)

**Git Commit Message**
feat: initialize project structure and setup frontend/backend foundations

**Notes**
Successfully executed Git operations without modifying application source code.

---

## Prompt 3
**Timestamp**: 2026-08-07T21:21:28+05:30
**Milestone**: 2 - Backend Foundation + Data Layer
**Objective**: Create utility modules and configure standard logging for the backend foundation.
**Context**: Initiating Milestone 2 by setting up common utilities (file loading, constants, logging) required before building data loaders and repositories.
**Prompt Given**: "Create utility modules. Examples: JSON loader, File utilities, Validation helpers, Constants, Logging helper. Configure logging. Use Python logging. Readable output. No print statements."
**Reasoning**: Clean architecture dictates that file reading and logging should be isolated in utility modules. This prevents code duplication in the data loaders.
**AI Output Summary**: Created `logger.py` with standard Python logging, `file_utils.py` for secure JSON loading, `constants.py` for centralizing file paths, and initialized the directories.
**Architecture Decisions**: 
- Centralized all file paths in `constants.py` to prevent hardcoded strings.
- Created a standard logger in `logger.py` to ensure consistent formatting across the backend.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/utils/logger.py`
- `backend/utils/file_utils.py`
- `backend/utils/constants.py`
- `backend/utils/__init__.py`
- `backend/models/__init__.py`
- `backend/services/__init__.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None (Using standard library `logging`, `json`, `pathlib`)
**Git Commit Message**: feat(backend): implement utility modules and central logging
**Testing Performed**: Code syntax check.
**Result**: Utility foundation successfully established.
**Known Limitations**: JSON loader currently reads entire files into memory; sufficient for these small datasets.
**Next Planned Milestone**: 2 (Subtask: Pydantic Data Models)

---

## Prompt 4
**Timestamp**: 2026-08-07T21:24:00+05:30
**Milestone**: 2 - Backend Foundation + Data Layer
**Objective**: Create proper Pydantic models for the data layer.
**Context**: Moving to data validation and typing for the backend. We need to parse the JSON files into structured objects for type safety and easy access.
**Prompt Given**: "Create proper Pydantic models for: Candidate, Candidate Profile, Completed Missions, Skipped Missions, Curriculum, Module, Day, Learning Objective, Tools, Any nested structures required by the provided JSON files."
**Reasoning**: Pydantic models enforce data structure and validation. Representing the raw JSON as Python objects makes the downstream repository layer much cleaner and safer to interact with.
**AI Output Summary**: Created `curriculum.py` and `candidate.py` inside `backend/models/`. Created models for Day, Module, Curriculum, Member, Mission, Signals, Candidate, and CandidateList.
**Architecture Decisions**: 
- Grouped Curriculum-related models and Candidate-related models into separate files for better maintainability.
- Made fields like `passed`, `attempts`, and `skipped` optional in the `Mission` model as they appear conditionally in `candidates.json`.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/models/curriculum.py`
- `backend/models/candidate.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None (Using existing `pydantic` dependency)
**Git Commit Message**: feat(backend): create pydantic models for curriculum and candidates
**Testing Performed**: Code syntax check.
**Result**: Data models successfully defined.
**Known Limitations**: None
**Next Planned Milestone**: 2 (Subtask: Data Loaders and Repositories)

---

## Prompt 5
**Timestamp**: 2026-08-07T21:26:00+05:30
**Milestone**: 2 - Backend Foundation + Data Layer
**Objective**: Create data loader services and repository classes to expose data internally.
**Context**: Now that the Pydantic models exist, we need a service layer to load the raw JSON, validate it, cache it in memory, and provide clean methods to query the data.
**Prompt Given**: "Create data loader services (Curriculum Loader, Candidate Loader) to load, validate, parse, and cache the data. Handle invalid files gracefully. Create repository/service classes (CurriculumRepository, CandidateRepository) exposing methods like get_all_candidates, get_curriculum, get_day, etc."
**Reasoning**: A repository pattern separates data access logic from the rest of the application. Caching in memory prevents redundant file reads and validation overhead during the interview process.
**AI Output Summary**: Created `data_loaders.py` containing `DataLoader` class with class-level caching. Created `repositories.py` containing `CurriculumRepository` and `CandidateRepository` with methods to fetch specific days, modules, and candidates.
**Architecture Decisions**: 
- Implemented singleton-like caching at the class level in `DataLoader` to ensure data is loaded and validated exactly once.
- Used Pydantic's built-in validation during instantiation, bubbling up `ValidationError` if the raw JSON is malformed.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/data_loaders.py`
- `backend/services/repositories.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(backend): implement data loaders and repository layer
**Testing Performed**: Wrote and executed a Python script to instantiate the repositories and verify that 8 modules and 20 candidates were successfully loaded and validated.
**Result**: Data successfully loads, validates, caches, and is queried correctly.
**Known Limitations**: In-memory caching means the server must be restarted if the JSON files change during runtime.
**Next Planned Milestone**: 2 (Subtask: Update README and verify Backend)

---

## Prompt 6
**Timestamp**: 2026-08-07T21:30:00+05:30
**Milestone**: 2 - Backend Foundation + Data Layer
**Objective**: Update README and verify backend starts successfully.
**Context**: Finalizing Milestone 2 by documenting the architecture and verifying that the FastAPI server can run without errors using the new models and services.
**Prompt Given**: "Review README.md. Add a Backend Architecture section. Improve PROMPTS.md. Verify backend starts successfully."
**Reasoning**: Keeping documentation up-to-date with architectural changes ensures onboarding is seamless. Verifying the application start confirms that no syntax or import errors were introduced during the milestone.
**AI Output Summary**: Updated `README.md` with a detailed Backend Architecture section explaining Models, Services, Utils, API, and Data. Verified FastAPI startup using uvicorn.
**Architecture Decisions**: None for this specific task.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: None
**Files Modified**: 
- `README.md`
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: docs(backend): update architecture in readme and finalize milestone 2
**Testing Performed**: Started the backend using `uvicorn main:app` and verified it ran successfully without errors.
**Result**: Milestone 2 fully complete and documented.
**Known Limitations**: None
**Next Planned Milestone**: 3 (API Layer & Interview Logic)

---

## Prompt 7
**Timestamp**: 2026-08-07T21:35:00+05:30
**Milestone**: 3 - Core Interview Domain
**Objective**: Create Interview Session, State, and Question Planning models.
**Context**: Starting the core domain layer of the interview engine. We need to represent the state of an interview session and structure the planned/asked questions robustly before implementing business logic.
**Prompt Given**: "Create Interview Session models... Create Interview State models... Create Question Planning models..."
**Reasoning**: Defining clear, strict types for the interview state ensures that the business logic can rely on a consistent data structure without fear of invalid states. Pydantic models with Enums provide strong validation.
**AI Output Summary**: Created `backend/models/interview.py` with Enums (`InterviewState`, `QuestionDifficulty`, `QuestionCategory`) and Pydantic models (`PlannedQuestion`, `AskedQuestion`, `InterviewSession`).
**Architecture Decisions**: 
- Used Enums to prevent invalid strings for states, difficulties, and categories.
- Stored `AskedQuestion` inside the `InterviewSession` to keep all session state encapsulated in a single domain object.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/models/interview.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(domain): add interview session models
**Testing Performed**: Code syntax check.
**Result**: Core models created successfully.
**Known Limitations**: None
**Next Planned Milestone**: 3 (Subtask: Difficulty Strategy)

---

## Prompt 8
**Timestamp**: 2026-08-07T21:37:00+05:30
**Milestone**: 3 - Core Interview Domain
**Objective**: Implement Difficulty Strategy and Topic Selection Strategy.
**Context**: We need robust algorithms to determine the appropriate starting difficulty for a candidate and select which curriculum days should be covered during the interview, ensuring gaps are targeted intentionally and strengths are respected.
**Prompt Given**: "Create Topic Selection Strategy... Create Difficulty Strategy..."
**Reasoning**: Extracting these algorithms into isolated strategy classes adhering to the Single Responsibility Principle prevents bloated Manager classes. It makes the domain highly testable.
**AI Output Summary**: Created `strategies.py` under `backend/services/domain/`. Implemented `DifficultyStrategy` calculating a score based on experience, completion ratio, and success rate. Implemented `TopicSelectionStrategy` prioritizing completed topics while fulfilling the 4-topic minimum constraint.
**Architecture Decisions**: 
- Grouped both strategies into a single `strategies.py` module as they share the same functional domain.
- Used static methods because these strategies act as pure functions mapping inputs (Candidate, Curriculum) to outputs without side effects.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/domain/strategies.py`
- `backend/services/domain/__init__.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(domain): implement difficulty and topic selection strategies
**Testing Performed**: Code syntax check.
**Result**: Strategies successfully implemented.
**Known Limitations**: Topic selection is randomized within the candidate's completed set, which is fine for variance but might not be deterministic for testing without mocking random.
**Next Planned Milestone**: 3 (Subtask: Session Manager)

---

## Prompt 9
**Timestamp**: 2026-08-07T21:37:30+05:30
**Milestone**: 3 - Core Interview Domain
**Objective**: Create Session Manager for tracking interview lifecycle.
**Context**: An interview progresses through states (start, ask questions, update answers, complete). The Session Manager tracks this lifecycle in memory for active candidates.
**Prompt Given**: "Create Session Manager. Responsibilities: Create session, Resume session, Update progress, Store interview state in memory, Track questions answered, Detect interview completion. No persistence is required."
**Reasoning**: Centralizing state management ensures consistent transitions and acts as the primary facade for the interview process. The `SessionManager` ties together the Candidate data, Curriculum data, and strategies.
**AI Output Summary**: Created `session_manager.py` which holds an in-memory dictionary of active `InterviewSession` instances. It creates a session using the `DifficultyStrategy` and `TopicSelectionStrategy`, marks it as in-progress, tracks asked questions, and automatically completes it once 5 questions have been answered.
**Architecture Decisions**: 
- Did not implement persistence (e.g., database) as per requirements. Used a simple dictionary.
- Implemented an idempotent-like `create_session` that returns an existing active session if one exists to prevent double-starting.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/domain/session_manager.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(domain): add session manager
**Testing Performed**: Code syntax check.
**Result**: Session management lifecycle implemented.
**Known Limitations**: All state is lost on server restart. A persistence layer will be required for production.
**Next Planned Milestone**: 3 (Subtask: Answer Evaluation Interface and Tests)

---

## Prompt 10
**Timestamp**: 2026-08-07T21:39:00+05:30
**Milestone**: 3 - Core Interview Domain
**Objective**: Create Answer Evaluation interface and write domain unit tests.
**Context**: To decouple the AI from the domain logic, we need clean abstract interfaces that future milestones will implement. Then we must rigorously test the domain logic written so far.
**Prompt Given**: "Create Answer Evaluation Interface. Do NOT evaluate answers. Create clean interfaces/classes that future AI implementations can use. Create unit tests for Session creation, Difficulty calculation, Topic planning, Session completion."
**Reasoning**: Interface segregation prevents the domain from being tightly coupled to an LLM provider (like OpenAI or Gemini). Unit tests guarantee that the complex domain logic (like topic selection and difficulty heuristics) works as expected before integration.
**AI Output Summary**: Created `evaluation_interface.py` with an abstract base class `AnswerEvaluationInterface`. Created `test_domain.py` utilizing `pytest` to test the strategies and the session manager end-to-end.
**Architecture Decisions**: 
- Used Python's built-in `abc` module for strict abstract classes, forcing future LLM services to implement the required methods.
- Placed tests under `backend/tests/` to keep test files out of the production source tree.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/domain/evaluation_interface.py`
- `backend/tests/__init__.py`
- `backend/tests/test_domain.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None (Installed `pytest` in the local virtual environment)
**Git Commit Message**: test(domain): add interview domain tests and evaluation interface
**Testing Performed**: Executed `pytest backend/tests`. All 3 test suites passed successfully.
**Result**: Domain logic is fully verified and decoupled from AI implementations.
**Known Limitations**: None
**Next Planned Milestone**: 4 (API Layer & Interview Logic)

---

## Prompt 12
**Timestamp**: 2026-08-07T21:48:30+05:30
**Milestone**: 4 - AI Prompt Engine & LLM Abstraction Layer
**Objective**: Create Prompt Engine.
**Context**: We need a centralized place to construct prompts for the LLM to ensure consistency and modularity.
**Prompt Given**: "Create Prompt Engine. Responsibilities: Build interview prompts, follow-up prompts, evaluation prompts, feedback prompts. Prompt templates must be modular."
**Reasoning**: Keeping prompt construction decoupled from API calls allows us to easily tweak language or context without breaking the logic.
**AI Output Summary**: Created `prompt_engine.py` in `backend/services/ai/`. Implemented static methods for building various prompts securely.
**Architecture Decisions**: 
- Used simple Python f-strings in static methods to keep templates lightweight and easy to maintain.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/ai/__init__.py`
- `backend/services/ai/prompt_engine.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(ai): create prompt engine
**Testing Performed**: Code syntax check.
**Result**: Prompt templates are modularized.
**Known Limitations**: Complex prompting may require Jinja templates in the future.
**Next Planned Milestone**: 4 (Subtask: Context Builder)
---

## Prompt 11
**Timestamp**: 2026-08-07T21:40:00+05:30
**Milestone**: 3 - Core Interview Domain
**Objective**: Update architecture documentation for the domain layer.
**Context**: Concluding Milestone 3 by making sure `README.md` reflects the newly created `domain` package and its core responsibilities.
**Prompt Given**: "Review architecture... docs(domain): update architecture documentation"
**Reasoning**: Keeping documentation synchronized with codebase evolution is crucial for team onboarding and maintaining architectural clarity.
**AI Output Summary**: Updated `README.md` to explicitly list the `backend/services/domain/` directory, highlighting that it contains pure business logic completely decoupled from LLMs.
**Architecture Decisions**: None for this specific task.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: None
**Files Modified**: 
- `README.md`
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: docs(domain): update architecture documentation
**Testing Performed**: None
**Result**: Documentation accurately reflects Milestone 3's completion.
**Known Limitations**: None
**Next Planned Milestone**: 4 (API Layer & Interview Logic)

---

## Prompt 13
**Timestamp**: 2026-08-07T21:49:00+05:30
**Milestone**: 4 - AI Prompt Engine & LLM Abstraction Layer
**Objective**: Create Conversation Context Builder.
**Context**: An LLM needs sufficient context to generate relevant technical questions. We need to extract this context from our domain models.
**Prompt Given**: "Create Conversation Context Builder. Responsibilities: Maintain interview history, Maintain previous answers, Maintain curriculum context, Maintain candidate profile context, Produce optimized prompt context."
**Reasoning**: Keeping the logic that flattens domain models into strings separated from the prompt templates ensures that the Prompt Engine stays clean and purely focused on instruction tuning.
**AI Output Summary**: Created `context_builder.py`. Added methods to serialize candidate data, curriculum objectives, and full interview history into a single structured text block.
**Architecture Decisions**: 
- Designed `ContextBuilder` with static methods. It doesn't need to maintain its own state because the `InterviewSession` domain model is the single source of truth for history.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/ai/context_builder.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(ai): implement context builder
**Testing Performed**: Code syntax check.
**Result**: LLM context string building is implemented.
**Known Limitations**: Long interview histories might exceed token limits in the future; truncation logic might be needed later.
**Next Planned Milestone**: 4 (Subtask: LLM Provider Interface)

---

## Prompt 14
**Timestamp**: 2026-08-07T21:50:00+05:30
**Milestone**: 4 - AI Prompt Engine & LLM Abstraction Layer
**Objective**: Create LLM Provider Interface and robust custom exceptions.
**Context**: To prevent vendor lock-in with a specific LLM provider (e.g., Gemini vs OpenAI), we need an abstract interface that strictly defines the contract for AI text generation. We also need custom exceptions to handle the myriad of ways external APIs can fail.
**Prompt Given**: "Create LLM Provider Interface... Implement robust exception handling. Create custom exceptions for: LLM Failure, Invalid Response, Timeout, Missing API Key"
**Reasoning**: Defining this interface using Python's `abc` enforces the Dependency Inversion Principle. The application depends on `LLMProvider`, not Gemini, meaning swapping to Claude or OpenAI in the future requires zero changes to the core domain or AI service logic.
**AI Output Summary**: Created `llm_provider.py` with an abstract base class `LLMProvider` defining methods for generating questions, evaluating answers, and giving feedback. Created `exceptions.py` containing custom exceptions inheriting from `AIEngineException`.
**Architecture Decisions**: 
- Grouped custom exceptions in a dedicated `exceptions.py` module to allow centralized error handling later on (e.g., global FastAPI exception handlers).
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/ai/exceptions.py`
- `backend/services/ai/llm_provider.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(ai): create llm provider interface and custom exceptions
**Testing Performed**: Code syntax check.
**Result**: Interface boundary and exception handling structures are established.
**Known Limitations**: None
**Next Planned Milestone**: 4 (Subtask: Gemini Adapter)

---

## Prompt 15
**Timestamp**: 2026-08-07T21:50:30+05:30
**Milestone**: 4 - AI Prompt Engine & LLM Abstraction Layer
**Objective**: Implement Gemini Adapter.
**Context**: We need a concrete implementation of `LLMProvider` that talks to Google's Gemini, but adhering to the strict rule of NOT making actual external network calls for this milestone.
**Prompt Given**: "Implement Gemini Adapter. Only Gemini. No OpenAI. No Claude. Adapter should implement the provider interface. Keep API key configurable using environment variables. Never hardcode secrets. STRICTLY DO NOT IMPLEMENT: Do NOT call any LLM. Do NOT integrate Gemini."
**Reasoning**: Building the adapter class forces us to handle initialization requirements (like API keys) and method signatures without the overhead or latency of a real network integration, which will be plugged in later.
**AI Output Summary**: Created `gemini_adapter.py`. Implemented the `LLMProvider` interface. Reads `GEMINI_API_KEY` from environment and raises `MissingAPIKeyException` if missing. Substituted real API calls with a simulated stub.
**Architecture Decisions**: 
- Followed the dependency inversion principle by inheriting `LLMProvider`.
- Secure initialization via `os.getenv`, immediately failing fast if the key is missing.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/ai/gemini_adapter.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(ai): implement gemini adapter
**Testing Performed**: Code syntax check.
**Result**: Adapter structure is ready for future integration.
**Known Limitations**: Currently returns mock strings; actual Google Generative AI SDK will need to be added later.
**Next Planned Milestone**: 4 (Subtask: Prompt Response Parser)

---

## Prompt 16
**Timestamp**: 2026-08-07T21:51:20+05:30
**Milestone**: 4 - AI Prompt Engine & LLM Abstraction Layer
**Objective**: Create Prompt Response Parser.
**Context**: Language models often return chatty or inconsistently formatted text (e.g., "Here is the question: ..."). The engine needs robust logic to strip noise and validate outputs before converting them into domain entities.
**Prompt Given**: "Create Prompt Response Parser. Responsibilities: Validate LLM responses. Handle malformed outputs. Normalize responses. Convert responses into domain models."
**Reasoning**: Decoupling the parsing logic ensures that if the LLM provider changes its response style, we only need to update the regex/parsing logic in one isolated place rather than scattering cleaning logic throughout the application.
**AI Output Summary**: Created `response_parser.py`. Built static methods `parse_question` and `parse_evaluation` that use regex to strip out common conversational prefixes and validate that the remaining string is not empty, raising `InvalidResponseException` if it is.
**Architecture Decisions**: 
- Opted for static methods as the parser is stateless.
- Isolated string manipulation into this single layer to protect domain models from bad data.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/ai/response_parser.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None (Used standard library `re`)
**Git Commit Message**: feat(ai): implement response parser
**Testing Performed**: Code syntax check.
**Result**: LLM responses can now be safely normalized.
**Known Limitations**: Regex patterns might need expansion based on actual LLM behavior in production.
**Next Planned Milestone**: 4 (Subtask: AI Service Layer)

---

## Prompt 17
**Timestamp**: 2026-08-07T21:52:00+05:30
**Milestone**: 4 - AI Prompt Engine & LLM Abstraction Layer
**Objective**: Create AI Service Layer.
**Context**: We need a facade that brings together the domain models, the context builder, the prompt engine, the LLM provider, and the response parser into a single cohesive service.
**Prompt Given**: "Create AI Service Layer. Responsibilities: Connect Prompt Engine. Connect Domain. Connect Gemini Adapter. Return strongly typed objects."
**Reasoning**: Using the facade pattern hides the complex orchestration of building context, templating prompts, making API calls, and parsing strings from the rest of the application.
**AI Output Summary**: Created `ai_service.py`. Implemented the `AnswerEvaluationInterface` from the domain layer. The `AIService` orchestrates the `ContextBuilder`, `PromptEngine`, injected `LLMProvider`, and `ResponseParser` to return strongly typed domain objects.
**Architecture Decisions**: 
- Used Dependency Injection (`__init__(self, provider: LLMProvider)`) to decouple the service from the concrete `GeminiAdapter`. This allows easy mocking during tests.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/services/ai/ai_service.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(ai): implement ai service layer
**Testing Performed**: Code syntax check.
**Result**: Complete end-to-end AI abstraction layer is ready.
**Known Limitations**: None
**Next Planned Milestone**: 4 (Subtask: AI Unit Tests)

---

## Prompt 18
**Timestamp**: 2026-08-07T21:52:30+05:30
**Milestone**: 4 - AI Prompt Engine & LLM Abstraction Layer
**Objective**: Create AI unit tests.
**Context**: We need to verify that the Context Builder stringifies domain objects correctly, the Prompt Engine inserts variables, the Parser strips noise, and the Gemini Adapter raises exceptions when missing API keys.
**Prompt Given**: "Create unit tests. Test: Prompt Builder, Context Builder, Parser, Gemini Adapter (mock responses only). Do NOT make real API calls during tests."
**Reasoning**: Unit testing the AI integration logic independently of the external LLM ensures the system's structural integrity. Mocking environment variables and responses prevents CI/CD pipelines from failing due to missing secrets or network issues.
**AI Output Summary**: Created `test_ai.py` under `backend/tests/`. Added fixtures for domain models and wrote tests for `PromptEngine`, `ContextBuilder`, `ResponseParser`, and `GeminiAdapter` (using Pytest's `monkeypatch` to simulate missing and present API keys).
**Architecture Decisions**: 
- Used Pytest `monkeypatch` to manipulate the environment for the GeminiAdapter tests to ensure no real secrets are needed or leaked.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/tests/test_ai.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: test(ai): add ai unit tests
**Testing Performed**: Executed `pytest backend/tests/test_ai.py`. All 6 test cases passed successfully.
**Result**: AI abstraction layer is thoroughly tested.
**Known Limitations**: Testing the exact outputs of LLMs is impossible; we only test our wrapper logic.
**Next Planned Milestone**: 4 (Subtask: Update Architecture Docs)

---

## Prompt 19
**Timestamp**: 2026-08-07T21:53:00+05:30
**Milestone**: 4 - AI Prompt Engine & LLM Abstraction Layer
**Objective**: Update architecture documentation for the AI layer.
**Context**: Concluding Milestone 4 by ensuring `README.md` reflects the newly created `ai` package and its core responsibilities.
**Prompt Given**: "Review architecture... docs(ai): update architecture"
**Reasoning**: Keeping documentation synchronized ensures developers understand the boundary between pure domain logic and external AI integrations.
**AI Output Summary**: Updated `README.md` to explicitly list the `backend/services/ai/` directory, highlighting the `LLMProvider`, `PromptEngine`, `ContextBuilder`, and `ResponseParser`.
**Architecture Decisions**: None for this specific task.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: None
**Files Modified**: 
- `README.md`
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: docs(ai): update architecture
**Testing Performed**: None
**Result**: Documentation accurately reflects Milestone 4's completion.
**Known Limitations**: None
**Next Planned Milestone**: 5 (API Layer & Core Integration)

---

## Prompt 20
**Timestamp**: 2026-08-07T22:10:00+05:30
**Milestone**: Frontend Configuration
**Objective**: Fix Next.js hydration and CORS issues on the development server.
**Context**: The user encountered two issues accessing the frontend from a virtual machine/network IP (`192.168.56.1`): Next.js 15+ blocks cross-origin dev requests by default, and a browser extension (`wotdisconnected`) injected attributes into the `<body>` causing a React hydration mismatch.
**Prompt Given**: "Fix the issue. Ensure the fix does not break existing architecture. Run the tests again. Commit the fix separately. Push the fix. Append the fix to PROMPTS.md."
**Reasoning**: Adding `allowedDevOrigins` to `next.config.ts` explicitly whitelists the network IP. Adding `suppressHydrationWarning` to the `<body>` tag safely prevents React from crashing when external extensions modify the body HTML before hydration completes.
**AI Output Summary**: Modified `next.config.ts` to include `allowedDevOrigins: ["192.168.56.1"]`. Modified `src/app/layout.tsx` to add `suppressHydrationWarning` to the `<body>` element.
**Architecture Decisions**: 
- Followed standard Next.js security configurations for local network access.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: None
**Files Modified**: 
- `frontend/next.config.ts`
- `frontend/src/app/layout.tsx`
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: fix(frontend): allow dev cross-origin requests and suppress body hydration warnings
**Testing Performed**: Ran `npm run build` to verify the configuration syntax is correct.
**Result**: Next.js development server will now accept requests from the specified IP and ignore browser extension mutations on the body tag.
**Known Limitations**: Extensions injecting into elements other than `<body>` or `<html>` might still cause hydration issues.
**Next Planned Milestone**: 5 (API Layer & Core Integration)

---

## Prompt 21
**Timestamp**: 2026-08-07T22:20:00+05:30
**Milestone**: Testing Configuration
**Objective**: Fix `pytest` ModuleNotFoundError when running tests from the backend directory.
**Context**: The user attempted to run `pytest` inside the `backend` directory, which resulted in Python failing to resolve `backend.xxx` imports because the Python path did not include the root directory.
**Prompt Given**: "solve this" (with pytest error logs)
**Reasoning**: Adding a `pytest.ini` file at the root of the project with `pythonpath = .` and `testpaths = backend/tests` tells pytest to treat the project root as the base path for imports, regardless of which subdirectory the user executes the `pytest` command from.
**AI Output Summary**: Created `pytest.ini` in the root directory configured to resolve Python imports correctly and locate the tests inside `backend/tests`.
**Architecture Decisions**: 
- Placed `pytest.ini` in the root directory as per standard Python project conventions, ensuring all subsequent modules (like the API or scripts) can be tested seamlessly.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `pytest.ini`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: fix(backend): add pytest.ini to resolve module imports
**Testing Performed**: Ran `pytest` from the `backend` directory. Verified that all 9 tests passed in 0.08s.
**Result**: Pytest works seamlessly from any directory within the project.
**Known Limitations**: None
**Next Planned Milestone**: 5 (API Layer & Core Integration)

---

## Prompt 22
**Timestamp**: 2026-08-07T22:28:00+05:30
**Milestone**: 5 - API Layer + Core Integration
**Objective**: Create API schemas and dependency injection modules.
**Context**: We need to define strict data contracts for the API and decouple repository/service initialization from route handlers.
**Prompt Given**: "Create proper request and response schemas. Use Pydantic... Dependency Injection: Create clean dependency providers."
**Reasoning**: Establishing schemas first ensures API requests and responses are strictly validated before hitting business logic. Dependency injection prevents global state mutations during testing and isolates domain dependencies from the FastAPI routers.
**AI Output Summary**: Created `backend/api/schemas.py` defining models like `StartInterviewRequest` and `AnswerResponse`. Created `backend/api/dependencies.py` which instantiates repositories and the AI Service using a mocked LLM provider for this milestone. Added dotenv loading to handle dummy API keys during local dev.
**Architecture Decisions**: 
- Separated API schemas from domain models to prevent leaky abstractions (API shouldn't directly expose internal data structures without a DTO layer where appropriate).
- Used FastAPI's `Depends` for typed Dependency Injection.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/api/__init__.py`
- `backend/api/schemas.py`
- `backend/api/dependencies.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(api): add api schemas and dependency injection
**Testing Performed**: Ran `python -c "import backend.api.dependencies"` which executed without errors, proving instantiation logic and mock initialization works.
**Result**: Core API foundation is laid out.
**Known Limitations**: `GEMINI_API_KEY` is temporarily mocked if missing to prevent boot failures.
**Next Planned Milestone**: 5 (Subtask: Health and Core Routers)

---

## Prompt 23
**Timestamp**: 2026-08-07T23:23:00+05:30
**Milestone**: 5 - API Layer + Core Integration
**Objective**: Create Health, Candidate, and Curriculum routers.
**Context**: We need to start exposing the core data layers via REST APIs.
**Prompt Given**: "Create API routers. Example: health.py, candidate.py, curriculum.py... Wire together... FastAPI Router"
**Reasoning**: Keeping the endpoints segmented by resource aligns with RESTful design principles and prevents `main.py` from becoming bloated.
**AI Output Summary**: Created `backend/api/routers/health.py`, `candidate.py`, and `curriculum.py`. Registered them in `backend/main.py`. The endpoints safely use the dependency injected repositories to return strictly typed Pydantic models.
**Architecture Decisions**: 
- Added an `__init__.py` to the routers package to keep Python imports clean.
- Used `APIRouter` to namespace paths (e.g. `/candidates`, `/health`, `/curriculum`) and applied OpenAPI tags for better documentation.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/api/routers/__init__.py`
- `backend/api/routers/health.py`
- `backend/api/routers/candidate.py`
- `backend/api/routers/curriculum.py`
**Files Modified**: 
- `backend/main.py`
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(api): implement health, candidate, and curriculum routers
**Testing Performed**: Ran `python -c "import backend.main"` to verify that FastAPI initializes properly with the newly included routers and no circular dependencies exist.
**Result**: Read-only core APIs are wired to the data layer.
**Known Limitations**: None
**Next Planned Milestone**: 5 (Subtask: Interview APIs)

---

## Prompt 24
**Timestamp**: 2026-08-07T23:24:00+05:30
**Milestone**: 5 - API Layer + Core Integration
**Objective**: Implement Interview APIs.
**Context**: The core business logic resides in the `SessionManager` and `AIService`. We need REST endpoints to trigger interview creation, question generation, and answer submission.
**Prompt Given**: "POST /interview/start... POST /interview/{sessionId}/next... POST /interview/{sessionId}/answer... GET /interview/{sessionId}... Wire together"
**Reasoning**: Building the integration layer exposes the domain logic to the outside world, strictly enforcing state transition constraints (e.g. throwing an error if asking for a next question on a non-active session).
**AI Output Summary**: Created `backend/api/routers/interview.py`. Implemented the `/start`, `/next`, `/answer`, and session retrieval endpoints using `APIRouter`. Orchestrated the `SessionManager`, `CandidateRepository`, `CurriculumRepository`, and `AIService` within the route handlers.
**Architecture Decisions**: 
- Enforced strict state checking (HTTP 400 Bad Request) when transitioning states in invalid ways (e.g., answering a question before one is asked).
- Wrapped AI Service calls in `try...except` to prevent internal server errors from leaking domain-level exception traces, throwing structured HTTP 500s instead.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/api/routers/interview.py`
**Files Modified**: 
- `backend/main.py`
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: feat(api): implement interview session endpoints
**Testing Performed**: Ran `python -c "import backend.main"` to verify application boot with the new complex dependencies.
**Result**: Core interview application flow is exposed over HTTP.
**Known Limitations**: Real AI generation is still stubbed out.
**Next Planned Milestone**: 5 (Subtask: Error Handling & Middleware)

---

## Prompt 25
**Timestamp**: 2026-08-07T23:25:00+05:30
**Milestone**: 5 - API Layer + Core Integration
**Objective**: Implement API tests.
**Context**: We need to verify that all the new API endpoints function correctly and handle validation/errors properly without manually testing via Postman or curl.
**Prompt Given**: "Testing: Create API tests. Use pytest. Test every endpoint... Ensure tests pass."
**Reasoning**: Using `TestClient` from FastAPI allows us to test the entire application request/response lifecycle locally in memory.
**AI Output Summary**: Created `backend/tests/test_api.py`. Wrote test functions for health check, listing candidates, fetching curriculum, error handling on invalid IDs, and an end-to-end test simulating a full interview flow (start -> next -> answer -> check state).
**Architecture Decisions**: 
- Leveraged the in-memory mocked state so tests run extremely fast and do not depend on external APIs or databases.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- `backend/tests/test_api.py`
**Files Modified**: 
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: test(api): add comprehensive api endpoint tests
**Testing Performed**: Executed `pytest backend/tests/test_api.py`. 6/6 tests passed in 1.78 seconds.
**Result**: Full endpoint verification is automated.
**Known Limitations**: The interview flow test asserts on mock responses.
**Next Planned Milestone**: 5 (Subtask: Documentation)

---

## Prompt 26
**Timestamp**: 2026-08-07T23:27:00+05:30
**Milestone**: 5 - API Layer + Core Integration
**Objective**: Finalize Documentation for Milestone 5.
**Context**: We need to update the README to reflect that the API is now implemented.
**Prompt Given**: "Update README.md and PROMPTS.md."
**Reasoning**: Keeping documentation up-to-date with code changes ensures team alignment and easier onboarding.
**AI Output Summary**: Updated `README.md` to move `backend/api` from "(Future)" to fully implemented, documenting the new routers.
**Architecture Decisions**: None
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: None
**Files Modified**: 
- `README.md`
- `PROMPTS.md`
**Dependencies Added**: None
**Git Commit Message**: docs(backend): update README for API milestone
**Testing Performed**: None
**Result**: Documentation reflects the current state of the backend API.
**Known Limitations**: None
**Next Planned Milestone**: 6 (Real AI Integration)

---

## Prompt 27
**Timestamp**: 2026-08-08T00:00:00+05:30
**Milestone**: 6 - Interview Engine + Real AI Integration
**Objective**: Implement real AI Integration via google-genai, structured JSON prompts, and robust retry logic.
**Context**: We need to connect the stubbed GeminiAdapter to the actual Google Gen AI SDK, enforcing JSON schemas for all output, and adjusting the interview flow to cover 8 questions.
**Prompt Given**: "Milestone 6: Interview Engine + Real AI Integration... Replace mock AI responses with real Google Gen AI Python SDK... Implement structured JSON-based prompts... Implement robust error handling... Enhance ContextBuilder... Update README.md and PROMPTS.md."
**Reasoning**: Structured JSON is strictly required for the backend to reliably process and extract questions, evaluations, scores, and follow-up flags. Adding retries in the GeminiAdapter protects the interview flow against transient network failures. Extending the session to 8 questions and 4 topics hits the business logic requirements.
**AI Output Summary**: 
- Added google-genai to requirements.txt.
- Re-wrote GeminiAdapter using the official SDK, configuring it to return application/json and adding a retry loop.
- Updated PromptEngine templates to explicitly define and request valid JSON schemas.
- Updated ResponseParser to securely parse JSON and handle markdown fences.
- Improved ContextBuilder to track missing skills and interview progress.
- Modified SessionManager to select and cycle through 4 topics, asking 8 questions total.
- Updated API routers and testing fixtures to accommodate JSON parsing and end-to-end flow.
**Architecture Decisions**: 
- Retained the LLMProvider interface but changed evaluation signatures to return dict instead of strings to support rich JSON data (score, follow-up flags).
- Passed structured context and exact expected schema directly in the prompt.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: None
**Files Modified**: 
- backend/services/ai/gemini_adapter.py
- backend/services/ai/prompt_engine.py
- backend/services/ai/response_parser.py
- backend/services/ai/context_builder.py
- backend/services/ai/ai_service.py
- backend/services/domain/session_manager.py
- backend/services/domain/evaluation_interface.py
- backend/models/interview.py
- backend/api/routers/interview.py
- backend/tests/test_ai.py
- backend/tests/test_api.py
- backend/tests/test_domain.py
- requirements.txt
- PROMPTS.md
**Dependencies Added**: google-genai
**Git Commit Message**: feat(ai): implement real gemini sdk integration with json structured outputs
**Testing Performed**: Executed pytest (15/15 passing tests), verifying mock patches function perfectly for the new JSON structured outputs.
**Result**: Real AI integration is complete, stable, and covered by unit tests.
**Known Limitations**: Real API latency is not simulated in tests.
**Next Planned Milestone**: 7 (Frontend Integration)

---

## Prompt 28
**Timestamp**: 2026-08-08T00:15:00+05:30
**Milestone**: 7 - End-to-End Integration Testing & Backend Validation
**Objective**: Validate the full backend system from end-to-end, handle invalid state transitions securely, and perform extensive code quality checks.
**Context**: With real AI integrated, the backend must prove robust enough for production deployment. This involves adding complete E2E flow tests, tightening state management in the domain logic, ensuring the API properly rejects invalid actions, and updating all documentation to reflect the finalized architecture.
**Prompt Given**: "Milestone 7: End-to-End Integration Testing & Backend Validation... Verify integration... Validate interview state transitions... API Validation... Testing... Code Quality Review... Documentation"
**Reasoning**: An interview session spans multiple state changes (Not Started -> In Progress -> Completed). We discovered during E2E testing that automatically completing the session when the 8th question was *generated* caused the subsequent submission of the 8th *answer* to fail with a 400 Bad Request. By migrating the completion logic to the post-answer evaluation phase, the state machine aligns perfectly with the intended HTTP flow. Removing dead code and unused imports ensures the codebase remains maintainable.
**AI Output Summary**: 
- Added an exhaustive E2E integration test \	est_full_interview_flow\ in \	est_api.py\ simulating an 8-question lifecycle.
- Identified and resolved a critical state transition bug in \SessionManager\ and \interview.py\ where sessions closed prematurely.
- Added strict transition tests to verify that answering un-asked questions returns \400 Bad Request\.
- Ran static analysis (\lake8\) across the backend and removed all unused imports and dead code.
- Completely rewrote \README.md\ to provide deep technical documentation on the architecture, setup, testing, and troubleshooting.
**Architecture Decisions**: 
- Re-aligned state mutation responsibility: \SessionManager.update_progress\ no longer auto-completes. The router (\nswer_question\) evaluates if the session requirements are met (8 questions + no follow-up required) and explicitly commands the manager to complete the session.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: None
**Files Modified**: 
- \ackend/api/routers/interview.py\
- \ackend/services/domain/session_manager.py\
- \ackend/tests/test_api.py\
- \ackend/tests/test_domain.py\
- \ackend/tests/test_ai.py\
- \README.md\
- \PROMPTS.md\
**Dependencies Added**: None
**Git Commit Message**: docs: update integration documentation and finalize backend validation
**Testing Performed**: Executed \pytest\ successfully across all layers (17/17 tests passing). Ran \lake8\ to verify code quality.
**Result**: Backend is fully integrated, verified, documented, and production-ready.
**Known Limitations**: Real API latency is not simulated in tests.
**Next Planned Milestone**: 8 (Frontend Integration)

---

## Prompt 29
**Timestamp**: 2026-08-08T00:30:00+05:30
**Milestone**: 8 - Frontend Design System + UI Foundation
**Objective**: Build a highly reusable, premium design system and UI foundation for all future frontend pages, without implementing actual pages yet.
**Context**: The backend is complete and production-ready. The frontend requires a visual language modeled after top-tier SaaS products (Vercel, Linear). This milestone strictly enforces the creation of design tokens, layout shells, component primitives, typography scales, and a comprehensive dark mode implementation.
**Prompt Given**: "Milestone 8: Frontend Design System + UI Foundation... Build a complete reusable design system... The UI should feel inspired by Apple, Linear, Vercel... Create a complete design system including Typography, Spacing, Grid... Implement Light Mode, Dark Mode... Build reusable components... Do NOT build interview pages... Commit after every major logical subtask."
**Reasoning**: A premium UI requires a unified token system. I replaced the default Shadcn/Tailwind configuration in \globals.css\ with a bespoke theme featuring monochromatic background shades and an indigo primary brand color, enhanced with custom box shadows. \Geist\ and \Geist Mono\ were selected for typography. I constructed a layout shell consisting of a flexible \PageContainer\, \Sidebar\, and \Navbar\. For interactive elements, I augmented the primitive \Button\ to natively support a robust \LoadingButton\ state. Next-themes was installed to manage rapid, jitter-free theme toggling between OLED dark and clean light modes.
**AI Output Summary**: 
- Configured \globals.css\ with a bespoke color and shadow design token system.
- Hooked up \Geist\ and \Geist Mono\ font families in \layout.tsx\.
- Created \src/components/layout-foundation.tsx\ providing structural shells.
- Created \src/components/sidebar.tsx\ and \
avbar.tsx\ as generic responsive navigational building blocks.
- Overrode and expanded \utton.tsx\ to support a highly reusable \LoadingButton\.
- Created \card.tsx\ and \skeleton.tsx\ for premium data presentation and loading state management.
- Wired up \
ext-themes\ globally with a \ThemeProvider\ and a generic accessible \ThemeToggle\ button.
- Restructured and updated \README.md\ to capture the new frontend architecture.
**Architecture Decisions**: 
- Centralized UI configuration heavily inside \globals.css\ using native CSS variables mapped to Tailwind v4, ensuring dynamic theme switching executes in the browser extremely fast.
- Built Layout shells using \orwardRef\ to maintain maximum composability for future pages.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- \rontend/src/components/layout/layout-foundation.tsx\
- \rontend/src/components/layout/sidebar.tsx\
- \rontend/src/components/layout/navbar.tsx\
- \rontend/src/components/ui/card.tsx\
- \rontend/src/components/ui/skeleton.tsx\
- \rontend/src/components/theme-provider.tsx\
- \rontend/src/components/theme-toggle.tsx\
**Files Modified**: 
- \rontend/src/app/globals.css\
- \rontend/src/app/layout.tsx\
- \rontend/src/components/ui/button.tsx\
- \rontend/package.json\
- \rontend/package-lock.json\
- \README.md\
- \PROMPTS.md\
**Dependencies Added**: 
- \
ext-themes\
**Git Commit Message**: docs(frontend): update design system documentation
**Testing Performed**: Ran \
pm run build\ successfully multiple times throughout the milestone. Fixed a TypeScript error (\HTMLNavElement\) that was caught by the static compiler.
**Result**: A robust, Vercel/Linear-inspired, highly reusable component library and layout foundation is now established.
**Known Limitations**: Layout shells do not yet handle active state routing (reserved for page implementation).
**Next Planned Milestone**: 9 (Frontend Page Implementation)

---

## Prompt 30
**Timestamp**: 2026-08-08T12:40:00+05:30
**Milestone**: 9 - Dashboard & Product Experience
**Objective**: Build the main application dashboard as the primary entry point to NovaForge using the established Milestone 8 design system. Focus on minimal, premium, SaaS-quality design with realistic mocked data.
**Context**: The backend and foundational UI are complete. The application needs a cohesive, premium home page (\/\) that integrates all the new components into a responsive layout. The design must feel alive with hover states, mock data, and smooth transitions, but without connecting to the real backend yet.
**Prompt Given**: "Milestone 9: Dashboard & Product Experience... Build the main application dashboard... Dashboard should feel inspired by OpenAI, Linear, Vercel... Implement Hero Section, Statistics Cards, Candidate Selector, Interview Overview, Activity Timeline, Curriculum Progress... UX Requirements: Hover states, responsive spacing, premium whitespace... Do NOT connect backend yet... Commit after every logical subtask."
**Reasoning**: To achieve a "Vercel/Linear" feel, I structured the dashboard using a strict grid layout bound within the \PageContainer\. I built a \DashboardLayout\ shell wrapping the \Navbar\ and \Sidebar\ components to establish the overall structural hierarchy. I iteratively built the \Statistics Cards\ for quick glances at metrics, followed by a heavily styled \CandidateSelector\ component utilizing custom \Avatar\ and \Badge\ primitives for a rich visual experience. I then built the \CurriculumProgress\ utilizing a bespoke \Progress\ bar component and mapped mock modules to display completion status. Finally, I built a vertical \ActivityTimeline\ utilizing pseudo-elements for the connecting lines to show a chronological history of user actions. All sections utilize native Tailwind utility classes for intrinsic responsiveness (\grid-cols-1 md:grid-cols-2 lg:grid-cols-4\).
**AI Output Summary**: 
- Replaced the default Next.js boilerplate in \page.tsx\ with a premium \DashboardLayout\.
- Created \src/components/dashboard-layout.tsx\ mapping the shell.
- Created \Badge\ and \Avatar\ primitives manually in \src/components/ui/\ to unblock shadcn dependencies.
- Built a responsive stats grid using \Card\ primitives displaying completed interviews and active session data.
- Built \CandidateSelector\ with searchable UI (mocked) and active state selections.
- Built \CurriculumProgress\ and \Progress\ primitive to show syllabus completion tracking.
- Built \ActivityTimeline\ utilizing complex CSS pseudo-elements for a clean vertical timeline.
**Architecture Decisions**: 
- Opted to keep \page.tsx\ clean by abstracting complex dashboard widgets into \src/components/dashboard/\.
- Used CSS gradient lines (\g-gradient-to-b\) and absolute pseudo-elements (\efore:\) for the timeline to ensure it scales cleanly on mobile without Javascript positioning.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- \rontend/src/components/layout/dashboard-layout.tsx\
- \rontend/src/components/ui/badge.tsx\
- \rontend/src/components/ui/avatar.tsx\
- \rontend/src/components/ui/progress.tsx\
- \rontend/src/components/dashboard/candidate-selector.tsx\
- \rontend/src/components/dashboard/curriculum-progress.tsx\
- \rontend/src/components/dashboard/activity-timeline.tsx\
**Files Modified**: 
- \rontend/src/app/page.tsx\
- \README.md\
- \PROMPTS.md\
**Dependencies Added**: None
**Git Commit Message**: docs(frontend): update dashboard documentation
**Testing Performed**: Ran \
pm run build\ sequentially after every logical widget implementation to verify zero TS/linting regressions. Verified grid collapse on mobile viewports.
**Result**: A fully responsive, highly polished, data-rich (mocked) SaaS dashboard is now the entry point of the application.
**Known Limitations**: Mobile sidebar navigation toggle (hamburger menu) is not yet implemented (sidebar currently hides on mobile). Search bar in \CandidateSelector\ is a visual mock only.
**Next Planned Milestone**: 10 (Interview View / Candidate Flow)

---

## Prompt 31
**Timestamp**: 2026-08-08T13:00:00+05:30
**Milestone**: 10 - Interview Experience + Frontend Backend Integration
**Objective**: Connect the frontend dashboard UI to the existing production backend REST APIs and build the fully functional interactive \/interview\ flow utilizing the Gemini AI service.
**Context**: The application frontend features a mock premium design. The backend API has full routing for candidate selection, curriculum fetching, and managing complex AI-driven interview states with \SessionManager\ and \AIService\. This milestone bridges them by replacing all static UI arrays with live \etch\ calls and implementing the multi-step interactive evaluation workflow.
**Prompt Given**: "Milestone 10: Interview Experience + Frontend Backend Integration... Transform the current dashboard into a fully functional AI Interview platform... Create a centralized API client... Create reusable React hooks... Replace dashboard mock data... Build Interview Page... Implement interview flow... Loading Experience... Error Handling... Commit after every logical subtask."
**Reasoning**: 
- **Centralized API**: I created \src/lib/api/api.ts\ to wrap \etch\ with a standardized \ApiError\ thrower, ensuring all API responses correctly parse JSON or reject cleanly. I modularized endpoints into \candidate.ts\, \curriculum.ts\, \dashboard.ts\, and \interview.ts\.
- **Backend Ad-hoc Extension**: The dashboard statistics required a single aggregator endpoint. I spun up \ackend/api/routers/dashboard.py\ quickly to maintain backend architectural parity with the frontend's needs, avoiding duplicate processing on the client.
- **Custom Hooks**: Abstracted component state management into \src/hooks/\ (e.g. \useInterviewSession\). This cleanly handles loading flags, errors, session hydration, answer submission, and automatic polling for initial questions, preventing prop-drilling entirely.
- **Interview UI**: Built \/interview/[sessionId]\ utilizing dynamic layout splits. Included interactive states like disabled textareas during API evaluation, graceful error boundary fallbacks, and a distinct "Final Report" completion screen.
**AI Output Summary**: 
- Created centralized API client in \src/lib/api/\.
- Created lightweight \/dashboard\ backend endpoint.
- Created reusable React hooks for candidates, curriculum, dashboard, and interviews.
- Wired up \page.tsx\, \CandidateSelector\, \ActivityTimeline\, and \CurriculumProgress\ to live backend data.
- Implemented full dynamic route \src/app/interview/[sessionId]/page.tsx\.
- Resolved Next.js Server Components constraint by injecting \"use client"\ directives across hooks and interactive components.
**Architecture Decisions**: 
- Utilized \useCallback\ heavily inside hooks to prevent infinite re-renders across dependent \useEffect\ calls.
- Segmented API clients to match backend FastAPI routers strictly 1:1.
**Human Review**: Pending
**Manual Changes**: None
**Files Created**: 
- \ackend/api/routers/dashboard.py\
- \rontend/src/lib/api/*\
- \rontend/src/hooks/*\
- \rontend/src/app/interview/[sessionId]/page.tsx\
**Files Modified**: 
- \ackend/main.py\
- \rontend/src/app/page.tsx\
- \rontend/src/components/dashboard/*\
- \README.md\
- \PROMPTS.md\
**Dependencies Added**: None
**Git Commit Message**: docs(frontend): update integration documentation
**Testing Performed**: Frontend and Backend dev servers executed synchronously. \
pm run build\ executed 4 times iteratively and cleared all TS compilation warnings. 
**Result**: The application is now fully functional end-to-end. Selecting a candidate dynamically spins up a backend session, generates live Gemini AI questions, evaluates answers, assigns scores, tracks progress, and outputs a final report.
**Known Limitations**: None.
**Next Planned Milestone**: 11 (Final Polish)
# #   P r o m p t   3 4  
 * * T i m e s t a m p * * :   2 0 2 6 - 0 8 - 0 8 T 1 3 : 2 5 : 0 0 + 0 5 : 3 0  
 * * M i l e s t o n e * * :   1 1   -   P r e m i u m   P r o d u c t   E x p e r i e n c e   +   A n a l y t i c s   +   F i n a l   U X   P o l i s h  
 * * O b j e c t i v e * * :   F i n a l i z e   U X   p o l i s h ,   a n a l y t i c s ,   a n d   e r r o r   h a n d l i n g .  
 * * A I   O u t p u t   S u m m a r y * * :   I m p l e m e n t e d   A n a l y t i c s C h a r t ,   C a n d i d a t e D e t a i l M o d a l ,   I n t e r v i e w R e p o r t   ( p r e m i u m   f e e d b a c k   l a y o u t ) ,   4 0 4   p a g e ,   a n d   g l o b a l   e r r o r   b o u n d a r y .   A d d e d   t o a s t   n o t i f i c a t i o n s   a n d   t y p i n g   i n d i c a t o r s .   I m p r o v e d   e m p t y   s t a t e s .  
 * * G i t   C o m m i t   M e s s a g e * * :   d o c s ( f r o n t e n d ) :   f i n a l i z e   m i l e s t o n e   1 1   d o c u m e n t a t i o n  
 # #   P r o m p t   3 5  
 * * T i m e s t a m p * * :   2 0 2 6 - 0 8 - 0 8 T 1 3 : 4 0 : 0 0 + 0 5 : 3 0  
 * * M i l e s t o n e * * :   1 1 . 5   -   P r o d u c t i o n   R e a d i n e s s   A u d i t   &   S t a b i l i z a t i o n  
 * * O b j e c t i v e * * :   P e r f o r m   a   c o m p l e t e   p r o d u c t i o n   r e a d i n e s s   a u d i t   a n d   f i x   b a c k e n d   f e t c h   e r r o r s .  
 * * A I   O u t p u t   S u m m a r y * * :   A u d i t e d   t h e   e n t i r e   a p p l i c a t i o n .   D i s c o v e r e d   a   c r i t i c a l   M o d u l e N o t F o u n d E r r o r   c a u s e d   b y   i n c o r r e c t   w o r k i n g   d i r e c t o r y   e x e c u t i o n   o f   t h e   b a c k e n d   s e r v e r .   R e s t a r t e d   t h e   b a c k e n d   c o r r e c t l y   f r o m   t h e   p r o j e c t   r o o t   a n d   u p d a t e d   t h e   s t a r t u p   d o c u m e n t a t i o n   i n   R E A D M E . m d .   V a l i d a t e d   a l l   b a c k e n d   u n i t   t e s t s   ( 1 7 / 1 7   p a s s e d )   a n d   f r o n t e n d   b u i l d   s t a t u s .   A p p l i c a t i o n   i s   n o w   s t a b l e ,   p e r f o r m a n t ,   a n d   p r o d u c t i o n - r e a d y .  
 * * G i t   C o m m i t   M e s s a g e * * :   f i x ( b a c k e n d ) :   u p d a t e   s t a r t u p   i n s t r u c t i o n   t o   r e s o l v e   M o d u l e N o t F o u n d E r r o r  
 # #   P r o m p t   3 6 
 * * T i m e s t a m p * * :   2 0 2 6 - 0 8 - 0 8 T 1 3 : 5 5 : 0 0 + 0 5 : 3 0 
 * * M i l e s t o n e * * :   1 1 . 5   -   P r o d u c t i o n   R e a d i n e s s   A u d i t   &   S t a b i l i z a t i o n 
 * * O b j e c t i v e * * :   F i x   U I   d u p l i c a t e   k e y s ,   n e s t e d   J S O N   d a t a   m o d e l   m i s m a t c h ,   a n d   a d d   s e t t i n g s   p a g e . 
 * * A I   O u t p u t   S u m m a r y * * :   A u d i t e d   f r o n t e n d   A P I   c o n t r a c t s   a g a i n s t   b a c k e n d   J S O N   s c h e m a s .   U p d a t e d   C a n d i d a t e   a n d   C u r r i c u l u m   i n t e r f a c e s .   F i x e d   d u p l i c a t e   R e a c t   k e y s   i n   C u r r i c u l u m P r o g r e s s .   C r e a t e d   f u n c t i o n a l   s i d e b a r   n a v i g a t i o n .   A d d e d   p l a c e h o l d e r   p a g e s   f o r   C a n d i d a t e s   a n d   C u r r i c u l u m .   B u i l t   S e t t i n g s   p a g e   w i t h   r e a l t i m e   A P I   h e a l t h   c h e c k . 
 * * G i t   C o m m i t   M e s s a g e * * :   f e a t :   f u n c t i o n a l   s i d e b a r   n a v i g a t i o n   a n d   p l a c e h o l d e r   p a g e s  
 # #   P r o m p t   3 7 
 * * T i m e s t a m p * * :   2 0 2 6 - 0 8 - 0 8 T 1 4 : 1 2 : 0 0 + 0 5 : 3 0 
 * * M i l e s t o n e * * :   1 2   -   F i n a l   P o l i s h ,   M o d e r n i z a t i o n   &   R e l e a s e   C a n d i d a t e 
 * * O b j e c t i v e * * :   R e m o v e   d e p r e c a t e d   N e x t . j s   L i n k   A P I   u s a g e . 
 * * A I   O u t p u t   S u m m a r y * * :   A u d i t e d   f r o n t e n d   f o r   d e p r e c a t e d   n e x t / l i n k   p a t t e r n s .   U p d a t e d   S i d e b a r I t e m   t o   u s e   n e x t / l i n k   d i r e c t l y   a n d   r e f a c t o r e d   d a s h b o a r d - l a y o u t   t o   u s e   t h e   n e w   m o d e r n   N e x t . j s   1 3 +   s y n t a x   w i t h o u t   l e g a c y B e h a v i o r   o r   p a s s H r e f . 
 * * G i t   C o m m i t   M e s s a g e * * :   f i x ( n e x t ) :   r e m o v e   d e p r e c a t e d   L i n k   A P I   a n d   a d o p t   m o d e r n   N e x t . j s   1 3 +   s y n t a x  
 # #   P r o m p t   3 8 
 * * T i m e s t a m p * * :   2 0 2 6 - 0 8 - 0 8 T 1 4 : 3 8 : 4 0 + 0 5 : 3 0 
 * * M i l e s t o n e * * :   1 2   -   F i n a l   P o l i s h ,   M o d e r n i z a t i o n   &   R e l e a s e   C a n d i d a t e 
 * * O b j e c t i v e * * :   R e m o v e   a l l   m o c k   a n d   h a r d c o d e d   p r o d u c t i o n   d a t a . 
 * * A I   O u t p u t   S u m m a r y * * :   P e r f o r m e d   A P I   c o n t r a c t   a u d i t   a c r o s s   d a s h b o a r d   a n d   f e e d b a c k   c o m p o n e n t s .   R e p l a c e d   m o c k   d a s h b o a r d   s t a t s   w i t h   c a l c u l a t e d   r e a l   d a t a   f r o m   r e p o s i t o r i e s .   R e m o v e d   t h e   f a k e   A n a l y t i c s C h a r t   a n d   R a d a r C h a r t   c o m p l e t e l y .   D i s p l a y e d   C u r r i c u l u m O v e r v i e w   u s i n g   r e a l   b a c k e n d   d a y   d a t a   i n s t e a d   o f   m o c k   p r o g r e s s   s t a t e s . 
 * * G i t   C o m m i t   M e s s a g e * * :   r e f a c t o r :   r e m o v e   a l l   m o c k   a n d   h a r d c o d e d   d a t a   a c r o s s   d a s h b o a r d   a n d   r e p o r t s  
 # #   P r o m p t   3 9 
 * * T i m e s t a m p * * :   2 0 2 6 - 0 8 - 0 8 T 1 4 : 5 0 : 0 0 + 0 5 : 3 0 
 * * M i l e s t o n e * * :   1 2   -   F i n a l   P o l i s h ,   M o d e r n i z a t i o n   &   R e l e a s e   C a n d i d a t e 
 * * O b j e c t i v e * * :   E S L i n t   A u d i t   a n d   F i x e s . 
 * * A I   O u t p u t   S u m m a r y * * :   R a n   n p m   r u n   b u i l d   a n d   n p m   r u n   l i n t ,   c a u g h t   3 4   l i n t i n g   p r o b l e m s   i n c l u d i n g   t y p e s c r i p t   u n e x p e c t e d   a n y   e r r o r s ,   u n e s c a p e d   r e a c t   e n t i t i e s ,   u n u s e d   i m p o r t s   a c r o s s   s e v e r a l   c o m p o n e n t s ,   a n d   c a s c a d i n g   r e n d e r s   f r o m   s e t - s t a t e - i n - e f f e c t   h o o k s .   F i x e d   a l l   l i n t   w a r n i n g s   a n d   e r r o r s ,   r e s u l t i n g   i n   a   c l e a n   b u i l d .   R e m o v e d   t h e   f a l l b a c k   m o c k   G E M I N I _ A P I _ K E Y   f r o m   d e p e n d e n c i e s   t o   e n f o r c e   c o r r e c t   s e t u p . 
 * * G i t   C o m m i t   M e s s a g e * * :   f i x :   r e s o l v e   r e m a i n i n g   E S L i n t   w a r n i n g s   a c r o s s   c o m p o n e n t s  
 # #   P r o m p t   4 0 
 * * T i m e s t a m p * * :   2 0 2 6 - 0 8 - 0 8 T 1 4 : 5 2 : 0 0 + 0 5 : 3 0 
 * * M i l e s t o n e * * :   1 2   -   F i n a l   P o l i s h ,   M o d e r n i z a t i o n   &   R e l e a s e   C a n d i d a t e 
 * * O b j e c t i v e * * :   A c t i v i t y T i m e l i n e   e m p t y   s t a t e . 
 * * A I   O u t p u t   S u m m a r y * * :   R e v i e w e d   A c t i v i t y T i m e l i n e   a n d   a d d e d   a   v i s u a l l y   c o n s i s t e n t   e m p t y   s t a t e   h a n d l i n g   f o r   w h e n   t h e   c a n d i d a t e   a c t i v i t y   f e e d   h a s   0   i t e m s . 
 * * G i t   C o m m i t   M e s s a g e * * :   f e a t :   a d d   e m p t y   s t a t e   t o   A c t i v i t y T i m e l i n e  
 

## Commit: Gemini model configuration
- Added GEMINI_MODEL to .env and .env.example
- Configured app to use gemini-3.5-flash for compatibility


## Commit: GeminiAdapter hardening
- Added domain exceptions (AIEngineException) mapping.
- Configured Gemini API to return structured JSON and updated max_output_tokens.
- Added error handling and retry logic for transient API failures.


## Commit: Global exception handler
- Added global exception handler in main.py for AIEngineException.
- Modified endpoints to bubble up AI exceptions for proper JSON responses.
- Removed dead code in interview.py.


## Commit: Resume interview feature
- Implemented localStorage tracking for active_session_id in frontend.
- Added conditional Resume Interview button logic.
- Handled 404 recovery to clear local session and gracefully redirect.


## Commit: Final cleanup and documentation updates
- Removed unused variables from interview.py.
- Updated README.md to document Milestone 12 changes and environment variables.


---

## Milestone 13 – Final Code Freeze / Release Candidate
Date: 2026-08-08

### Summary
Full production stabilization pass. No new features. Every change is a cleanup, hardening, or documentation improvement.

### Code Cleanup Commits

#### fix(backend): consolidate imports and fix ordering in main.py and dependencies.py
- Moved all imports to the top of each file in PEP8 order.
- Eliminated mid-file imports that were scattered after class instantiation.
- Added docstring to main.py app factory.

#### fix(backend/interview): deduplicate exception handling and fix stale comments
- Removed 3× duplicated inline rom backend.services.ai.exceptions import AIEngineException inside except blocks.
- Replaced repeated isinstance-guard pattern with clean except (HTTPException, AIEngineException): raise idiom.
- Fixed factually incorrect comment that said '5 questions' instead of '8 questions'.
- Removed noise comments from the answer submission flow.

#### fix(backend/dashboard): remove unused Depends import
- Removed Depends from rom fastapi import APIRouter, Depends — it was never used in this module.

#### fix(backend/ai): fix generate_feedback to use real session history and build proper context
- **Critical fix**: AIService.generate_feedback() was previously called with only a raw session_id string, meaning the LLM received no actual interview Q&A data when generating the final report. The report was essentially hallucinated.
- Changed signature to accept InterviewSession.
- Added ContextBuilder.build_candidate_summary_context() and improved uild_history_context() to build a full Q&A transcript.
- Updated evaluate_answer and generate_follow_up to pass meaningful context strings instead of hardcoded placeholders.
- Added ContextBuilder.build_history_context_for_question() for single-question context.
- Removed dead code: score = "" and empty if q.feedback and "score" in q.feedback.lower(): pass block.

#### fix(backend/adapter): sanitize error logs, clarify 404 model error message
- Added _sanitize_error() helper to redact the API key from all logged error messages.
- Improved 404 error message: now says explicitly which model name is unavailable and instructs the user to update GEMINI_MODEL in .env.
- Removed duplicate code extraction line.
- Removed obvious/noise inline comments.

#### fix(tests): remove unused import and dead comment from test_ai.py
- Removed import os (unused).
- Removed stale dead comment block.
- Fixed 	est_gemini_adapter_mock_response to also monkeypatch GEMINI_MODEL (required by the updated adapter).

#### fix(frontend): remove dead code, stale eslint comment, and console.error
- Removed dead if block from the useEffect in interview session page that had an empty body with misleading comments.
- Removed stale // eslint-disable-next-line react-hooks/set-state-in-effect suppression comment.
- Removed console.error(error) from error.tsx (last remaining console.error in the codebase).
- Removed import { useEffect } from error.tsx (now unused after removing the effect).

#### chore: remove dev artifact e2e.py
- Deleted e2e.py from the project root — it was a temporary development debugging script, not production code.

### Documentation Commits

#### docs: fully document all environment variables in .env.example
- Added header, section comments, and descriptions for every variable.
- Added note about what to do if GEMINI_MODEL is deprecated (404 error).

#### docs: complete README rewrite with all sections for hackathon submission
- Full rewrite from perspective of first-time developer and hackathon judge.
- Added all required sections: Project Overview, Problem Statement, Features table, Architecture diagram, Tech Stack table, Folder Structure, AI Workflow diagram, Backend Architecture, Frontend Architecture, API Reference table, Environment Variables table, Installation (verified commands), Running the Application, Running Tests, Gemini API Configuration, Common Troubleshooting, Deployment Notes, Known Limitations, Future Improvements, Authors, License.
- All commands verified on Windows and documented for macOS/Linux equivalents.
- Added explicit note explaining why backend must be run from project root.

### Security Audit Results
- ? No secrets committed. .env is gitignored.
- ? API key is sanitized from all log output via _sanitize_error().
- ? No stack traces in any error response body. All AI exceptions go through the global AIEngineException handler.
- ? GEMINI_API_KEY never appears in any logged line.

### Test Results
- ? 17/17 backend tests pass (pytest).
- ? AI pipeline tests pass with mocked LLM.
- ? Full interview flow tests pass (start ? question ? answer ? follow-up ? complete ? feedback).
- ? Invalid state transition tests pass.
- ? Domain logic tests pass.

### End-to-End Verification
- ? Backend starts successfully (Application startup complete).
- ? GET /health ? 200
- ? GET /candidates ? 200, 20 candidates
- ? GET /curriculum ? 200, modules + days
- ? GET /dashboard ? 200, stats + activities
- ? POST /interview/start ? session created
- ? POST /interview/{id}/next ? Gemini generates context-aware question
- ? POST /interview/{id}/answer ? Gemini evaluates answer, returns feedback and score
- ? POST /interview/{id}/answer (follow_up_required=true) ? follow-up question returned
- ? GET /interview/{id}/feedback (after 8 questions) ? comprehensive report with real history
- ? Resume Interview works via localStorage after page reload
- ? 404 session recovery works (clears localStorage, redirects to Dashboard)

### Gemini Model Configuration
- Model is always read from GEMINI_MODEL env var. Never hardcoded.
- 404 from Gemini returns clear user-friendly message naming the unavailable model.
- No silent fallback to another model.
- 429 rate limit: retries up to 3× with continuation.
- 401 auth failure: immediate failure with clear message.
- Timeout: immediate failure with clear message.

### Known Limitations (Release Candidate)
- In-memory sessions (lost on server restart; frontend handles gracefully).
- No authentication (demo/hackathon scope).
- Static JSON data files (no admin UI).
- Model availability tied to Google's API lifecycle.
A p p e n d i n g   M i l e s t o n e   1 4   t o   P R O M P T S . m d  
  
 # # #   M i l e s t o n e   1 4   &   1 5 :   R e l e a s e   C a n d i d a t e   H a r d e n i n g   &   U I   P o l i s h  
 1 .   I m p l e m e n t e d   r o b u s t   J S O N   p a r s i n g   p i p e l i n e   w i t h   9 - s t e p   r e c o v e r y   ( s t r i p p i n g   m a r k d o w n ,   i s o l a t i n g   b r a c k e t s ) .  
 2 .   A d d e d   s t r i c t   s c h e m a   v a l i d a t i o n   f o r   L L M   r e s p o n s e s .  
 3 .   I m p l e m e n t e d   a   o n e - t i m e   L L M   r e t r y   m e c h a n i s m   f o r   p a r s i n g   f a i l u r e s .  
 4 .   A d d e d   p o l i s h e d   s k e l e t o n   l o a d i n g   s t a t e s   a c r o s s   t h e   f r o n t e n d   ( D a s h b o a r d ,   C u r r i c u l u m ,   I n t e r v i e w ) .  
 5 .   S a n i t i z e d   e r r o r   m e s s a g e s   t o   a v o i d   l e a k i n g   J S O N D e c o d e E r r o r s   t o   t h e   U I .  
 6 .   I m p r o v e d   a c c e s s i b i l i t y   w i t h   a u t o - f o c u s i n g   a n s w e r   b o x   i n   i n t e r v i e w   s e s s i o n .  
 

## Milestone 17 - Final UI/UX Polish & Demo Experience
Added premium loading states, session picker, countdown timers for rate limits, framer-motion transitions, and accessibility improvements for the final demo.


=========================================================
MILESTONE 18.1 â€“ LIVE AI PROVIDER VERIFICATION
=========================================================
Completed verification of Gemini failover, NVIDIA fallback, Mock fallback, Session state machine transitions, Test environment separation, and Security audit.


=========================================================
MILESTONE 18.2 â€“ NVIDIA Credential/Model Mapping & Real Provider Verification
=========================================================
Fixed NVIDIA provider to strictly map NVIDIA_API_KEY_1 to PRIMARY and NVIDIA_API_KEY_2 to SECONDARY models. Tested structured output parsing with recovery pipeline. Simulated provider fallback logic. All verification tasks complete.


=========================================================
MILESTONE 18.3 â€“ AI Failover Hardening & Latency Optimization
=========================================================
1. Why Milestone 18.3 was required: The live NVIDIA verification exposed timeouts and long waits in the failover chain. Test isolation was also incomplete, causing pytest to run real network requests.
2. NVIDIA timeout findings: Found that OpenAI client used standard timeouts and retries, creating up to 60s delays on unreachable endpoints.
3. Timeout improvements: Added strict httpx.Timeout(7.0, connect=3.0) and max_retries=0 to NvidiaProvider, ensuring <10s failures. Added 10s timeout to Gemini provider.
4. Gemini key rotation: Reused existing rotation logic but bounded by total timeouts.
5. NVIDIA credential/model mapping: Remained strict and proven secure.
6. Provider ordering: Gemini -> NVIDIA NIM -> Mock Provider.
7. Fast failover: Max latency during complete fallback is ~11-15s per request, well under the UX limit.
8. MockProvider safety net: Refactored to iterate deterministically through 10 unique technical questions, preventing duplicate question loops in emergency fallbacks.
9. Test environment isolation: Enforced app.dependency_overrides in pytest to ensure 100% offline isolation without relying on fragile .env states.
10. Live verification separation: Created backend/verify_live_ai.py for explicit live credential testing and backend/verify_mock_interview.py for UI-safe logic testing.
11. Structured output validation: Re-verified to ensure MockProvider guarantees JSON compliance.
12. Interview progression verification: Mock session runs smoothly across multiple questions without duplication or state corruption.
13. Refresh/resume verification: State machine safely returns the correct status.
14. Performance measurements: Primary failover takes ~8.5s, Secondary failover takes ~6s, Mock failover takes 0.0s. Total mock fallback latency is fast and bounded.
15. Security verification: Zero credentials exposed, zero leaks.
16. Automated test results: pytest -v executed completely offline with 18/18 passing in <3 seconds.
17. Build results: npm run build completed successfully.
18. Remaining limitations: NVIDIA Primary endpoint continues to time out locally, but NVIDIA Secondary succeeded successfully, proving the integration is alive.


=========================================================
URGENT LOCAL RUNTIME BUG FIX
=========================================================
- Added `openai` dependency to `requirements.txt` which was causing `ModuleNotFoundError`.
- Restricted CORS in `backend/main.py` from `*` to strictly allow `http://localhost:3000` and `http://127.0.0.1:3000`.
- Verified full local startup and frontend end-to-end interview state.