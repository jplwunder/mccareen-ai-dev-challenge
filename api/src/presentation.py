from fastapi import APIRouter, Query
from pydantic import BaseModel, HttpUrl
from typing import List

from api.src import service

# Requests ----------------------------------------


class WebsiteAnalysisRequest(BaseModel):
    website_url: HttpUrl


# Responses ---------------------------------------


class CompanyProfile(BaseModel):
    company_name: str
    service_lines: List[str] | str
    company_description: str
    tier1_keywords: List[str] | str
    tier2_keywords: List[str] | str
    emails: List[str] | str
    point_of_contact: List[str] | str


# Routes ----------------------------------------

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Company Profile Generator API", "version": "1.0.0"}


@router.get("/health")
async def health_check():
    return {"status": "healthy"}


@router.post("/analyze-website", response_model=CompanyProfile)
async def analyze_website(website_url: HttpUrl = Query(..., description="Website URL to analyze")):
    company_profile = await service.analyze_website(website_url)
    return CompanyProfile(**company_profile)
