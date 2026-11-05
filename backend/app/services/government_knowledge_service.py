"""
Government Schemes & Agricultural Law Knowledge Service for DHARTI-X
Maintains a curated repository of official central and Maharashtra state schemes,
eligibility rules, mandatory documents, and APMC grievance escalation pathways.
"""

from typing import Dict, Any, List

class GovernmentKnowledgeService:
    SCHEMES_DB = [
        {
            "id": "mahadbt_irrigation",
            "name": "MahaDBT Micro-Irrigation Subsidy (Drip / Sprinkler)",
            "jurisdiction": "Maharashtra State",
            "implementing_agency": "Department of Agriculture, Government of Maharashtra",
            "benefit": "75% to 80% subsidy for small and marginal farmers on certified drip/sprinkler systems.",
            "target_crops": ["Paddy (Rice)", "Sapota (Chikoo)", "Vegetables", "Flowers"],
            "eligibility": {
                "land_holding": "Up to 5 Acres (2 Hectares) for max subsidy; open to all verified 7/12 holders",
                "required_documents": [
                    "Aadhaar Card linked with bank account",
                    "Latest 7/12 (Satbara) & 8-A land extract",
                    "Electricity bill & water source certificate (well/borewell)"
                ]
            },
            "application_portal": "https://mahadbt.maharashtra.gov.in",
            "is_api": False,
            "verification_contact": "Taluka Agriculture Officer (TAO) / Krishi Sahayak"
        },
        {
            "id": "pm_kisan_namo",
            "name": "PM-KISAN + Namo Shetkari Mahasanman Nidhi",
            "jurisdiction": "Central + Maharashtra Joint Assistance",
            "implementing_agency": "Ministry of Agriculture & Farmers Welfare + GoM",
            "benefit": "₹12,000 per year (₹6,000 Central PM-KISAN + ₹6,000 Maharashtra Namo Shetkari) via direct bank transfer.",
            "target_crops": ["All agricultural landholders"],
            "eligibility": {
                "land_holding": "Cultivable landholding in farmer's name",
                "required_documents": [
                    "e-KYC verified Aadhaar",
                    "Aadhaar-seeded bank account with active NPCI mapping",
                    "Land mutation extract (7/12 with farmer's name)"
                ]
            },
            "application_portal": "https://pmkisan.gov.in",
            "is_api": False,
            "verification_contact": "Village Krishi Mitra / CSC VLE Centre"
        },
        {
            "id": "pmfby_one_rupee",
            "name": "Pradhan Mantri Fasal Bima Yojana (Maharashtra ₹1 Scheme)",
            "jurisdiction": "Maharashtra State",
            "implementing_agency": "Maharashtra State Agri Insurance Cell",
            "benefit": "Kharif and Rabi crop insurance with farmer paying only ₹1 token premium; remaining premium subsidized by government.",
            "target_crops": ["Paddy (Rice)", "Nachani (Ragi)", "Urad", "Moong"],
            "eligibility": {
                "land_holding": "Loanee and Non-loanee farmers owning cultivable land in notified revenue circles",
                "required_documents": [
                    "Crop sowing declaration certificate (Pik Perni Nond)",
                    "Aadhaar card",
                    "Bank passbook copy with IFSC"
                ]
            },
            "application_portal": "https://pmfby.gov.in",
            "is_api": False,
            "verification_contact": "District Agriculture Officer (DAO), Palghar"
        }
    ]

    DISPUTE_ESCALATION = {
        "apmc_delayed_payment": {
            "title": "Delayed Payment by APMC Commission Agent / Trader",
            "legal_framework": "Maharashtra Agricultural Produce Marketing (Development and Regulation) Act, 1963",
            "statutory_period": "Payment must be settled within 24 hours of sale on the market yard.",
            "escalation_steps": [
                "1. Lodge a written complaint with the APMC Secretary, Palghar / Dahanu / Wada along with the original sale receipt (Patti).",
                "2. If unresolved within 7 days, appeal to the District Deputy Registrar (DDR) Cooperative Societies, Palghar.",
                "3. The DDR holds statutory powers to attach the trader's bank guarantee or cancel their market license."
            ],
            "disclaimer": "This is procedural guidance. Consult the Palghar District Legal Services Authority or an advocate for formal legal dispute filing."
        }
    }

    @classmethod
    def get_all_schemes(cls) -> List[Dict[str, Any]]:
        return cls.SCHEMES_DB

    @classmethod
    def get_dispute_guidance(cls, topic: str = "apmc_delayed_payment") -> Dict[str, Any]:
        return cls.DISPUTE_ESCALATION.get(topic, cls.DISPUTE_ESCALATION["apmc_delayed_payment"])

