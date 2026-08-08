import os
import time
import json
from dotenv import load_dotenv

# Load env before imports
load_dotenv()

from backend.services.ai.engine import AIEngine
from backend.services.ai.providers.gemini import GeminiProvider
from backend.services.ai.providers.nvidia import NvidiaProvider
from backend.services.ai.providers.mock import MockProvider
from backend.services.ai.exceptions import LLMRateLimitException
from backend.services.ai.response_parser import ResponseParser
from backend.utils.logger import logger

def measure_latency(func, *args):
    start = time.time()
    try:
        res = func(*args)
        success = True
    except Exception as e:
        res = str(e)
        success = False
    end = time.time()
    return success, res, end - start

def verify_gemini_rotation():
    print("\n--- 2. VERIFY GEMINI PROVIDER ---")
    provider = GeminiProvider()
    print(f"Loaded {len(provider.api_keys)} Gemini keys.")
    if len(provider.api_keys) > 0:
        original_keys = list(provider.api_keys)
        for idx, key in enumerate(original_keys):
            print(f"Testing Gemini Key {idx + 1}...")
            provider.api_keys = [key]
            success, res, latency = measure_latency(provider.generate_question, "Give me a one sentence React question.")
            if not success and "timeout" in str(res).lower():
                print(f"Gemini Key {idx + 1} Success: False, Latency: {latency:.2f}s, Status: TIMEOUT")
            elif not success and ("invalid" in str(res).lower() or "400" in str(res).lower()):
                print(f"Gemini Key {idx + 1} Success: False, Latency: {latency:.2f}s, Status: AUTH_FAILURE")
            elif not success and ("rate limit" in str(res).lower() or "busy" in str(res).lower() or "exhausted" in str(res).lower()):
                print(f"Gemini Key {idx + 1} Success: False, Latency: {latency:.2f}s, Status: RATE_LIMIT")
            elif not success and "not found" in str(res).lower():
                print(f"Gemini Key {idx + 1} Success: False, Latency: {latency:.2f}s, Status: MODEL_NOT_FOUND")
            else:
                print(f"Gemini Key {idx + 1} Success: {success}, Latency: {latency:.2f}s")
                if not success:
                    print(f"Sanitized Error: {res}")
        provider.api_keys = original_keys
    else:
        print("No Gemini keys configured.")

def verify_nvidia_mapping():
    print("\n--- 3 & 4. VERIFY NVIDIA PROVIDER & MAPPING ---")
    provider = NvidiaProvider()
    print(f"Loaded {len(provider.configs)} NVIDIA configurations.")
    
    original_configs = list(provider.configs)
    
    if len(original_configs) >= 1:
        # Test Primary explicitly
        key1, model1 = original_configs[0]
        print(f"Primary config: Key length {len(key1) if key1 else 0}, Model: {model1}")
        
        # Temporarily mock provider to ONLY test Primary
        provider.configs = [(key1, model1)]
        success, res, latency = measure_latency(provider.generate_question, "Give me a one sentence React question.")
        if not success and "timeout" in str(res).lower():
            print(f"NVIDIA Primary Success: False, Latency: {latency:.2f}s, Status: TIMEOUT")
        else:
            print(f"NVIDIA Primary Success: {success}, Latency: {latency:.2f}s")
            if not success:
                print(f"Sanitized Error: {res}")
            
    if len(original_configs) >= 2:
        # Test Secondary explicitly
        key2, model2 = original_configs[1]
        print(f"Secondary config: Key length {len(key2) if key2 else 0}, Model: {model2}")
        
        provider.configs = [(key2, model2)]
        success, res, latency = measure_latency(provider.generate_question, "Give me a one sentence React question.")
        if not success and "timeout" in str(res).lower():
            print(f"NVIDIA Secondary Success: False, Latency: {latency:.2f}s, Status: TIMEOUT")
        else:
            print(f"NVIDIA Secondary Success: {success}, Latency: {latency:.2f}s")
            if not success:
                print(f"Sanitized Error: {res}")
                
    provider.configs = original_configs

def verify_structured_output():
    print("\n--- 5. VERIFY STRUCTURED OUTPUT ---")
    # Using MockProvider to ensure we test the parser contract deterministically
    # (since we don't know if live keys have credits)
    provider = MockProvider()
    
    # 1. Question
    q_str = provider.generate_question("prompt")
    q_val = ResponseParser.parse_question(q_str)
    print(f"Question parsing success: {isinstance(q_val, str) and len(q_val) > 0}")
    
    # 2. Evaluate
    e_str = provider.evaluate_answer("prompt")
    e_val = ResponseParser.parse_evaluation(e_str)
    print(f"Evaluation parsing success: {isinstance(e_val, str) and len(e_val) > 0}")

def verify_failover_engine():
    print("\n--- 6 & 7. VERIFY PROVIDER FAILOVER & ORDERING ---")
    engine = AIEngine()
    print(f"Provider Order: {[p.provider_name for p in engine.providers]}")
    
    print("Scenario A/B: Normal Engine Execution (Should attempt Gemini -> NVIDIA -> Mock)")
    success, res, latency = measure_latency(engine.generate_question, "Hello")
    print(f"Execution Success: {success}, Latency: {latency:.2f}s")

    print("Scenario D: All external unavailable -> MockProvider")
    original_providers = engine.providers
    engine.providers = [MockProvider()]
    success, res, latency = measure_latency(engine.generate_question, "Hello")
    print(f"Mock Fallback Success: {success}, Latency: {latency:.2f}s")
    
    engine.providers = original_providers

def run_all():
    print("Starting AI Provider Verification...")
    verify_gemini_rotation()
    verify_nvidia_mapping()
    verify_structured_output()
    verify_failover_engine()
    print("\nVerification Complete.")

if __name__ == "__main__":
    logger.setLevel("ERROR")
    run_all()
