"""
Pollinations AI & Flux Architectural 3D Rendering Integration
Generates photorealistic architectural concept prompts and streams AI renderings.
"""

import urllib.parse
import hashlib
from typing import Dict, Any

def build_architectural_prompt(
    structure_type: str,
    location_tier: str,
    quality_grade: str,
    completion_percentage: float
) -> str:
    """
    Constructs an evocative architectural visualization prompt tailored for Flux / SDXL models.
    """
    tier_city = "Mumbai skyline" if "Tier 1" in location_tier else ("Pune tech hub" if "Tier 2" in location_tier else "modern Indian smart city")
    
    stage_desc = ""
    if completion_percentage < 30:
        stage_desc = "construction in early structural framing phase, tower cranes silhouetted, exposed reinforced concrete columns"
    elif completion_percentage < 75:
        stage_desc = "active construction phase with glistening curtain wall glazing being fitted, scaffolding on upper tiers"
    else:
        stage_desc = "near-complete luxury facade, architectural LED uplighting, manicured green landscape podium"

    prompt = (
        f"Masterpiece 3D architectural rendering of a {quality_grade.lower()} {structure_type} in {tier_city}, "
        f"{stage_desc}, dramatic golden hour volumetric lighting, cinematic wide angle view, "
        f"unreal engine 5 octane render, photorealistic, 8k resolution, crisp architectural details, "
        f"hyperdetailed concrete and glass textures, lush Indian tropical landscaping"
    )
    return prompt


def get_pollinations_image_url(
    prompt: str,
    width: int = 1024,
    height: int = 600,
    model: str = "flux",
    seed: int = 42
) -> str:
    """
    Builds the direct Pollinations.ai image endpoint URL.
    """
    # Deterministic seed based on prompt
    prompt_hash = int(hashlib.md5(prompt.encode('utf-8')).hexdigest()[:8], 16) % 100000
    encoded_prompt = urllib.parse.quote(prompt.strip())
    
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model={model}&seed={prompt_hash}&nologo=true"
    return url
