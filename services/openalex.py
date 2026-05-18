import httpx

async def search_openalex(query: str):
    
    url = f"https://api.openalex.org/works?search={query}&per-page=10"
    
    papers = []
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    
    for result in data["results"]:
        
        # get authors
        authors = []
        for authorship in result.get("authorships", []):
            name = authorship.get("author", {}).get("display_name", "")
            if name:
                authors.append(name)
        
        # reconstruct abstract
        abstract = ""
        inverted = result.get("abstract_inverted_index", {})
        if inverted:
            words = [""] * (max(max(v) for v in inverted.values()) + 1)
            for word, positions in inverted.items():
                for pos in positions:
                    words[pos] = word
            abstract = " ".join(words)
        
        papers.append({
            "title": result.get("title", ""),
            "authors": authors,
            "year": result.get("publication_year", ""),
            "abstract": abstract,
            "doi": result.get("doi", ""),
            "url": result.get("id", ""),
            "source": "openalex",
            "relevance_score": result.get("relevance_score", 0)
        })
    
    return papers