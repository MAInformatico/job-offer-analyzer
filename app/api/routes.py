from fastapi import APIRouter, HTTPException
from app.models.schemas import JobOfferRequest, JobOfferAnalysis
from app.services.llm.groq_client import GroqClient

router = APIRouter()
llm_client = GroqClient()

@router.post("/analyze", response_model=JobOfferAnalysis)
async def analyze_offer(request: JobOfferRequest):
    try:
        result = llm_client.analyze(request.offer_text)
        return JobOfferAnalysis(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))