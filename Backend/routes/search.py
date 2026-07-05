from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    language: str = "en"
    limit: int = 10

class UserSignUp(BaseModel):
    username:str
    email:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

import httpx
import asyncio
from fastapi import APIRouter , Query
from typing import Annotated
from ..RAG.chain import answer_query, index_papers
from ..RAG.embeddings import index_papers


router=APIRouter()

@router.post("/search")
async def search(request: SearchRequest):
    """
    Main search route.
    Calls all 4 APIs simultaneously, merges results,
    deduplicates by DOI, sorts by relevance, returns top N.
    
    Multi-source paper search.
    Calls all 4 APIs simultaneously, merges, deduplicates by DOI,
    sorts by relevance, and returns top N results.
    
    Also triggers background RAG indexing of the results so follow-up
    /rag queries have immediate context available.
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
        
@router.get("/paper/{doi:path}")
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