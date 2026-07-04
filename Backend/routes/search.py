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


    from fastapi import APIRouter
    from typing import Annotated

    router=APIRouter()

    @router.post(/search)
    async def SearchRequest(request:Annotated[SearchRequest,
     Query(...,alias="request")]):
        """
        Search for papers using the SearchRequest model.

        Args:
            request: SearchRequest model containing the query, language, and limit.

        Returns:
            list[Paper]: List of papers matching the query.
        """
        print(request)

        