import asyncio
import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from models.paper import SearchRequest, Paper
from services.semantic import search_semantic_scholar
from services.semantic         import search_semantic_scholar
from services.openalex         import search_openalex
from services.arxiv            import search_arxiv
from services.pubmed           import search_pubmed
from services.claude_services   import summarise_paper, generate_ideas
from services.claude_services  import summarise_paper, generate_ideas
from cache.redis_client        import (
    get_cached_summary, set_cached_summary,
    get_cached_ideas,   set_cached_ideas
    get_cached_ideas,   set_cached_ideas,
)
RAG_DIR = os.path.join(os.path.dirname(__file__), "..", "RAG")
sys.path.insert(0, os.path.abspath(RAG_DIR))
try:
    from chain import answer_query, index_and_answer
    from embeddings import index_papers
    RAG_AVAILABLE = True
except ImportError as e:
    print(f"[main] RAG not available (install RAG deps): {e}")
    RAG_AVAILABLE = False
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
class RAGRequest(BaseModel):
    query:         str
    papers:        list[dict] | None = None   # optional: index these papers first
    use_reranker:  bool              = True   # cross-encoder reranking (slower, more precise)

@app.get("/")
def health_check():
    return {"status": "running", "app": "SchoLang API", "version": "1.0.0"}
    return {
        "status":        "running",
        "app":           "SchoLang API",
        "version":       "1.0.0",
        "rag_available": RAG_AVAILABLE,
    }
@app.post("/search")
async def search(request: SearchRequest):
    "
    Main search route.
    Calls all 4 APIs simultaneously, merges results,
    deduplicates by DOI, sorts by relevance, returns top N.
    
    Multi-source paper search.
    Calls all 4 APIs simultaneously, merges, deduplicates by DOI,
    sorts by relevance, and returns top N results.
    
    Also triggers background RAG indexing of the results so follow-up
    /rag queries have immediate context available.
    "
    results = await asyncio.gather(
        search_semantic_scholar(request.query, request.limit),
        search_openalex(request.query, request.limit),
        search_arxiv(request.query, request.limit),
        search_pubmed(request.query, request.limit),
        return_exceptions=True  
        return_exceptions=True,
    )
    all_papers = []
    for result in results:
        if isinstance(result, Exception):
            print(f"API failure: {result}")
            print(f"[search] API failure: {result}")
            continue
        all_papers.extend(result)
    seen_dois    = set()
    # Deduplicate by DOI
    seen_dois     = set()
    unique_papers = []
    for paper in all_papers:
        doi = paper.doi
        if doi and doi in seen_dois:
            continue
        if doi:
            seen_dois.add(doi)
        unique_papers.append(paper)
    
    # Sort by relevance score descending
    unique_papers.sort(key=lambda x: x.relevance_score, reverse=True)
    top_papers = unique_papers[: request.limit]
    return unique_papers[:request.limit]
    # Background: index papers into RAG vector store
    if RAG_AVAILABLE and top_papers:
        paper_dicts = [p.model_dump() for p in top_papers]
        asyncio.create_task(_index_papers_background(paper_dicts))
    return top_papers
async def _index_papers_background(papers: list[dict]) -> None:
    """Fire-and-forget task to index search results into the RAG vector store."""
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, index_papers, papers)
    except Exception as e:
        print(f"[search] Background RAG indexing failed: {e}")
@app.post("/summarise")
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
# ── Generate project ideas from a paper ──────────────────────────────────────
@app.post("/ideas")
async def ideas(request: IdeasRequest):
    """
    Takes a paper's DOI, title, abstract, and language.
    Returns 3 AI-generated buildable project ideas.
    Checks Redis cache first — only calls Claude if not cached.
    Generate 3 buildable project ideas from a paper.
    Uses Redis cache — only calls Claude if result not already cached.
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
@app.post("/rag")
async def rag_query(request: RAGRequest):
    """
    RAG-based Q&A grounded in retrieved academic paper context.
    If 'papers' are provided in the request body, they are indexed first
    (useful for first-time queries on a fresh topic).
    Returns a cited answer generated from retrieved paper chunks.
    """
    if not RAG_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="RAG pipeline is not available. Install RAG dependencies.",
        )
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    if request.papers:
        result = await index_and_answer(request.query, request.papers)
    else:
        result = await answer_query(request.query, use_reranker=request.use_reranker)
    return result
@app.get("/paper/{doi:path}")
async def get_paper(doi: str):
    """
    Placeholder for single paper fetch.
    doi:path allows dots and slashes in DOI string.
    Will be expanded in later phases.
    Single paper detail endpoint.
    doi:path allows dots and slashes in DOI strings.
    Expanded in Phase 3.
    """
    return {"doi": doi, "message": "Single paper endpoint — Phase 3"}
    return {"doi": doi, "message": "Single paper endpoint — Phase 3"} 