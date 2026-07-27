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