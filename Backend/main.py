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
   


import routes.health as health_router
import routes.search as search_router
import routes.ideas as ideas_router
import routes.rag as rag_router
import routes.retriever as retriever_router
import routes.summarize as summary_router



