from pydantic import BaseModel
from typing import Optional

class JobOfferRequest(BaseModel):
    offer_text: str

class JobOfferAnalysis(BaseModel):
    should_apply: bool
    reasons: list[str]
    summary: str
    red_flags: list[str]
    salary_info: Optional[str] = None

class CompanyRequest(BaseModel):
    company_name: str

class CompanyAnalysis(BaseModel):
    company_name: str
    reputation_score: str  # "positive", "neutral", "negative", "unknown"
    summary: str
    red_flags: list[str]
    positive_signals: list[str]
    sources_consulted: list[str]

class FullAnalysisRequest(BaseModel):
    offer_text: str
    company_name: str

class FullAnalysis(BaseModel):
    offer_analysis: JobOfferAnalysis
    company_analysis: CompanyAnalysis
    final_recommendation: str