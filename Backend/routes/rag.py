from fastapi import APIRouter, HTTPException
from ..models.model import RAGRequest
from ..services.rag_services import answer_query, index_and_answer


router=APIRouter()

@router.post("/rag")
async def rag_query(request: RAGRequest):
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