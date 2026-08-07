import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# We use an autouse fixture to patch _call_gemini on GeminiAdapter
# so no tests accidentally hit the real API.
@pytest.fixture(autouse=True)
def mock_gemini():
    with patch("backend.services.ai.gemini_adapter.GeminiAdapter._call_gemini") as mock:
        # Provide a default valid JSON response depending on the prompt
        def side_effect(prompt):
            if "feedback" in prompt.lower() and "score" in prompt.lower() and "follow_up" in prompt.lower():
                return '{"feedback": "Good answer.", "score": 8, "follow_up_required": false, "confidence": "high"}'
            elif "overall_score" in prompt.lower():
                return '{"overall_score": 85, "strengths": ["a"], "weaknesses": ["b"], "improvement_topics": ["c"], "recommended_learning_path": "d", "curriculum_references": ["e"], "confidence_level": "high", "interview_summary": "Great"}'
            else:
                return '{"question_text": "What is React?"}'
        mock.side_effect = side_effect
        yield mock

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

def test_full_interview_flow():
    # 1. Get a valid candidate
    candidates = client.get("/candidates").json()
    candidate_id = candidates[1]["member"]["id"]
    
    # 2. Start Interview
    req = {"candidate_id": candidate_id}
    start_resp = client.post("/interview/start", json=req)
    session_id = start_resp.json()["session_id"]
    
    # Run through 8 questions
    for i in range(8):
        next_resp = client.post(f"/interview/{session_id}/next")
        assert next_resp.status_code == 200
        
        ans_req = {"answer_text": "This is a test answer."}
        ans_resp = client.post(f"/interview/{session_id}/answer", json=ans_req)
        assert ans_resp.status_code == 200
        
    state_resp = client.get(f"/interview/{session_id}")
    assert state_resp.json()["status"] == "completed"
    
    # Try getting next when completed (Invalid state transition)
    bad_next = client.post(f"/interview/{session_id}/next")
    assert bad_next.status_code == 400
    assert "cannot fetch next question" in bad_next.json()["detail"].lower()
    
    # Try answering when completed (Invalid state transition)
    bad_ans = client.post(f"/interview/{session_id}/answer", json={"answer_text": "test"})
    assert bad_ans.status_code == 400
    
    # Get Final Feedback
    feedback = client.get(f"/interview/{session_id}/feedback")
    assert feedback.status_code == 200
    assert "overall_score" in feedback.json()

def test_invalid_transitions():
    candidates = client.get("/candidates").json()
    candidate_id = candidates[2]["member"]["id"]
    
    req = {"candidate_id": candidate_id}
    start_resp = client.post("/interview/start", json=req)
    session_id = start_resp.json()["session_id"]
    
    # Try to answer before getting the first question
    ans_req = {"answer_text": "This is a test answer."}
    ans_resp = client.post(f"/interview/{session_id}/answer", json=ans_req)
    assert ans_resp.status_code == 400
    assert "No question has been asked yet" in ans_resp.json()["detail"]
