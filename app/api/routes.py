from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    JobOfferRequest, JobOfferAnalysis,
    CompanyRequest, CompanyAnalysis,
    FullAnalysisRequest, FullAnalysis
)
from app.services.llm.groq_client import GroqClient
from app.services.search.duckduckgo_client import DuckDuckGoClient
from app.services.company_analyzer import CompanyAnalyzer

router = APIRouter()
llm_client = GroqClient()
search_client = DuckDuckGoClient()
company_analyzer = CompanyAnalyzer(llm_client, search_client)


@router.post("/analyze", response_model=JobOfferAnalysis)
async def analyze_offer(request: JobOfferRequest):
    try:
        result = llm_client.analyze(request.offer_text)
        return JobOfferAnalysis(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/company", response_model=CompanyAnalysis)
async def analyze_company(request: CompanyRequest):
    try:
        result = company_analyzer.analyze(request.company_name)
        return CompanyAnalysis(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/full", response_model=FullAnalysis)
async def full_analysis(request: FullAnalysisRequest):
    try:
        offer_result = llm_client.analyze(request.offer_text)
        company_result = company_analyzer.analyze(request.company_name)
        
        final_recommendation = (
            "Recommended to apply"
            if offer_result.get("should_apply") and 
            company_result.get("reputation_score") in ["positive", "neutral"]
            else "Not recommended to apply"
        )
        
        return FullAnalysis(
            offer_analysis=JobOfferAnalysis(**offer_result),
            company_analysis=CompanyAnalysis(**company_result),
            final_recommendation=final_recommendation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))