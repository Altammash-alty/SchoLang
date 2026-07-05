from fastapi import APIRouter, HTTPException
from ..models.paper import RAGRequest
from ..services.rag_services import answer_query, index_and_answer


router=APIRouter()

@router.post("/rag")
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