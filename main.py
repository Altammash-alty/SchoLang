from fastapi import FastAPI
from routes.search import SearchRequest
import asyncio
from services.semantic import search_semantic_scholar
from services.openalex import search_openalex
from services.arxiv import search_arxiv
from services.pubmed import search_pubmed

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/search")
async def search(request: SearchRequest):
    
    results = await asyncio.gather(
        search_semantic_scholar(request.query),
        search_openalex(request.query),
        search_arxiv(request.query),
        search_pubmed(request.query)
    )
    

    all_papers = []
    for result in results:
        all_papers.extend(result)
    
    
    seen = set()
    unique_papers = []
    for paper in all_papers:
        if paper["doi"] not in seen:
            seen.add(paper["doi"])
            unique_papers.append(paper)
    
    
    return unique_papers[:10]
