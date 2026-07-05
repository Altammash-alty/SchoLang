from fastapi import APIRouter, HTTPException


router=APIRouter()

@router.post("/summarise")
async def summarise(request: SummariseRequest):
    """
    Takes a paper's DOI, abstract, and language.
    Returns AI-generated plain-language summary.
    Checks Redis cache first — only calls Claude if not cached.
    AI plain-language summary of a paper abstract.
    Uses Redis cache — only calls Claude if result not already cached.
    """ 
    # Check cache first
    if request.doi:
        cached = await get_cached_summary(request.doi, request.language)
        if cached:
            return {"source": "cache", "summary": cached}
    # Not in cache — call Claude
    if not request.abstract:
        raise HTTPException(status_code=400, detail="Abstract is required for summarisation")
    summary = await summarise_paper(request.abstract, request.language)
    # Save to cache for next time
    if request.doi and summary["summary"]:
        await set_cached_summary(request.doi, request.language, summary)
    return {"source": "claude", "summary": summary}
