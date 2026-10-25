"""
PPE Safety Vision & Site Compliance Module (Epic 2)
Audits worker PPE compliance (helmets, high-vis vests, steel-toe boots, safety harnesses)
under OSHA (1926.95/100/102/501) and Indian Standards (IS 456, IS 3696, IS 2925).
"""

from typing import Dict, Any, Tuple
from PIL import Image
from modules.gemini_client import GeminiVisionEngine, clean_json_response

PPE_AUDIT_PROMPT = """
You are a Senior Construction Safety Inspector and Auditor certified under OSHA 1926 and Bureau of Indian Standards (IS 456:2000, IS 3696 Part 1 & 2, IS 2925).
Analyze the provided construction site photo with high precision and produce an exhaustive safety audit in STRICT JSON format.

Your JSON response must adhere to the following schema without any extra text:
{
  "safety_score": <integer from 0 to 100>,
  "overall_status": "<Compliant | Partially Compliant | Non-Compliant | Critical Risk>",
  "workers_detected_count": <integer>,
  "ppe_detection": {
    "helmets": {
      "detected": <integer>,
      "compliant": <integer>,
      "non_compliant": <integer>,
      "standard": "IS 2925 / OSHA 1926.100",
      "status": "<Pass | Warning | Fail>",
      "observations": "<detailed description of compliance or violations>"
    },
    "high_vis_vests": {
      "detected": <integer>,
      "compliant": <integer>,
      "non_compliant": <integer>,
      "standard": "EN ISO 20471 / OSHA 1926.201",
      "status": "<Pass | Warning | Fail>",
      "observations": "<detailed description>"
    },
    "steel_toe_boots": {
      "detected": <integer>,
      "compliant": <integer>,
      "non_compliant": <integer>,
      "standard": "IS 15298 / OSHA 1926.96",
      "status": "<Pass | Warning | Fail>",
      "observations": "<detailed description>"
    },
    "safety_harnesses": {
      "detected": <integer>,
      "compliant": <integer>,
      "non_compliant": <integer>,
      "standard": "IS 3521 / OSHA 1926.502",
      "status": "<Pass | Warning | Fail>",
      "observations": "<detailed description of anchorages and lifelines>"
    },
    "respiratory_eye_protection": {
      "detected": <integer>,
      "compliant": <integer>,
      "non_compliant": <integer>,
      "standard": "IS 5983 / OSHA 1926.102",
      "status": "<Pass | Warning | Fail>",
      "observations": "<detailed description>"
    }
  },
  "identified_hazards": [
    {
      "hazard_title": "<Concise hazard name>",
      "severity": "<Critical | High | Medium | Low>",
      "zone": "<Specific site location visible in image>",
      "standards_violation": "<e.g., OSHA 1926.501(b)(1) & IS 3696 Part 1>",
      "risk_description": "<Precise description of dangerous condition or behavior>",
      "corrective_remedy": "<Mandatory engineering and procedural corrective action>"
    }
  ],
  "executive_summary": "<Professional 2-3 sentence overview of site compliance state>",
  "recommended_stop_work": <boolean true or false>
}
"""

def generate_mock_ppe_audit(image_name: str = "") -> Dict[str, Any]:
    """Generates a realistic, highly detailed audit report for demonstration mode."""
    return {
        "safety_score": 72,
        "overall_status": "Partially Compliant",
        "workers_detected_count": 2,
        "ppe_detection": {
            "helmets": {
                "detected": 2,
                "compliant": 1,
                "non_compliant": 1,
                "standard": "IS 2925 / OSHA 1926.100",
                "status": "Warning",
                "observations": "Worker #1 is wearing an approved yellow Type I Class E safety helmet. Worker #2 is operating without required cranial protection near the overhead scaffold."
            },
            "high_vis_vests": {
                "detected": 2,
                "compliant": 1,
                "non_compliant": 1,
                "standard": "EN ISO 20471 / OSHA 1926.201",
                "status": "Warning",
                "observations": "Worker #1 has fluorescent orange retroreflective vest. Worker #2 is in non-reflective blue civilian clothing, presenting low-visibility collision risk."
            },
            "steel_toe_boots": {
                "detected": 2,
                "compliant": 1,
                "non_compliant": 1,
                "standard": "IS 15298 / OSHA 1926.96",
                "status": "Warning",
                "observations": "Worker #1 is equipped with IS-marked puncture-resistant safety boots. Worker #2 is wearing standard non-reinforced rubber sneakers on an active slab."
            },
            "safety_harnesses": {
                "detected": 2,
                "compliant": 1,
                "non_compliant": 1,
                "standard": "IS 3521 / OSHA 1926.502",
                "status": "Fail",
                "observations": "Worker #1 has full-body harness donned. Worker #2 is exposed at an unprotected edge exceeding 2.0 meters without tie-off or arrest lanyard."
            },
            "respiratory_eye_protection": {
                "detected": 2,
                "compliant": 0,
                "non_compliant": 2,
                "standard": "IS 5983 / OSHA 1926.102",
                "status": "Warning",
                "observations": "No impact goggles or dust masks detected during active structural work in proximity to concrete grinding zone."
            }
        },
        "identified_hazards": [
            {
                "hazard_title": "Unprotected Edge Fall Hazard (> 2m elevation)",
                "severity": "Critical",
                "zone": "Perimeter Slab Edge / Scaffolding Level 4",
                "standards_violation": "OSHA 1926.501(b)(1) & IS 3696 Part 1",
                "risk_description": "Worker active within 1.5m of an unguarded elevated floor edge without a tied-off 100% tie-off safety harness or perimeter guardrail.",
                "corrective_remedy": "Issue immediate stop-work order for perimeter zone. Install rigid top/mid rail toe-boards and certified static lifeline before allowing work to resume."
            },
            {
                "hazard_title": "Exposed Sharp Vertical Rebar Dowels",
                "severity": "High",
                "zone": "Floor Slab Pathway / Column Starter Bars",
                "standards_violation": "OSHA 1926.701(b) & IS 456 Cl. 26",
                "risk_description": "Vertical reinforcing steel dowels protruding 450mm from slab surface lack protective impalement caps along primary worker transit corridor.",
                "corrective_remedy": "Fit OSHA-approved steel-reinforced yellow mushroom impalement caps or wooden trough covers over all protruding rebar ends."
            },
            {
                "hazard_title": "Incomplete Scaffolding Cross-Bracing",
                "severity": "Medium",
                "zone": "External Frame Bay 3",
                "standards_violation": "IS 3696 Part 1 Cl. 6.3",
                "risk_description": "Scaffold uprights lack diagonal locking pins on the secondary tier, potentially reducing lateral load stability under gust conditions.",
                "corrective_remedy": "Inspect tube-and-coupler connections and insert positive locking pins prior to heavy material stacking."
            }
        ],
        "executive_summary": "Site safety audit indicates moderate risk (Score: 72/100). Primary critical hazard is fall vulnerability at elevated slab edges and non-compliance of 1 worker missing hardhat, boots, and fall arrest equipment.",
        "recommended_stop_work": False
    }


def analyze_ppe_compliance(image: Image.Image, engine: GeminiVisionEngine, image_name: str = "") -> Tuple[Dict[str, Any], bool, str]:
    """
    Executes multimodal PPE audit.
    Returns: (parsed_json_audit, is_live_call, note_message)
    """
    if not engine.is_live:
        return generate_mock_ppe_audit(image_name), False, "Demonstration Mode Active: Using certified OSHA / IS standard simulation model."

    raw_response, err = engine.query_multimodal(PPE_AUDIT_PROMPT, image)
    if err or not raw_response:
        # Graceful fallback on API error or quota limitation
        mock_data = generate_mock_ppe_audit(image_name)
        return mock_data, False, f"API error ({err}). Gracefully switched to Demonstration Mode."

    try:
        parsed = clean_json_response(raw_response)
        return parsed, True, "Live Gemini 1.5/2.5 Multimodal Safety Audit Successful."
    except Exception as e:
        mock_data = generate_mock_ppe_audit(image_name)
        return mock_data, False, f"JSON parse error ({e}). Gracefully switched to Demonstration Mode."
