import asyncio
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.candidate import Candidate, Member
from backend.services.domain.session_manager import SessionManager
from backend.models.interview import InterviewState
import pytest

client = TestClient(app)

def test_api_behavior():
    print("Testing HTTP Behavior...")
    
    # 1. Start Interview
    print("-> POST /interview/start")
    # Need a candidate ID first. Let's just pass anything and see 404.
    response = client.post("/interview/start", json={"candidate_id": "nonexistent"})
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    # Create a mock candidate
    from backend.api.dependencies import get_candidate_repo, get_session_manager, get_curriculum_repo, get_ai_service
    repo = get_candidate_repo()
    candidates = repo.get_all_candidates()
    assert len(candidates) > 0
    candidate_id = candidates[0].member.id
    
    response = client.post("/interview/start", json={"candidate_id": candidate_id})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    session_id = response.json()["session_id"]
    
    # 2. GET /interview/active
    print("-> GET /interview/active")
    response = client.get("/interview/active")
    assert response.status_code == 200
    active_sessions = response.json()
    assert len(active_sessions) == 1
    assert active_sessions[0]["session_id"] == session_id
    
    # 3. GET /interview/{id}
    print("-> GET /interview/{id}")
    response = client.get(f"/interview/{session_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "initializing"
    
    # 4. Mock AI Service to simulate 429
    class MockAIService:
        def generate_initial_question(self, *args, **kwargs):
            from backend.services.ai.exceptions import LLMRateLimitException
            raise LLMRateLimitException("Rate limited", retry_after=5)
            
        def evaluate_answer(self, *args, **kwargs):
            return {"feedback": "Good", "score": 8, "confidence": "high", "follow_up_required": "false"}
            
        def generate_follow_up(self, *args, **kwargs):
            return None
            
        def generate_feedback(self, *args, **kwargs):
            return {"overall_score": 8, "strengths": [], "weaknesses": [], "improvement_topics": [], "recommended_learning_path": "", "curriculum_references": [], "confidence_level": "high", "interview_summary": ""}
            
    app.dependency_overrides[get_ai_service] = lambda: MockAIService()
    
    print("-> POST /interview/{id}/next (Testing Demo Fallback on Rate Limit)")
    response = client.post(f"/interview/{session_id}/next")
    assert response.status_code == 200
    assert response.json()["question_text"] == "Can you describe a time when you had to optimize a piece of code for performance? What was the outcome?"
    
    response = client.get(f"/interview/{session_id}")
    assert response.json()["status"] == "active"
    
    # Reset AI Service to normal mock
    class SuccessMockAIService:
        def generate_initial_question(self, *args, **kwargs):
            return "What is React?"
            
        def evaluate_answer(self, *args, **kwargs):
            return {"feedback": "Good", "score": 8, "confidence": "high", "follow_up_required": "false"}
            
        def generate_follow_up(self, *args, **kwargs):
            return None
            
        def generate_feedback(self, *args, **kwargs):
            return {"overall_score": 8, "strengths": [], "weaknesses": [], "improvement_topics": [], "recommended_learning_path": "", "curriculum_references": [], "confidence_level": "high", "interview_summary": ""}

    app.dependency_overrides[get_ai_service] = lambda: SuccessMockAIService()
    
    # Bypass wait time for test
    session_manager = get_session_manager()
    session = session_manager.get_session(session_id)
    session.retry_after = None
    
    # Answer the fallback question so we can get the next one
    client.post(f"/interview/{session_id}/answer", json={"answer_text": "I used caching."})
    
    print("-> POST /interview/{id}/next (Success)")
    response = client.post(f"/interview/{session_id}/next")
    assert response.status_code == 200
    assert response.json()["question_text"] == "What is React?"
    
    # Test Idempotency (calling next again should return same question since it's unanswered)
    print("-> POST /interview/{id}/next (Idempotency)")
    response = client.post(f"/interview/{session_id}/next")
    assert response.status_code == 200
    assert response.json()["question_text"] == "What is React?"
    
    print("-> POST /interview/{id}/answer")
    response = client.post(f"/interview/{session_id}/answer", json={"answer_text": "A UI library."})
    assert response.status_code == 200
    assert response.json()["feedback"] == "Good"
    assert response.json()["follow_up_question"] is None
    
    # Test Idempotency for answer
    print("-> POST /interview/{id}/answer (Idempotency)")
    response = client.post(f"/interview/{session_id}/answer", json={"answer_text": "A UI library."})
    assert response.status_code == 200
    assert response.json()["feedback"] == "Good"
    
    # Complete interview test
    session.current_question_number = 7
    client.post(f"/interview/{session_id}/next") # get question 8
    
    response = client.post(f"/interview/{session_id}/answer", json={"answer_text": "Final."})
    assert response.status_code == 200
    
    response = client.get(f"/interview/{session_id}")
    assert response.json()["status"] == "completed"
    
    print("-> GET /interview/{id}/feedback")
    response = client.get(f"/interview/{session_id}/feedback")
    assert response.status_code == 200
    assert response.json()["overall_score"] == 8
    
    # Test 400
    print("-> POST /interview/{id}/next on completed session (Testing 400)")
    response = client.post(f"/interview/{session_id}/next")
    assert response.status_code == 400
    
    print("All HTTP checks passed!")

if __name__ == "__main__":
    test_api_behavior()
