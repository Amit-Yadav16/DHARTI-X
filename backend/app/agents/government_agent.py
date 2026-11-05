"""
Government Schemes & Agricultural Law Specialist Agent
Provides verified portal linkages (MahaDBT, PM-KISAN, PMFBY) and dispute guidance without unauthorized legal claims.
Connected with GovernmentKnowledgeService.
"""

from typing import Dict, Any, List
from app.services.government_knowledge_service import GovernmentKnowledgeService

class GovernmentSchemesAgent:
    def __init__(self, gemini_service=None):
        self.name = "Government Schemes & Agricultural Law Agent"
        self.gemini = gemini_service
        self.sources = [
            "MahaDBT Farmer Portal (mahadbt.maharashtra.gov.in)",
            "PM-KISAN Samman Nidhi (pmkisan.gov.in)",
            "Pradhan Mantri Fasal Bima Yojana (pmfby.gov.in)",
            "Maharashtra Agricultural Produce Marketing (Regulation) Act, 1963"
        ]

    def provide_scheme_guidance(self, query: str, taluka: str = "Palghar") -> Dict[str, Any]:
        q = query.lower()

        # Handle grievance / dispute cases
        if any(w in q for w in ["trader", "payment", "apmc", "cheat", "dispute", "patti", "not paid"]):
            disp = GovernmentKnowledgeService.get_dispute_guidance("apmc_delayed_payment")
            steps_text = "\n".join(disp["escalation_steps"])
            text = (
                f"Statutory Guidance for Trader Payment Issues in {taluka}:\n"
                f"Framework: {disp['legal_framework']}\n"
                f"Statutory Timeline: {disp['statutory_period']}\n"
                f"Escalation Pathway:\n{steps_text}\n\n"
                f"{disp['disclaimer']}"
            )
            return {
                "agent": self.name,
                "text": text,
                "sources": self.sources,
                "is_demo": True,
                "disclaimer": disp["disclaimer"]
            }

        # Otherwise list official schemes
        schemes = GovernmentKnowledgeService.get_all_schemes()
        lines = []
        for s in schemes:
            lines.append(f"• {s['name']}: {s['benefit']} (Portal: {s['application_portal']})")
        schemes_summary = "\n".join(lines)

        text = (
            f"Active Government Agricultural Schemes for Palghar Farmers ({taluka}):\n"
            f"{schemes_summary}\n\n"
            f"Note: Applications must be submitted through official government portals. DHARTI-X does not collect payments or personal documents."
        )

        return {
            "agent": self.name,
            "text": text,
            "schemes_list": schemes,
            "sources": self.sources,
            "is_demo": True,
            "disclaimer": "Verify active application cycles and cut-off dates on the respective official portals."
        }
