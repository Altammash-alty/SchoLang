import httpx
from models.paper import Paper

BASE_URL = "https://api.openalex.org/works"

async def search_openalex(query: str, limit: int = 10) -> list[Paper]:
    params = {
        "search":   query,
        "per-page": limit,
    }

    papers = []

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params, timeout=10)
            data     = response.json()

        for result in data.get("results", []):

            # Extract authors from nested authorships list
            authors = []
            for authorship in result.get("authorships", []):
                name = authorship.get("author", {}).get("display_name", "")
                if name:
                    authors.append(name)

            # Reconstruct abstract from inverted index
            abstract = ""
            inverted = result.get("abstract_inverted_index", {})
            if inverted:
                max_pos = max(pos for positions in inverted.values() for pos in positions)
                words   = [""] * (max_pos + 1)
                for word, positions in inverted.items():
                    for pos in positions:
                        words[pos] = word
                abstract = " ".join(words)

            papers.append(Paper(
                title           = result.get("title", "") or "",
                authors         = authors,
                year            = str(result.get("publication_year", "")),
                abstract        = abstract,
                doi             = result.get("doi", "") or "",
                url             = result.get("id",  "") or "",
                source          = "OpenAlex",
                relevance_score = float(result.get("relevance_score", 0) or 0)
            ))

    except Exception as e:
        print(f"OpenAlex error: {e}")

    return papers