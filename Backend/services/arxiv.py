import httpx
import xml.etree.ElementTree as ET
from models.paper import Paper

BASE_URL = "http://export.arxiv.org/api/query"

# arXiv returns XML — not JSON like the others
NS = {
    "atom":  "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom"
}

async def search_arxiv(query: str, limit: int = 10) -> list[Paper]:
    params = {
        "search_query": f"all:{query}",
        "start":        0,
        "max_results":  limit
    }

    papers = []

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params, timeout=10)
            root     = ET.fromstring(response.text)

        for entry in root.findall("atom:entry", NS):

            # Title
            title    = ""
            title_el = entry.find("atom:title", NS)
            if title_el is not None:
                title = title_el.text.strip().replace("\n", " ")

            # Abstract — in arXiv this is the <summary> tag
            abstract    = ""
            summary_el  = entry.find("atom:summary", NS)
            if summary_el is not None:
                abstract = summary_el.text.strip().replace("\n", " ")

            # Authors — multiple <author><name> tags
            authors = []
            for author in entry.findall("atom:author", NS):
                name_el = author.find("atom:name", NS)
                if name_el is not None:
                    authors.append(name_el.text)

            # Year — first 4 chars of published date (e.g. 2023-04-12T00:00:00Z)
            year         = ""
            published_el = entry.find("atom:published", NS)
            if published_el is not None:
                year = published_el.text[:4]

            # URL — the <id> tag
            url    = ""
            id_el  = entry.find("atom:id", NS)
            if id_el is not None:
                url = id_el.text.strip()

            # DOI — inside a <link> tag with title="doi" (not always present)
            doi = ""
            for link in entry.findall("atom:link", NS):
                if link.get("title") == "doi":
                    doi = link.get("href", "")

            papers.append(Paper(
                title           = title,
                authors         = authors,
                year            = year,
                abstract        = abstract,
                doi             = doi,
                url             = url,
                source          = "arXiv",
                relevance_score = 0.0
            ))

    except Exception as e:
        print(f"arXiv error: {e}")

    return papers