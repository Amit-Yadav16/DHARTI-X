"""
DHARTI-X FastAPI Backend
Multi-Agent Agricultural Intelligence Platform for Palghar, Maharashtra
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from app.agents.master_agent import MasterAgricultureAgent
from app.services.weather_service import WeatherService, PALGHAR_TALUKA_COORDS
from app.services.mandi_service import MandiService
from app.services.crop_vision_service import CropVisionService
from app.services.government_knowledge_service import GovernmentKnowledgeService

app = FastAPI(
    title="DHARTI-X Backend API",
    description="Multi-Agent API supporting Crop Health, Weather, Financial Planning, and Government Schemes for Palghar, Maharashtra.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

master_agent = MasterAgricultureAgent()

class ChatRequest(BaseModel):
    query: str
    taluka: Optional[str] = "Palghar"
    language: Optional[str] = "en"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    routed_agent: str
    response_text: str
    citations: List[str]
    is_demo: bool
    disclaimer: Optional[str] = None

class CropDiagnoseRequest(BaseModel):
    crop_name: str = "Rice (Paddy)"
    growth_stage: str = "Vegetative / Tillering"
    symptom_notes: str
    image_base64: Optional[str] = None

@app.get("/")
def read_root():
    return {
        "platform": "DHARTI-X",
        "tagline": "Intelligence Rooted in Nature",
        "geography": "Palghar District, Maharashtra",
        "status": "Ready",
        "environment": "MVP Phase 5 & 6 (Crop Diagnostic Vision & Schemes Engine)",
        "supported_talukas": [t["name"] for t in PALGHAR_TALUKA_COORDS.values()]
    }

@app.get("/api/weather")
async def get_weather(taluka: str = Query("Palghar", description="Palghar district taluka name")):
    """
    Returns live weather telemetry and daily forecast using verified Open-Meteo Palghar coordinates.
    """
    return await WeatherService.get_forecast(taluka)

@app.get("/api/finance/scenarios")
def get_crop_scenarios(
    crop: str = Query("rice", description="Crop key: rice, nachani, sapota"),
    acreage: float = Query(2.0, ge=0.5, le=50.0, description="Cultivation acreage")
):
    """
    Returns deterministic Low / Expected / High economics and input cost breakdown.
    """
    return MandiService.calculate_scenario_economics(crop, acreage)

@app.post("/api/crop/diagnose")
def diagnose_crop_symptoms(req: CropDiagnoseRequest):
    """
    Evaluates plant health symptoms and triggers expert escalation to KVK Kosbad Hill.
    """
    return CropVisionService.analyze_crop_sample(
        crop_name=req.crop_name,
        growth_stage=req.growth_stage,
        symptom_notes=req.symptom_notes,
        image_base64=req.image_base64
    )

@app.get("/api/schemes")
def list_government_schemes():
    """
    Returns curated official schemes (MahaDBT, PM-KISAN, PMFBY).
    """
    return GovernmentKnowledgeService.get_all_schemes()

@app.get("/api/schemes/dispute")
def get_dispute_escalation(topic: str = "apmc_delayed_payment"):
    """
    Returns statutory grievance guidelines under the Maharashtra APMC Act, 1963.
    """
    return GovernmentKnowledgeService.get_dispute_guidance(topic)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_handler(req: ChatRequest):
    """
    Master Agent Intent Routing:
    Delegates to the appropriate specialist agent with token-saving single dispatch.
    """
    result = await master_agent.process_query(
        query=req.query,
        taluka=req.taluka or "Palghar",
        language=req.language or "en"
    )
    return ChatResponse(**result)
