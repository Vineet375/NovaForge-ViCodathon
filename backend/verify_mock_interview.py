import time
from backend.main import app
from fastapi.testclient import TestClient

def run_mock_interview():
    print("Starting Mock Interview Progress Tracking Test...")
    client = TestClient(app)

    # 1. Get candidate
    candidates = client.get("/candidates").json()
    candidate_id = candidates[1]["member"]["id"]
    
    # 2. Start Interview
    print("\n--- Starting Interview ---")
    start_resp = client.post("/interview/start", json={"candidate_id": candidate_id})
    session_id = start_resp.json()["session_id"]
    print(f"Session ID: {session_id}")
    
    # Track questions to ensure no duplicates
    asked_questions = set()

    for i in range(1, 4):
        print(f"\n--- Turn {i} ---")
        
        # Get Next Question
        t0 = time.time()
        next_resp = client.post(f"/interview/{session_id}/next")
        t1 = time.time()
        q_data = next_resp.json()
        q_text = q_data.get("question_text", "")
        print(f"Question (latency: {t1-t0:.3f}s): {q_text[:50]}...")
        
        if q_text in asked_questions:
            print(f"FAIL: Duplicate question detected! '{q_text}'")
            return False
        asked_questions.add(q_text)

        # Answer
        t0 = time.time()
        ans_resp = client.post(f"/interview/{session_id}/answer", json={"answer_text": f"Mock answer {i}"})
        t1 = time.time()
        f_data = ans_resp.json()
        feedback = f_data.get("feedback", "")
        print(f"Evaluation (latency: {t1-t0:.3f}s): {feedback[:50]}...")
        
        # State
        state = client.get(f"/interview/{session_id}").json()
        print(f"Current Question Number: {state['current_question_number']}")
        print(f"Total Questions Asked: {len(state['questions_asked'])}")

    print("\nSUCCESS: Mock interview completed 3 turns without duplicates or hanging.")
    return True

if __name__ == "__main__":
    run_mock_interview()
