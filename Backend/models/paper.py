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