from fastapi import APIRouter
import asyncio

from models.model import SearchRequest
from RAG.embeddings import index_papers
from services.semantic import search_semantic_scholar
from services.openalex import search_openalex
from services.arxiv import search_arxiv
from services.pubmed import search_pubmed

router = APIRouter()

RAG_AVAILABLE = True


@router.post("/search")
async def search(request: SearchRequest):
    results = await asyncio.gather(
        search_semantic_scholar(request.query, request.limit),
        search_openalex(request.query, request.limit),
        search_arxiv(request.query, request.limit),
        search_pubmed(request.query, request.limit),
        return_exceptions=True,
    )

    all_papers = []

    for result in results:
        if isinstance(result, Exception):
            print(f"[search] API failure: {result}")
            continue
        all_papers.extend(result)

    seen_dois = set()
    unique_papers = []

    for paper in all_papers:
        doi = getattr(paper, "doi", None)

        if doi and doi in seen_dois:
            continue

        if doi:
            seen_dois.add(doi)

        unique_papers.append(paper)

    unique_papers.sort(
        key=lambda paper: getattr(paper, "relevance_score", 0),
        reverse=True,
    )

    top_papers = unique_papers[: request.limit]

    if RAG_AVAILABLE and top_papers:
        asyncio.create_task(
            _index_papers_background(
                [paper.model_dump() for paper in top_papers]
            )
        )

    return top_papers


async def _index_papers_background(papers: list[dict]):
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, index_papers, papers)
    except Exception as e:
        print(f"[search] Background RAG indexing failed: {e}")


@router.get("/paper/{doi:path}")
async def get_paper(doi: str):
    return {
        "doi": doi,
        "message": "Single paper endpoint — Phase 3",
    }