import httpx
import os
from models.paper import Paper

PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")
ESEARCH_URL    = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL   = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# PubMed works in two steps:
# Step 1 — esearch: query → list of paper IDs
# Step 2 — esummary: paper IDs → paper details

async def search_pubmed(query: str, limit: int = 10) -> list[Paper]:
    papers = []

    try:
        async with httpx.AsyncClient() as client:

            # Step 1 — get paper IDs
            search_response = await client.get(ESEARCH_URL, params={
                "db":      "pubmed",
                "term":    query,
                "retmax":  limit,
                "retmode": "json",
                "api_key": PUBMED_API_KEY
            }, timeout=10)

            ids = search_response.json().get("esearchresult", {}).get("idlist", [])

            if not ids:
                return []

            # Step 2 — get paper details using those IDs
            summary_response = await client.get(ESUMMARY_URL, params={
                "db":      "pubmed",
                "id":      ",".join(ids),
                "retmode": "json",
                "api_key": PUBMED_API_KEY
            }, timeout=10)

            results = summary_response.json().get("result", {})

        for paper_id in ids:
            paper = results.get(paper_id, {})
            if not paper:
                continue

            # Authors
            authors = [a.get("name", "") for a in paper.get("authors", [])]

            # Year — first 4 chars of pubdate (e.g. "2023 Apr 12")
            year = paper.get("pubdate", "")[:4]

            # DOI — inside articleids list where idtype == "doi"
            doi = ""
            for article_id in paper.get("articleids", []):
                if article_id.get("idtype") == "doi":
                    doi = article_id.get("value", "")

            papers.append(Paper(
                title           = paper.get("title",  "") or "",
                authors         = authors,
                year            = year,
                abstract        = "",   # esummary doesn't return abstract
                doi             = doi,
                url             = f"https://pubmed.ncbi.nlm.nih.gov/{paper_id}/",
                source          = "PubMed",
                relevance_score = 0.0
            ))

    except Exception as e:
        print(f"PubMed error: {e}")

    return papers