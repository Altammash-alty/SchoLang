import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from services.semantic_scholar import search_semantic_scholar
from services.openalex import search_openalex
from services.arxiv import search_arxiv
from services.pubmed import search_pubmed

load_dotenv()  # loads your .env file so API keys are available

app = FastAPI(title="SchoLang API", version="1.0.0")

# ── CORS — allows your React frontend to talk to this backend ────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React runs on port 3000
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def health_check():
    return {"status": "running", "app": "SchoLang API"}


@app.post("/search")
async def search(request: SearchRequest):
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
            print(f"One API failed: {result}")
            continue
        all_papers.extend(result)


    seen_dois = set()
    unique_papers = []

    for paper in all_papers:
        doi = paper.get("doi", "")
        if doi and doi in seen_dois:
            continue  # skip duplicate
        if doi:
            seen_dois.add(doi)
        unique_papers.append(paper)

    unique_papers.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

    return unique_papers[:request.limit]


@app.get("/paper/{doi:path}")
async def get_paper(doi: str):
    # doi:path allows dots and slashes in the DOI string
    # This endpoint will be used later when fetching a single paper for idea generation
    # For now just return a placeholder — Phase 3 will build this out fully
    return {"doi": doi, "message": "Single paper endpoint — coming in Phase 3"}
