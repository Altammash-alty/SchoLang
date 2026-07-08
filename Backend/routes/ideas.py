from fastapi import APIRouter, HTTPException
from ..models.model import IdeasRequest
#from ..services.claude_services import generate_ideas
from ..local_llm.idea_gen import generate_ideas
from ..cache.redis_client import get_cached_ideas, set_cached_ideas
from pydantic import BaseModel


router = APIRouter()

@router.post("/ideas")
async def ideas(request: IdeasRequest):
    if request.doi:
        cached = await get_cached_ideas(request.doi, request.language)
        if cached:
            return {"source": "cache", "ideas": cached}
    if not request.abstract:
        raise HTTPException(status_code=400, detail="Abstract is required for idea generation")
    generated = await generate_ideas(request.title, request.abstract, request.language)
    # Save to cache
    if request.doi and generated:
        await set_cached_ideas(request.doi, request.language, generated)
    return {"source": "claude", "ideas": generated}