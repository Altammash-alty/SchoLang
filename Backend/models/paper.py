# ── Request model ─────────────────────────────────────────────────────────────
class SearchRequest(BaseModel):
    query:    str
    language: str = "en"
    limit:    int = 10

# ----Paper Cache --- 
class PaperCache(BaseModel):
    dois:     str
    title:    str
    abstract: str
    authors:  List[str]
    venue:    str
    year:     int
    url:      str
    sources:  List[str] 
