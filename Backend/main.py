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