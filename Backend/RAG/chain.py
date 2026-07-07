from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage

from .retriever import (
    retriever,
    query_expansion_prompt,
)

from .model import (
    rag_model,
    query_expansion_model,
)

from .prompts import rag_prompt

from .embeddings import index_papers

from .Eval.reranker import rerank


def format_docs(docs: List[Document]) -> str:

    if not docs:
        return "No relevant papers found."

    sections = []

    for idx, doc in enumerate(docs, start=1):

        meta = doc.metadata

        title = meta.get("title", "Unknown")

        authors = meta.get("authors", "")

        year = meta.get("year", "")

        doi = meta.get("doi", "")

        block = f"[{idx}] {title}"

        if authors:
            block += f" | {authors}"

        if year:
            block += f" ({year})"

        block += "\n"

        block += doc.page_content

        if doi:
            block += f"\nDOI : {doi}"

        sections.append(block)

    return "\n\n-------------------------\n\n".join(sections)


async def expand_query(query: str) -> List[str]:

    prompt = query_expansion_prompt.invoke(
        {
            "query": query
        }
    )

    response = await query_expansion_model.ainvoke(
        [
            HumanMessage(content=prompt.text)
        ]
    )

    queries = []

    for line in response.content.split("\n"):

        line = line.strip()

        if line:

            queries.append(line)

    queries = queries[:3]

    return [query] + queries


async def retrieve_documents(query: str):

    expanded_queries = await expand_query(query)

    seen = set()

    documents = []

    for q in expanded_queries:

        docs = retriever.invoke(q)

        for doc in docs:

            key = hash(doc.page_content)

            if key in seen:
                continue

            seen.add(key)

            documents.append(doc)

    return documents


async def answer_query(
    query: str,
    use_reranker: bool = True,
):

    docs = await retrieve_documents(query)

    if use_reranker and docs:

        docs = rerank(
            query=query,
            docs=docs,
            top_k=5,
        )

    context = format_docs(docs)

    prompt = rag_prompt.invoke(
        {
            "context": context,
            "question": query,
        }
    )

    response = await rag_model.ainvoke(
        [
            HumanMessage(content=prompt.text)
        ]
    )

    return {

        "query": query,

        "answer": response.content,

        "sources": [

            {
                "title": doc.metadata.get("title"),

                "authors": doc.metadata.get("authors"),

                "year": doc.metadata.get("year"),

                "doi": doc.metadata.get("doi"),
            }

            for doc in docs

        ],

        "documents_retrieved": len(docs)

    }


async def index_and_answer(
    query: str,
    papers: list[dict],
):

    index_papers(papers)

    return await answer_query(query)