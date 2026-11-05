"""
Master Agriculture Agent for DHARTI-X
Coordinates intent routing across the four specialist agents.
Implements token saving: only calls the necessary specialist agent.
"""

from typing import Dict, Any, List
from app.services.gemini_service import GeminiService
from app.agents.crop_agent import CropAnalysisAgent
from app.agents.weather_agent import WeatherInformationAgent
from app.agents.financial_agent import FinancialPlanningAgent
from app.agents.government_agent import GovernmentSchemesAgent

class MasterAgricultureAgent:
    def __init__(self):
        self.agent_name = "DHARTI-X Master Agriculture Agent"
        self.gemini = GeminiService()
        self.crop_agent = CropAnalysisAgent(self.gemini)
        self.weather_agent = WeatherInformationAgent(self.gemini)
        self.financial_agent = FinancialPlanningAgent(self.gemini)
        self.government_agent = GovernmentSchemesAgent(self.gemini)

    async def process_query(self, query: str, taluka: str = "Palghar", language: str = "en") -> Dict[str, Any]:
        """
        Token-saving selective routing:
        Analyzes the farmer query and determines which single specialist agent should answer.
        """
        q = query.lower()

        # 1. Weather Intent
        if any(w in q for w in ["weather", "rain", "temperature", "hawa", "cyclone", "humidity", "pani"]):
            res = await self.weather_agent.get_weather_advisory(taluka, query)
            return {
                "routed_agent": self.weather_agent.name,
                "response_text": res["text"],
                "citations": res["sources"],
                "is_demo": res["is_demo"],
                "disclaimer": res.get("disclaimer")
            }

        # 2. Crop Health & Disease Intent
        elif any(w in q for w in ["leaf", "yellow", "pest", "disease", "fungus", "spot", "insect", "keeda", "rice", "paddy"]):
            res = self.crop_agent.analyze_query(query, taluka, language)
            return {
                "routed_agent": self.crop_agent.name,
                "response_text": res["text"],
                "citations": res["sources"],
                "is_demo": res["is_demo"],
                "disclaimer": res.get("disclaimer")
            }

        # 3. Financial & Mandi Economics Intent
        elif any(w in q for w in ["cost", "profit", "mandi", "price", "bhav", "yield", "roi", "income", "kharch"]):
            res = self.financial_agent.evaluate_economics(crop="rice", acreage=2.0, query=query)
            return {
                "routed_agent": self.financial_agent.name,
                "response_text": res["text"],
                "citations": res["sources"],
                "is_demo": res["is_demo"],
                "disclaimer": res.get("disclaimer")
            }

        # 4. Government Schemes & Rights Intent (Default)
        else:
            res = self.government_agent.provide_scheme_guidance(query, taluka)
            return {
                "routed_agent": self.government_agent.name,
                "response_text": res["text"],
                "citations": res["sources"],
                "is_demo": res["is_demo"],
                "disclaimer": res.get("disclaimer")
            }
