"""
Daily Site Assistant & Weather-Aware Advisory Module (Epic 5)
Provides weather-driven dynamic safety protocols (crane shutdown, concrete curing,
electrical de-energization) and an interactive civil/structural AI engineering chatbot.
"""

from typing import Dict, Any, List
from modules.gemini_client import GeminiVisionEngine

WEATHER_PROTOCOLS = {
    "High Wind (> 45 km/h / Gale)": {
        "status_level": "CRITICAL DANGER",
        "css_class": "alert-danger",
        "icon": "🌪️",
        "headline": "MANDATORY HIGH WIND PROTOCOL: Suspend All Crane & Height Operations",
        "osha_is_code": "OSHA 1926.1431 / IS 456 / IS 875 Part 3",
        "action_items": [
            "TOWER CRANE LOCKDOWN: Immediately suspend all tower crane hook lifting operations. Release slewing brake to allow crane arm to weathervane safely with wind direction.",
            "SUSPENDED CRADLES & BMUs: Lower all facade suspended platforms, mast climbers, and gondolas to ground anchor level; lash securely.",
            "LOOSE SHEET ANCHORAGE: Secure or weight down all corrugated metal roof sheets, plywood shuttering panels, and tarpaulins.",
            "PERIMETER WORK HALT: Evacuate all personnel working on scaffolding platforms above 3 storeys."
        ],
        "concrete_protocol": "Shield newly poured slabs with windbreak canvas to prevent high-rate surface evaporation causing severe plastic shrinkage cracking."
    },
    "Heavy Rain / Monsoon Storm": {
        "status_level": "SEVERE HAZARD",
        "css_class": "alert-danger",
        "icon": "⛈️",
        "headline": "MONSOON FLOODING & ELECTRICAL WARNING: Active Dewatering Required",
        "osha_is_code": "IS 3764 (Excavation Safety) / OSHA 1926.404 (Electrical Grounding)",
        "action_items": [
            "CONCRETE POUR STOP: Immediately cease external structural slab casting. Rainwater alters water-cement ratio, drastically dropping characteristic compressive strength.",
            "ELECTRICAL DE-ENERGIZATION: De-energize temporary 415V distribution boxes in lower basements and waterlogged zones. Test all ELCB/RCCB earth leakage trips.",
            "TRENCH & FOUNDATION STABILITY: Inspect deep retaining cuts and diaphragm walls for hydrostatic pore pressure build-up and toe slope slumping.",
            "CONTINUOUS PUMPING: Activate diesel standby dewatering sump pumps in lift pits and basements."
        ],
        "concrete_protocol": "Cover unhardened concrete surfaces immediately with heavy polythene sheeting (minimum 250 microns) to prevent cement paste washout."
    },
    "Extreme Heat (> 40°C / Heat Wave)": {
        "status_level": "MODERATE WARNING",
        "css_class": "alert-warning",
        "icon": "☀️",
        "headline": "HOT WEATHER CONCRETING PROTOCOL: IS 7861 Part 1 Compliance Mandatory",
        "osha_is_code": "IS 7861 Part 1 (Extreme Weather Concreting) / OSHA Heat Safety Standard",
        "action_items": [
            "CONCRETE TEMPERATURE CONTROL: Ensure fresh concrete placement temperature does not exceed 32°C. Use chilled mixing water or flaked ice substitution.",
            "HYDRATION RETARDERS: Dose admixture with ASTM C494 Type D/G set-retarding plasticizers to maintain slump workability during transit.",
            "POND CURING: Initiate wet hessian burlap wrapping followed by ponding within 2 hours of initial set; maintain wet curing for minimum 14 days.",
            "WORKER HEAT MITIGATION: Mandatory 15-minute hydration breaks every 45 minutes with oral rehydration salts (ORS) in shaded rest shelters."
        ],
        "concrete_protocol": "Schedule heavy mass structural pours during evening or night shifts (after 18:00 hrs) to minimize peak heat of hydration thermal cracking."
    },
    "Dense Fog / Dust Storm (< 50m Visibility)": {
        "status_level": "CAUTION PROTOCOL",
        "css_class": "alert-info",
        "icon": "🌫️",
        "headline": "POOR VISIBILITY PROTOCOL: Restrict Earthmoving & Blind Lifting",
        "osha_is_code": "OSHA 1926.1419 (Crane Signals) / IS 7293",
        "action_items": [
            "BLIND LIFTS PROHIBITED: Crane operators must not perform any picks without direct radio-linked certified signal persons (Rigger Level 2).",
            "TRANSIT SPEED LIMIT: Reduce speed limit of dump trucks, transit mixers, and backhoes to 10 km/h across the site.",
            "HIGH-INTENSITY BEACONS: Turn on strobe beacons and high-visibility illuminated vests for all marshals and banksmen.",
            "RESPIRATORY PROTECTION: Distribute N95/FFP2 particulate respirators to all workers in dust-entrained zones."
        ],
        "concrete_protocol": "Inspect surface moisture condensation on cold formwork surfaces before pouring to prevent interfacial honeycombing."
    },
    "Normal / Favorable (24°C - 30°C Clear)": {
        "status_level": "OPTIMAL CONDITIONS",
        "css_class": "alert-success",
        "icon": "🌤️",
        "headline": "FULL SPEED OPERATIONS: Optimal Production Window",
        "osha_is_code": "Standard IS 456:2000 Operating Protocols",
        "action_items": [
            "PRIORITY TASKS: Ideal conditions for high-precision structural concrete pours, precast panel erection, and facade exterior glazing.",
            "STANDARD PPE: Enforce regular 100% hardhat, high-vis vest, and safety shoe compliance across all active zones.",
            "SCAFFOLDING AUDIT: Execute scheduled weekly green-tag scaffold inspections.",
            "MATERIAL LOGISTICS: Expedite bulk delivery of TMT rebar bundles and cement trailers."
        ],
        "concrete_protocol": "Standard IS 456 curing: Apply continuous water sprinkling or membrane curing compound for standard 7-day curing cycle."
    }
}

CONSTRUCTION_EXPERT_SYSTEM_PROMPT = """
You are the Chief Construction Engineer, Quality Assurance Auditor, and Site Safety Director for a Tier-1 infrastructure and real estate conglomerate.
You possess deep expertise in:
- Bureau of Indian Standards: IS 456:2000 (Plain and Reinforced Concrete), IS 1893:2016 (Earthquake Design), IS 875:2015 (Wind & Gravity Loads), IS 3696 (Scaffolding Safety), IS 7861 (Hot/Cold Concreting), NBC 2016 (National Building Code of India).
- International Standards: OSHA 1926 Construction Safety Regulations, ACI 318, ACI 224R.
- Practical Site Engineering: Slump tests, cube testing (7-day and 28-day target mean strength $f_{ck}$), formwork stripping time, rebar lap length calculation ($50d$), cover blocks, micro-silica and fly-ash mix designs, tower crane operations, structural repairs (epoxy injection, micro-concrete jacketing).

Guidelines for your responses:
1. Provide authoritative, concise, and mathematically rigorous engineering explanations.
2. Quote relevant IS Codes or OSHA clauses whenever answering structural or safety questions.
3. Include numerical benchmarks (e.g. permissible crack widths, curing days, concrete cover thickness).
4. Maintain a professional, constructive tone suitable for project managers and site engineers.
"""

# Offline knowledge base responses for demonstration mode
DEMO_CHAT_KNOWLEDGE = {
    "wind": (
        "**Tower Crane Wind Cutoff Protocol (OSHA 1926.1431 & IS 456):**\n\n"
        "1. **Operational Limit:** Most standard hammerhead and luffing-jib tower cranes must cease lifting operations when sustained wind speeds exceed **38 km/h to 45 km/h** (approx. 20 knots / 10-12 m/s), or manufacturer-specified gust limits.\n"
        "2. **Critical Shutdown (> 45 km/h):**\n"
        "   - Slew brake MUST be released into free-wheeling (weathervane) mode so the jib rotates freely with the wind without inducing catastrophic torsional stress on the mast section.\n"
        "   - Trolley brought in close to the mast and hook block raised to the highest mechanical limit stop.\n"
        "3. **Regulatory Reference:** IS 875 (Part 3) Wind Loads on Structures & OSHA 1926.1431 Subpart CC."
    ),
    "heat": (
        "**Hot Weather Concrete Placement Protocol (IS 7861 Part 1:1975):**\n\n"
        "When ambient temperature exceeds 38°C - 40°C, the rate of cement hydration accelerates drastically, leading to premature slump loss, thermal micro-cracking, and lower ultimate 28-day compressive strength.\n\n"
        "**Mandatory Site Measures:**\n"
        "1. **Concrete Temperature Control:** Keep fresh concrete placement temp below **32°C**. Substitute 20-30% of mixing water with crushed flaked ice.\n"
        "2. **Chemical Admixtures:** Use IS 9103 compliant Type D/G set-retarding plasticizers to maintain slump for 90 minutes.\n"
        "3. **Pre-wetting:** Drench formwork and rebar cages with chilled water mist immediately before pouring.\n"
        "4. **Curing:** Begin wet burlap curing as soon as surface finishing permits, preventing plastic shrinkage fissures."
    ),
    "crack": (
        "**Permissible Crack Width Limits under IS 456:2000 (Clause 35.3.2):**\n\n"
        "- **Mild Exposure (Indoor/Protected):** Maximum allowable crack width is **0.30 mm**.\n"
        "- **Moderate to Severe Exposure (Exterior/Rain/Coastal):** Maximum allowable width is **0.20 mm**.\n"
        "- **Critical / Water-Retaining Structures (IS 3370):** Maximum allowable width is **0.10 mm** to ensure water-tightness.\n\n"
        "If a structural shear crack exceeds 0.3mm in a beam or column, it represents an ultimate limit state serviceability failure requiring immediate structural propping, core testing, and low-pressure epoxy injection or CFRP jacketing."
    ),
    "cover": (
        "**Nominal Concrete Cover Requirements (IS 456:2000 Table 16 & Cl. 26.4):**\n\n"
        "- **Footings (Foundations):** 50 mm minimum\n"
        "- **Columns:** 40 mm (or not less than main longitudinal bar diameter)\n"
        "- **Beams:** 25 mm minimum\n"
        "- **Slabs:** 20 mm minimum (15 mm for mild exposure)\n"
        "- **Severe / Coastal Exposure:** Increase cover by 15-20 mm or use anti-carbonation coatings."
    )
}


def get_weather_advisory(condition_key: str) -> Dict[str, Any]:
    """Retrieves the protocol dictionary for selected weather condition."""
    return WEATHER_PROTOCOLS.get(condition_key, WEATHER_PROTOCOLS["Normal / Favorable (24°C - 30°C Clear)"])


def answer_engineering_query(
    user_query: str,
    chat_history: List[Dict[str, str]],
    engine: GeminiVisionEngine
) -> str:
    """
    Answers construction engineering queries using Gemini LLM with domain system prompt,
    or falls back to high-fidelity engineering answers if in demo mode.
    """
    if engine.is_live:
        context_prompt = f"User Question: {user_query}\nProvide an authoritative engineering response referencing IS codes and OSHA."
        res, err = engine.query_text(context_prompt, system_instruction=CONSTRUCTION_EXPERT_SYSTEM_PROMPT)
        if res and not err:
            return res

    # Offline Demonstration Mode fallback
    q_lower = user_query.lower()
    if "wind" in q_lower or "crane" in q_lower:
        return DEMO_CHAT_KNOWLEDGE["wind"]
    elif "heat" in q_lower or "curing" in q_lower or "summer" in q_lower or "temperature" in q_lower:
        return DEMO_CHAT_KNOWLEDGE["heat"]
    elif "crack" in q_lower or "width" in q_lower or "shear" in q_lower:
        return DEMO_CHAT_KNOWLEDGE["crack"]
    elif "cover" in q_lower or "column" in q_lower or "slab" in q_lower or "rebar" in q_lower:
        return DEMO_CHAT_KNOWLEDGE["cover"]
    else:
        return (
            f"**Site Engineer AI Advisory (Demonstration Mode):**\n\n"
            f"Regarding your query on: *'{user_query}'*:\n\n"
            f"- **Structural Standard Compliance:** All reinforced concrete operations must be executed as per **IS 456:2000** (Code of practice for plain and reinforced concrete) and ductile detailing in seismic zones conforming to **IS 13920:2016**.\n"
            f"- **Safety Mandate:** As per **OSHA 1926.501** and **IS 3696**, any work performed at an elevation greater than 2.0 meters requires 100% fall protection with certified anchorage capable of supporting 22.2 kN (5,000 lbs).\n"
            f"- **Quality Control:** Ensure minimum 3 concrete cubes are cast for every 15 $m^3$ of ready-mix concrete batch for 7-day and 28-day compressive strength testing.\n\n"
            f"*Tip: Configure your Gemini API key in the sidebar for real-time generative responses to arbitrary engineering scenarios.*"
        )
