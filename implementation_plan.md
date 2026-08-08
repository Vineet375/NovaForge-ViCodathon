# Goal Description
Harden the AI failover pipeline for fast, deterministic performance, fix NVIDIA timeout cascades, isolate the test environment explicitly, and run a live mock fallback interview to prove UI/UX integrity.

## User Review Required
No major architectural redesigns are proposed. All changes are targeted optimizations matching Milestone 18.3 requirements.

## Proposed Changes

### AI Pipeline Latency & Failover Hardening
- **[MODIFY] backend/services/ai/providers/nvidia.py**: Implement explicit separate timeouts `httpx.Timeout(7.0, connect=3.0)` and set `max_retries=0` in the OpenAI client constructor to prevent 60s+ cascades.
- **[MODIFY] backend/services/ai/providers/gemini.py**: Implement bounded timeouts for the Gemini genai client using `http_options={'timeout': 10000}` (10s) to prevent it from hanging indefinitely on network issues, and preserve rate-limiting semantics without hammering the API.
- **[MODIFY] backend/services/ai/engine.py**: Add explicit `test_mode: bool = False` to `AIEngine.__init__` to force MockProvider, removing reliance on `.env` parsing which causes bleed-through in pytest.

### Test Environment Isolation
- **[MODIFY] backend/tests/test_api.py**: Remove legacy `GeminiAdapter` mocking. Implement `app.dependency_overrides[get_ai_service]` to inject a test-mode `AIEngine`, absolutely guaranteeing no external network calls during `pytest`.
- **[MODIFY] backend/tests/test_ai.py**: Remove legacy `GeminiAdapter` tests, replace with localized MockProvider and AIEngine testing.

### Fallback Enhancements
- **[MODIFY] backend/services/ai/providers/mock.py**: Enhance `MockProvider` to use a seeded or stateful mechanism to prevent duplicate questions within the same mock session flow.
- **[MODIFY] backend/api/dependencies.py**: Ensure `AIEngine` can be easily overridden in tests.

### Verification Assets
- **[RENAME/MODIFY] backend/verify_live_ai.py**: Rename `verify.py` to `verify_live_ai.py` and update it to strictly bound timeouts and classify timeouts explicitly as "TIMEOUT" rather than masking them.
- **[NEW] backend/verify_mock_interview.py**: A script to simulate a complete 3-question interview strictly using the mock provider to prove progress tracking without hanging UI.

## Verification Plan
### Automated Tests
- Run `pytest -v` to prove fast, offline completion with zero API calls.
### Manual Verification
- Run `python backend/verify_live_ai.py` to prove bounded timeouts (< 10s per failover).
- Run `npm run build` to ensure frontend integrity.
- Run `python backend/verify_mock_interview.py` to prove the state machine safely handles mock failover without duplicating questions.
