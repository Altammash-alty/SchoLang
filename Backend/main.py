import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import routes.health as health_router
import routes.search as search_router
import routes.ideas as ideas_router
import routes.rag as rag_router
import routes.retriever as retriever_router
import routes.summarize as summary_router


load_dotenv()

RAG_DIR = os.path.join(os.path.dirname(__file__), "..", "RAG")
sys.path.insert(0, os.path.abspath(RAG_DIR))
try:
    from chain import answer_query, index_and_answer
    from embeddings import index_papers
    RAG_AVAILABLE = True
except ImportError as e:
    print(f"[main] RAG not available (install RAG deps): {e}")
    RAG_AVAILABLE = False



app = FastAPI(title="SchoLang API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["http://localhost:3000"],
    allow_methods     = ["*"],
    allow_headers     = ["*"],
    allow_credentials = True,
)


app.include_router(health_router)
app.include_router(search_router)
app.include_router(ideas_router)
app.include_router(rag_router)
app.include_router(retriever_router)
app.include_router(summary_router)

