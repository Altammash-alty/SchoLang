"""
RAG/chain.py
────────────
Wires the full RAG pipeline using LangChain LCEL (| pipe syntax).

Pipeline flow:
  User query
    │
    ├─[Pre-Retrieval]─ query_expansion_model rewrites query into 3 variants
    │                   → multi-query retrieval for higher recall
    │
    ├─[Retrieval]─────  MMR retriever pulls top-10 diverse paper chunks
    │
    ├─[Post-Retrieval]─ Reranker (cross-encoder) re-scores and selects top-5
    │
    ├─[Augmentation]──  RAG prompt templates context + question
    │
    └─[Generation]────  rag_model produces cited, grounded answer

Public API:
  answer_query(query: str) -> dict
  index_and_answer(query: str, papers: list[dict]) -> dict  (index first then answer)
"""

from __future__ import annotations

from typing import List

from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document

from retriever import retriever, query_expansion_prompt
from model import rag_model, query_expansion_model
from Eval.reranker import rerank
from embeddings import index_papers


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _format_docs(docs: List[Document]) -> str:
    """
    Format retrieved documents into a numbered context block.
    Includes title, authors, year, and DOI for citation support.
    """
    if not docs:
        return "No relevant papers found in the knowledge base."

    formatted = []
    for i, doc in enumerate(docs, 1):
        meta    = doc.metadata
        title   = meta.get("title", "Unknown Paper")
        authors = meta.get("authors", "")
        year    = meta.get("year", "")
        doi     = meta.get("doi", "")

        header = f"[{i}] {title}"
        if authors:
            header += f" | {authors}"
        if year:
            header += f" ({year})"

        block = f"{header}\n{doc.page_content}"
        if doi:
            block += f"\n→ DOI: {doi}"

        formatted.append(block)

    return "\n\n---\n\n".join(formatted)


def _expand_query(query: str) -> List[str]:
    """
    Use the query expansion model to generate 3 alternative phrasings.
    Falls back to just the original query on any error.
    """
    try:
        prompt_value = query_expansion_prompt.invoke({"query": query})
        response     = query_expansion_model.invoke(
            [HumanMessage(content=prompt_value.text)]
        )
        alternatives = [
            line.strip()
            for line in response.content.strip().split("\n")
            if line.strip()
        ]
        # Always include the original query too
        all_queries = [query] + alternatives[:3]
        return all_queries
    except Exception as e:
        print(f"[chain] Query expansion failed, using original: {e}")
        return [query]


def _multi_query_retrieve(query: str) -> List[Document]:
    """
    Retrieve docs for all query variants, deduplicate by content hash.
    This significantly boosts recall compared to single-query retrieval.
    """
    all_queries = _expand_query(query)
    seen        = set()
    docs        = []

    for q in all_queries:
        try:
            results = retriever.invoke(q)
            for doc in results:
                key = hash(doc.page_content)
                if key not in seen:
                    seen.add(key)
                    docs.append(doc)
        except Exception as e:
            print(f"[chain] Retrieval failed for query '{q}': {e}")

    return docs


# ─────────────────────────────────────────────────────────────────────────────
# RAG ANSWER PROMPT
# ─────────────────────────────────────────────────────────────────────────────

rag_template = """You are an expert academic research assistant for SchoLang, \
a multilingual research intelligence platform.

Using ONLY the retrieved paper excerpts below, answer the user's research question.

Rules:
- Cite specific papers using their bracket numbers, e.g. [1], [2], [3]
- Be specific, factual, and grounded in the evidence
- If the context doesn't contain enough information to answer, say so clearly
- Do not fabricate results, statistics, or citations

Retrieved Papers:
{context}

Research Question: {question}

Answer:"""

rag_prompt = PromptTemplate(
    template=rag_template,
    input_variables=["context", "question"],
)


# ─────────────────────────────────────────────────────────────────────────────
# LCEL CHAIN  (simple path — no reranker, fast)
# ─────────────────────────────────────────────────────────────────────────────
# Use this when speed matters more than maximum precision.

simple_rag_chain = (
    RunnableParallel(
        context=retriever | RunnableLambda(_format_docs),
        question=RunnablePassthrough(),
    )
    | rag_prompt
    | rag_model
    | StrOutputParser()
)


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

async def answer_query(query: str, use_reranker: bool = True) -> dict:
    """
    Run the full RAG pipeline for a research question.

    Args:
        query:        The user's research question
        use_reranker: If True, applies cross-encoder reranking after retrieval
                      for higher precision (slightly slower). Default: True.

    Returns:
        {
          "answer": str,
          "query":  str,
          "num_docs_retrieved": int,
        }
    """
    try:
        # Step 1: Multi-query retrieval (pre-retrieval query expansion)
        docs = _multi_query_retrieve(query)

        # Step 2: Cross-encoder reranking (post-retrieval)
        if use_reranker and docs:
            docs = rerank(query=query, docs=docs, top_k=5)

        # Step 3: Format context
        context = _format_docs(docs)

        # Step 4: Build prompt + generate answer
        prompt_value = rag_prompt.invoke({"context": context, "question": query})
        response     = await rag_model.ainvoke(
            [HumanMessage(content=prompt_value.text)]
        )
        answer = response.content.strip()

        return {
            "answer":            answer,
            "query":             query,
            "num_docs_retrieved": len(docs),
        }

    except Exception as e:
        print(f"[chain] RAG pipeline error: {e}")
        return {"answer": "", "query": query, "error": str(e), "num_docs_retrieved": 0}


async def index_and_answer(query: str, papers: List[dict]) -> dict:
    """
    Index a fresh batch of papers then immediately answer the query.
    Useful when the frontend fetches new papers and wants RAG answers on them.

    Args:
        query:  The user's research question
        papers: List of paper dicts from the Backend search APIs

    Returns:
        Same shape as answer_query()
    """
    index_papers(papers)
    return await answer_query(query)