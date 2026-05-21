import httpx
import os

PUBMED_API_KEY = os.getenv("NCBI_API_KEY")

# PubMed works in two steps:
# Step 1 — esearch: give it a query, get back a list of paper IDs
# Step 2 — efetch: give it those IDs, get back the actual paper details

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

async def search_pubmed(query: str, limit: int = 10) -> list:
    papers = []

    try:
        async with httpx.AsyncClient() as client:

            # ── Step 1: Search — get paper IDs ──────────────────────────────
            search_params = {
                "db":      "pubmed",
                "term":    query,
                "retmax":  limit,
                "retmode": "json",
                "api_key": PUBMED_API_KEY
            }
            search_response = await client.get(ESEARCH_URL, params=search_params, timeout=10)
            search_data = search_response.json()

            # Extract the list of IDs
            ids = search_data.get("esearchresult", {}).get("idlist", [])

            if not ids:
                return []

            # ── Step 2: Fetch summaries using those IDs ──────────────────────
            summary_params = {
                "db":      "pubmed",
                "id":      ",".join(ids),   # pass all IDs as comma-separated string
                "retmode": "json",
                "api_key": PUBMED_API_KEY
            }
            summary_response = await client.get(ESUMMARY_URL, params=summary_params, timeout=10)
            summary_data = summary_response.json()

        # Parse each paper from the summary result
        results = summary_data.get("result", {})

        for paper_id in ids:
            paper = results.get(paper_id, {})
            if not paper:
                continue

            # Authors — PubMed gives a list of author objects with "name" field
            authors = [a.get("name", "") for a in paper.get("authors", [])]

            # Year — PubMed gives pubdate like "2023 Apr 12" — take first 4 chars
            year = paper.get("pubdate", "")[:4]

            # DOI — inside articleids list, look for idtype == "doi"
            doi = ""
            for article_id in paper.get("articleids", []):
                if article_id.get("idtype") == "doi":
                    doi = article_id.get("value", "")

            # PubMed URL
            url = f"https://pubmed.ncbi.nlm.nih.gov/{paper_id}/"

            # Note: esummary does not return full abstract
            # Abstract requires efetch — added as empty for now, can enhance later
            papers.append({
                "title":           paper.get("title", ""),
                "authors":         authors,
                "year":            year,
                "abstract":        "",   # esummary doesn't return abstract
                "doi":             doi,
                "url":             url,
                "source":          "PubMed",
                "relevance_score": 0
            })

    except Exception as e:
        print(f"PubMed error: {e}")

    return papers
