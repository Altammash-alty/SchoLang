from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from local_llm.summarisation import summarise_paper
from cache.redis_client import get_cached_summary, set_cached_summary


class SummariseRequest(BaseModel):
    doi:      Optional[str] = None
    abstract: str
    language: str             = "en"


router=APIRouter()

@router.post("/summarise")
async def summarise(request: SummariseRequest):
    if request.doi:
        cached = await get_cached_summary(request.doi, request.language)
        if cached:
            return {"source": "cache", "summary": cached}
    if not request.abstract:
        raise HTTPException(status_code=400, detail="Abstract is required for summarisation")
    summary = await summarise_paper(request.abstract, request.language)
    if request.doi and summary["summary"]:
        await set_cached_summary(request.doi, request.language, summary)
    return {"source": "claude", "summary": summary}
