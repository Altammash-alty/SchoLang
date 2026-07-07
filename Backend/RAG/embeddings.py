from pathlib import Path

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from .config import (
    EMBEDDING_MODEL,
    VECTOR_DB,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    encode_kwargs={"normalize_embeddings": True},
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

vector_store = Chroma(
    persist_directory=VECTOR_DB,
    embedding_function=embeddings,
)


def index_papers(papers: list[dict]) -> None:
    """
    Index papers into the vector database.

    Expected paper format:

    {
        "title": "...",
        "abstract": "...",
        "authors": "...",
        "year": "...",
        "doi": "..."
    }
    """

    docs = []

    for paper in papers:

        text = paper.get("abstract", "")

        if not text:
            continue

        chunks = splitter.create_documents(
            [text],
            metadatas=[
                {
                    "title": paper.get("title", ""),
                    "authors": paper.get("authors", ""),
                    "year": paper.get("year", ""),
                    "doi": paper.get("doi", ""),
                }
            ],
        )

        docs.extend(chunks)

    if docs:
        vector_store.add_documents(docs)