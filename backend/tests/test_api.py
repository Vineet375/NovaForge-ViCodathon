import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.api.schemas import StartInterviewRequest

client = TestClient(app)

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
    
    # 2. Start Interview
    req = {"candidate_id": candidate_id}
    start_resp = client.post("/interview/start", json=req)
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    session_id = start_data["session_id"]
    assert session_id is not None
    
    # 3. Get Next Question
    next_resp = client.post(f"/interview/{session_id}/next")
    assert next_resp.status_code == 200
    next_data = next_resp.json()
    assert "question_text" in next_data
    
    # 4. Answer Question
    ans_req = {"answer_text": "This is a test answer."}
    ans_resp = client.post(f"/interview/{session_id}/answer", json=ans_req)
    assert ans_resp.status_code == 200
    ans_data = ans_resp.json()
    assert "feedback" in ans_data
    
    # 5. Get Session State
    state_resp = client.get(f"/interview/{session_id}")
    assert state_resp.status_code == 200
    state_data = state_resp.json()
    assert state_data["status"] == "in_progress"
    assert state_data["current_question_number"] == 1
    assert len(state_data["questions_asked"]) == 1
