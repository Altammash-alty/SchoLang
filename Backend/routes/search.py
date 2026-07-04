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
    

router=APIRouter()

@router.post("/search")
async def SearchRequest(request:Annotated[SearchRequest,
    Query(...,alias="request")]):
     
    results = await asyncio.gather(
        search_semantic_scholar(request.query, request.limit),
        search_openalex(request.query, request.limit),
        search_arxiv(request.query, request.limit),
        search_pubmed(request.query, request.limit),
        return_exceptions=True,
    )
    
all_papers=[]

for result in results:
    if isinstance(result, Exception):
        print(f"API failure: {result}")
        continue
    all_papers.extend(result)
    

        