from fastapi import APIRouter

router = APIRouter()



@router.get("/")
async def health_check():
    return {
        "status":        "running",
        "app":           "SchoLang API",
        "version":       "1.0.0",
        "rag_available": RAG_AVAILABLE,
    }

