import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from models.paper import SearchRequest, Paper
from services.semantic import search_semantic_scholar
from services.openalex         import search_openalex
from services.arxiv            import search_arxiv
from services.pubmed           import search_pubmed
from services.claude_services   import summarise_paper, generate_ideas
from cache.redis_client        import (
    get_cached_summary, set_cached_summary,
    get_cached_ideas,   set_cached_ideas
)

load_dotenv()

app = FastAPI(title="SchoLang API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["http://localhost:3000"],
    allow_methods     = ["*"],
    allow_headers     = ["*"],
    allow_credentials = True,
)


class SummariseRequest(BaseModel):
    doi:      str
    abstract: str
    language: str = "en"

class IdeasRequest(BaseModel):
    doi:      str
    title:    str
    abstract: str
    language: str = "en"

@app.get("/")
def health_check():
    return {"status": "running", "app": "SchoLang API", "version": "1.0.0"}



@app.post("/search")
async def search(request: SearchRequest):
    """
    Main search route.
    Calls all 4 APIs simultaneously, merges results,
    deduplicates by DOI, sorts by relevance, returns top N.
    """

    
    results = await asyncio.gather(
        search_semantic_scholar(request.query, request.limit),
        search_openalex(request.query, request.limit),
        search_arxiv(request.query, request.limit),
        search_pubmed(request.query, request.limit),
        return_exceptions=True  
    )

    all_papers = []
    for result in results:
        if isinstance(result, Exception):
            print(f"API failure: {result}")
            continue
        all_papers.extend(result)

    seen_dois    = set()
    unique_papers = []
    for paper in all_papers:
        doi = paper.doi
        if doi and doi in seen_dois:
            continue
        if doi:
            seen_dois.add(doi)
        unique_papers.append(paper)

    
    unique_papers.sort(key=lambda x: x.relevance_score, reverse=True)

    return unique_papers[:request.limit]



@app.post("/summarise")
async def summarise(request: SummariseRequest):
    """
    Takes a paper's DOI, abstract, and language.
    Returns AI-generated plain-language summary.
    Checks Redis cache first — only calls Claude if not cached.
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


# ── Generate project ideas from a paper ──────────────────────────────────────
@app.post("/ideas")
async def ideas(request: IdeasRequest):
    """
    Takes a paper's DOI, title, abstract, and language.
    Returns 3 AI-generated buildable project ideas.
    Checks Redis cache first — only calls Claude if not cached.
    """

    # Check cache first
    if request.doi:
        cached = await get_cached_ideas(request.doi, request.language)
        if cached:
            return {"source": "cache", "ideas": cached}

    # Not in cache — call Claude
    if not request.abstract:
        raise HTTPException(status_code=400, detail="Abstract is required for idea generation")

    generated = await generate_ideas(request.title, request.abstract, request.language)

    # Save to cache
    if request.doi and generated:
        await set_cached_ideas(request.doi, request.language, generated)

    return {"source": "claude", "ideas": generated}


@app.get("/paper/{doi:path}")
async def get_paper(doi: str):
    """
    Placeholder for single paper fetch.
    doi:path allows dots and slashes in DOI string.
    Will be expanded in later phases.
    """
    return {"doi": doi, "message": "Single paper endpoint — Phase 3"}