import httpx
import os

SEMANTIC_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

async def search_semantic_scholar(query: str, limit: int = 10) -> list:
    headers = {"x-api-key": SEMANTIC_API_KEY}
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,externalIds,url"
    }

    papers = []

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, headers=headers, params=params, timeout=10)
            data = response.json()

        for result in data.get("data", []):
            authors = [a.get("name", "") for a in result.get("authors", [])]
            doi = result.get("externalIds", {}).get("DOI", "")

            papers.append({
                "title":           result.get("title", ""),
                "authors":         authors,
                "year":            str(result.get("year", "")),
                "abstract":        result.get("abstract", ""),
                "doi":             doi,
                "url":             result.get("url", ""),
                "source":          "Semantic Scholar",
                "relevance_score": 0
            })

    except Exception as e:
        print(f"Semantic Scholar error: {e}")

    return papers
