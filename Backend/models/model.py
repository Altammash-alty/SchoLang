from pydantic import BaseModel

class SearchRequest(BaseModel):
    query:    str
    language: str = "en"
    limit:    int = 10

class Paper(BaseModel):
    title:           str
    authors:         list
    year:            str
    abstract:        str
    doi:             str
    url:             str
    source:          str
    relevance_score: float = 0.0

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
   
