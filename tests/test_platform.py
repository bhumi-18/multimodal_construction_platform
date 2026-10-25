"""
Unit & Integration Test Suite for Multimodal Construction Intelligence Platform
"""

import sys
import os
from PIL import Image

# Reconfigure stdout for utf-8 on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add root directory to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from modules.gemini_client import GeminiVisionEngine, clean_json_response
from modules.ppe_detector import analyze_ppe_compliance, generate_mock_ppe_audit
from modules.crack_diagnostics import analyze_crack_integrity, generate_mock_crack_diagnosis
from modules.cost_valuation import calculate_project_metrics, format_inr
from modules.pollinations_client import build_architectural_prompt, get_pollinations_image_url
from modules.weather_advisory import get_weather_advisory, answer_engineering_query


def test_gemini_client():
    print("--> 1. Testing Gemini Client & JSON Sanitizer...")
    engine = GeminiVisionEngine(api_key="")
    assert not engine.is_live, "Default without API key must be in demonstration mode"
    
    test_json_str = '```json\n{"status": "ok", "safety_score": 90}\n```'
    parsed = clean_json_response(test_json_str)
    assert parsed["safety_score"] == 90
    assert parsed["status"] == "ok"
    print("    [PASS] Gemini client and JSON parser functional.")


def test_ppe_detector():
    print("--> 2. Testing PPE Site Safety Audit...")
    engine = GeminiVisionEngine(api_key="")
    dummy_img = Image.new("RGB", (200, 200), color="blue")
    result, is_live, note = analyze_ppe_compliance(dummy_img, engine)
    
    assert "safety_score" in result
    assert "overall_status" in result
    assert "ppe_detection" in result
    assert "identified_hazards" in result
    assert len(result["identified_hazards"]) > 0
    assert not is_live
    print(f"    [PASS] PPE detector returned valid schema: Safety Score = {result['safety_score']}")


def test_crack_diagnostics():
    print("--> 3. Testing Concrete Crack Diagnostics...")
    engine = GeminiVisionEngine(api_key="")
    dummy_img = Image.new("RGB", (200, 200), color="gray")
    result, is_live, note = analyze_crack_integrity(dummy_img, engine, image_name="shear_crack.jpg")
    
    assert "defect_type" in result
    assert "estimated_crack_width_mm" in result
    assert "is_456_permissible_limit_mm" in result
    assert "engineering_repair_protocol" in result
    assert len(result["engineering_repair_protocol"]) > 0
    print(f"    [PASS] Crack diagnostics functional: Defect = {result['defect_type']}, Width = {result['estimated_crack_width_mm']}mm")


def test_cost_valuation():
    print("--> 4. Testing Indian Real Estate Valuation & Material Estimation...")
    metrics = calculate_project_metrics(
        structure_type="Residential High-Rise (G+25 Floors)",
        built_up_sqft=65000,
        location_tier="Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Chennai, Hyderabad)",
        quality_grade="Premium",
        completion_percentage=45.0
    )
    
    assert metrics["total_budget_inr"] > 0
    assert metrics["capex_incurred_inr"] > 0
    assert metrics["current_asset_valuation_inr"] > 0
    assert "Cr" in metrics["total_budget_formatted"] or "L" in metrics["total_budget_formatted"]
    assert metrics["materials"]["steel_tonnes"] > 0
    assert metrics["materials"]["cement_bags"] > 0
    assert len(metrics["stages"]) == 4
    print(f"    [PASS] Valuation completed: Total Budget = {metrics['total_budget_formatted']}, CapEx = {metrics['capex_incurred_formatted']}")


def test_pollinations():
    print("--> 5. Testing Pollinations 3D Render Prompt Generator...")
    prompt = build_architectural_prompt(
        structure_type="Commercial IT Park / Grade-A Office",
        location_tier="Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Chennai, Hyderabad)",
        quality_grade="Ultra-Luxury / High-Tech",
        completion_percentage=60.0
    )
    assert len(prompt) > 30
    url = get_pollinations_image_url(prompt)
    assert url.startswith("https://image.pollinations.ai/prompt/")
    print("    [PASS] Pollinations URL and prompt generation verified.")


def test_weather_and_chat():
    print("--> 6. Testing Weather Protocols and Engineering Chatbot...")
    engine = GeminiVisionEngine(api_key="")
    proto = get_weather_advisory("High Wind (> 45 km/h / Gale)")
    assert "action_items" in proto
    assert len(proto["action_items"]) > 0
    
    chat_response = answer_engineering_query("What is the crane wind speed limit?", [], engine)
    assert "crane" in chat_response.lower() or "wind" in chat_response.lower()
    print("    [PASS] Weather protocols and domain chatbot verified.")


if __name__ == "__main__":
    print("==================================================================")
    print("RUNNING MULTIMODAL CONSTRUCTION PLATFORM TEST SUITE")
    print("==================================================================")
    test_gemini_client()
    test_ppe_detector()
    test_crack_diagnostics()
    test_cost_valuation()
    test_pollinations()
    test_weather_and_chat()
    print("==================================================================")
    print("ALL TESTS PASSED SUCCESSFULLY! (100% PASS RATE)")
    print("==================================================================")
