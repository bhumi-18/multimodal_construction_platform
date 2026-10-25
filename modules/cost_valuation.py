"""
Project Planning & Real Estate Valuation Module (Epic 3)
Calculates construction budgets, incurred CapEx, material quantities (Steel, Cement, Concrete),
and current market asset valuation in INR (₹ Lakhs & ₹ Crores) for Tier 1/2/3 Indian cities.
"""

from typing import Dict, Any, Tuple

# Baseline construction cost per sq. ft. in INR based on Tier & Construction Grade
COST_MATRIX_PER_SQFT = {
    "Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Chennai, Hyderabad)": {
        "Economy / Standard": 2250,
        "Premium": 3400,
        "Ultra-Luxury / High-Tech": 5200
    },
    "Tier 2 (Pune, Ahmedabad, Kolkata, Kochi, Jaipur, Chandigarh)": {
        "Economy / Standard": 1850,
        "Premium": 2800,
        "Ultra-Luxury / High-Tech": 4100
    },
    "Tier 3 (Coimbatore, Indore, Vadodara, Bhubaneswar, Nagpur, Jaipur)": {
        "Economy / Standard": 1550,
        "Premium": 2300,
        "Ultra-Luxury / High-Tech": 3400
    }
}

# Average finished market sale / asset value rate per sq. ft. in INR based on Tier & Grade
MARKET_VALUATION_RATE_PER_SQFT = {
    "Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Chennai, Hyderabad)": {
        "Economy / Standard": 9500,
        "Premium": 16500,
        "Ultra-Luxury / High-Tech": 28000
    },
    "Tier 2 (Pune, Ahmedabad, Kolkata, Kochi, Jaipur, Chandigarh)": {
        "Economy / Standard": 5500,
        "Premium": 8500,
        "Ultra-Luxury / High-Tech": 14000
    },
    "Tier 3 (Coimbatore, Indore, Vadodara, Bhubaneswar, Nagpur, Jaipur)": {
        "Economy / Standard": 3600,
        "Premium": 5200,
        "Ultra-Luxury / High-Tech": 8500
    }
}

# Multipliers based on structure type
STRUCTURE_MULTIPLIERS = {
    "Residential High-Rise (G+25 Floors)": {
        "cost_factor": 1.15,
        "steel_kg_per_sqft": 4.5,
        "cement_bags_per_sqft": 0.44,
        "concrete_cum_per_sqft": 0.038
    },
    "Commercial IT Park / Grade-A Office": {
        "cost_factor": 1.25,
        "steel_kg_per_sqft": 4.8,
        "cement_bags_per_sqft": 0.46,
        "concrete_cum_per_sqft": 0.040
    },
    "Industrial Warehouse / PEB Structure": {
        "cost_factor": 0.85,
        "steel_kg_per_sqft": 3.2,
        "cement_bags_per_sqft": 0.28,
        "concrete_cum_per_sqft": 0.024
    },
    "Luxury Villa Community": {
        "cost_factor": 1.10,
        "steel_kg_per_sqft": 3.8,
        "cement_bags_per_sqft": 0.40,
        "concrete_cum_per_sqft": 0.032
    },
    "Institutional / Multi-Specialty Hospital": {
        "cost_factor": 1.35,
        "steel_kg_per_sqft": 5.2,
        "cement_bags_per_sqft": 0.48,
        "concrete_cum_per_sqft": 0.042
    }
}


def format_inr(amount_inr: float) -> Tuple[str, str]:
    """
    Formats a numeric INR amount into Indian Lakhs (L) and Crores (Cr).
    Returns (formatted_string, unit_label)
    e.g. format_inr(14500000) -> ("₹ 1.45 Cr", "Crores")
    """
    if amount_inr >= 10000000:  # >= 1 Crore
        crores = amount_inr / 10000000
        return f"₹ {crores:,.2f} Cr", "Crores"
    elif amount_inr >= 100000:  # >= 1 Lakh
        lakhs = amount_inr / 100000
        return f"₹ {lakhs:,.2f} L", "Lakhs"
    else:
        return f"₹ {amount_inr:,.0f}", "Rupees"


def calculate_project_metrics(
    structure_type: str,
    built_up_sqft: float,
    location_tier: str,
    quality_grade: str,
    completion_percentage: float
) -> Dict[str, Any]:
    """
    Calculates detailed project budgets, CapEx incurred, asset valuation,
    and material requirements for Indian construction context.
    """
    # 1. Base rates and factors
    base_cost_rate = COST_MATRIX_PER_SQFT.get(location_tier, {}).get(quality_grade, 2500)
    structure_specs = STRUCTURE_MULTIPLIERS.get(structure_type, {
        "cost_factor": 1.0,
        "steel_kg_per_sqft": 4.0,
        "cement_bags_per_sqft": 0.4,
        "concrete_cum_per_sqft": 0.035
    })
    
    effective_cost_rate = base_cost_rate * structure_specs["cost_factor"]
    
    # Total Construction Cost (Budget)
    total_budget_inr = built_up_sqft * effective_cost_rate
    
    # CapEx incurred based on progress percentage
    capex_incurred_inr = total_budget_inr * (completion_percentage / 100.0)
    
    # Contingency & Statutory Approvals (typically 6% of budget)
    contingency_inr = total_budget_inr * 0.06
    
    # Total Project Value at Completion
    market_sale_rate = MARKET_VALUATION_RATE_PER_SQFT.get(location_tier, {}).get(quality_grade, 8000)
    completed_asset_valuation_inr = built_up_sqft * market_sale_rate
    
    # Current Asset Valuation (reflecting land equity + construction WIP + appreciation)
    # Land cost component is typically 35-50% of finished value in Indian urban markets
    land_equity_base = completed_asset_valuation_inr * 0.38
    wip_added_value = (completed_asset_valuation_inr - land_equity_base) * (completion_percentage / 100.0) * 0.95
    current_asset_valuation_inr = land_equity_base + wip_added_value
    
    # Materials Estimation
    steel_tonnes = (built_up_sqft * structure_specs["steel_kg_per_sqft"]) / 1000.0  # kg to metric tonnes
    cement_bags = built_up_sqft * structure_specs["cement_bags_per_sqft"]            # 50kg bags
    concrete_cum = built_up_sqft * structure_specs["concrete_cum_per_sqft"]          # cubic meters (m3)
    
    # Milestone Stages calculation
    stages = [
        {"name": "Substructure & Foundation", "weight": 20, "completed": min(100.0, completion_percentage * (100 / 20))},
        {"name": "RCC Superstructure & Framing", "weight": 35, "completed": max(0.0, min(100.0, (completion_percentage - 20) * (100 / 35)))},
        {"name": "Masonry, MEP & Firefighting", "weight": 25, "completed": max(0.0, min(100.0, (completion_percentage - 55) * (100 / 25)))},
        {"name": "Finishing, Facade & Handover", "weight": 20, "completed": max(0.0, min(100.0, (completion_percentage - 80) * (100 / 20)))}
    ]
    
    total_budget_str, total_budget_unit = format_inr(total_budget_inr)
    capex_str, capex_unit = format_inr(capex_incurred_inr)
    valuation_str, valuation_unit = format_inr(current_asset_valuation_inr)
    completed_val_str, _ = format_inr(completed_asset_valuation_inr)

    return {
        "built_up_sqft": built_up_sqft,
        "effective_cost_rate_per_sqft": effective_cost_rate,
        "market_sale_rate_per_sqft": market_sale_rate,
        "total_budget_inr": total_budget_inr,
        "total_budget_formatted": total_budget_str,
        "capex_incurred_inr": capex_incurred_inr,
        "capex_incurred_formatted": capex_str,
        "current_asset_valuation_inr": current_asset_valuation_inr,
        "current_asset_valuation_formatted": valuation_str,
        "completed_asset_valuation_formatted": completed_val_str,
        "contingency_inr": contingency_inr,
        "completion_percentage": completion_percentage,
        "materials": {
            "steel_tonnes": round(steel_tonnes, 1),
            "cement_bags": int(round(cement_bags)),
            "concrete_cum": round(concrete_cum, 1),
            "sand_cum": round(concrete_cum * 0.45, 1),
            "aggregate_cum": round(concrete_cum * 0.85, 1)
        },
        "stages": stages
    }
