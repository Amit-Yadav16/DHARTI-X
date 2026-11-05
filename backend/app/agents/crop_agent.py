"""
Crop Analysis & Disease Detection Specialist Agent
Focuses on plant health, symptom explanations, and agricultural advisory.
Strictly disallows chemical guessing or inventing pesticide dosages.
Connected with CropVisionService and expert escalation protocols.
"""

from typing import Dict, Any, List, Optional
from app.services.crop_vision_service import CropVisionService

class CropAnalysisAgent:
    def __init__(self, gemini_service=None):
        self.name = "Crop Analysis & Disease Detection Agent"
        self.gemini = gemini_service
        self.sources = [
            "ICAR - Central Rice Research Advisory",
            "Dr. Balasaheb Sawant Konkan Krishi Vidyapeeth (DBSKKV), Dapoli",
            "Krishi Vigyan Kendra (KVK) Kosbad Hill, Palghar"
        ]

    def analyze_query(
        self, 
        query: str, 
        taluka: str = "Palghar", 
        language: str = "en",
        image_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Provides guidance on crop health with structured safety rules and expert escalation.
        """
        # Call the grounded vision/symptom diagnostic engine
        diag = CropVisionService.analyze_crop_sample(
            crop_name="Paddy (Rice)",
            growth_stage="Vegetative / Tillering",
            symptom_notes=query,
            image_base64=image_data
        )

        non_chem_bullets = " ".join([f"• {m}" for m in diag["non_chemical_guidance"]])
        text = (
            f"Screening Analysis for {taluka} ({diag['crop']}):\n"
            f"Primary Indicator: {diag['provisional_diagnosis']} (Confidence: {diag['confidence']})\n"
            f"Observed Symptoms: {diag['visual_symptoms']}\n"
            f"Cultural & Organic Care:\n{non_chem_bullets}\n\n"
            f"Expert Escalation: {diag['expert_escalation']['organization']}, {diag['expert_escalation']['location']} "
            f"(Ph: {diag['expert_escalation']['phone']})."
        )

        return {
            "agent": self.name,
            "text": text,
            "diagnostic_data": diag,
            "sources": self.sources,
            "is_demo": True,
            "disclaimer": diag["disclaimer"]
        }
