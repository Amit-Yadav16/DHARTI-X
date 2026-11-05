"""
Financial & Crop Planning Specialist Agent
Provides deterministic farmgate economics, APMC mandi modal analysis, and transparent calculations.
Supports Low, Expected, and High agricultural scenarios.
"""

from typing import Dict, Any
from app.services.mandi_service import MandiService

class FinancialPlanningAgent:
    def __init__(self, gemini_service=None):
        self.name = "Financial & Crop Planning Agent"
        self.gemini = gemini_service
        self.sources = [
            "Agmarknet Palghar APMC Benchmark (Sample Reference)",
            "Maharashtra Department of Agriculture Cost of Cultivation Cell"
        ]

    def evaluate_economics(self, crop: str = "rice", acreage: float = 2.0, query: str = "") -> Dict[str, Any]:
        data = MandiService.calculate_scenario_economics(crop, acreage)
        exp = data["scenarios"]["expected"]
        low = data["scenarios"]["low"]
        high = data["scenarios"]["high"]

        text = (
            f"Scenario Analysis for {data['crop']} ({acreage} Acres) in Palghar:\n"
            f"• Expected Scenario: ₹{exp['mandi_price_rs_per_quintal']}/q modal price, {exp['total_yield_quintals']}q yield &rarr; Net Margin ₹{exp['net_profit_rs']:,} (ROI: {exp['roi_percentage']}%)\n"
            f"• Low Yield/Price Scenario: ₹{low['mandi_price_rs_per_quintal']}/q, {low['total_yield_quintals']}q &rarr; Net Margin ₹{low['net_profit_rs']:,} (ROI: {low['roi_percentage']}%)\n"
            f"• High Yield/Price Scenario: ₹{high['mandi_price_rs_per_quintal']}/q, {high['total_yield_quintals']}q &rarr; Net Margin ₹{high['net_profit_rs']:,} (ROI: {high['roi_percentage']}%)\n"
            f"Total benchmark input cost across {acreage} acres: ₹{data['total_cultivation_cost_rs']:,} (Break-even: ~₹{exp['break_even_price_per_quintal_rs']}/quintal)."
        )

        return {
            "agent": self.name,
            "text": text,
            "scenario_data": data,
            "sources": self.sources,
            "is_demo": True,
            "disclaimer": "Mandi rates fluctuate daily based on grade, moisture, and market arrivals. Not a legally guaranteed price."
        }
