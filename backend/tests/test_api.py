import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app

from backend.api.dependencies import get_ai_service
from backend.services.ai.ai_service import AIService
from backend.services.ai.engine import AIEngine

client = TestClient(app)

# Explicitly inject MockProvider via test_mode=True to ensure ZERO external API calls.
@pytest.fixture(autouse=True)
def isolate_ai_engine():
    # Instantiate the engine in test_mode to bypass all real keys
    mock_engine = AIEngine(test_mode=True)
    mock_service = AIService(mock_engine)
    
    app.dependency_overrides[get_ai_service] = lambda: mock_service
    yield
    app.dependency_overrides.clear()

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "uptime" in data

def test_get_candidates():
    response = client.get("/candidates")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_curriculum():
    response = client.get("/curriculum")
    assert response.status_code == 200
    data = response.json()
    assert "modules" in data
    assert "days" in data

def test_get_invalid_candidate():
    response = client.get("/candidates/invalid_id")
    assert response.status_code == 404

def test_get_invalid_curriculum_day():
    response = client.get("/curriculum/day/999")
    assert response.status_code == 404

def test_interview_flow():
    # 1. Get a valid candidate
    candidates = client.get("/candidates").json()
    candidate_id = candidates[0]["member"]["id"]
    
    # 2. Start Interview (Generates Q1 in background synchronously in TestClient)
    req = {"candidate_id": candidate_id}
    start_resp = client.post("/interview/start", json=req)
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    session_id = start_data["session_id"]
    assert session_id is not None
    
    # 3. Verify Q1 is ready
    state_resp = client.get(f"/interview/{session_id}")
    assert state_resp.status_code == 200
    state_data = state_resp.json()
    assert state_data["status"] == "question_ready"
    assert state_data["current_question_number"] == 1
    
    # 4. Answer Q1 (Generates Q2 in background)
    ans_req = {"answer_text": "This is a test answer."}
    ans_resp = client.post(f"/interview/{session_id}/answer", json=ans_req)
    assert ans_resp.status_code == 200
    
    # 5. Verify Q2 is ready
    state_resp = client.get(f"/interview/{session_id}")
    assert state_resp.status_code == 200
    state_data = state_resp.json()
    assert state_data["status"] == "question_ready"
    assert state_data["current_question_number"] == 2
    assert len(state_data["questions_asked"]) == 2

def test_full_interview_flow():
    # 1. Get a valid candidate
    candidates = client.get("/candidates").json()
    candidate_id = candidates[1]["member"]["id"]
    
    # 2. Start Interview
    req = {"candidate_id": candidate_id}
    start_resp = client.post("/interview/start", json=req)
    session_id = start_resp.json()["session_id"]
    
    # Run through 4 questions
    for i in range(4):
        ans_req = {"answer_text": "This is a test answer."}
        ans_resp = client.post(f"/interview/{session_id}/answer", json=ans_req)
        assert ans_resp.status_code == 200
        
    state_resp = client.get(f"/interview/{session_id}")
    assert state_resp.json()["status"] == "completed"
    
    # Try answering when completed (Idempotency should return 200)
    bad_ans = client.post(f"/interview/{session_id}/answer", json={"answer_text": "test"})
    assert bad_ans.status_code == 200
    feedback = client.get(f"/interview/{session_id}/feedback")
    assert feedback.status_code == 200
    assert "overall_score" in feedback.json()

def test_invalid_transitions():
    candidates = client.get("/candidates").json()
    candidate_id = candidates[2]["member"]["id"]
    
    req = {"candidate_id": candidate_id}
    start_resp = client.post("/interview/start", json=req)
    session_id = start_resp.json()["session_id"]
    
    # Try to fetch next manually when it's already generated (409)
    bad_next = client.post(f"/interview/{session_id}/next")
    assert bad_next.status_code == 409
