# RAG Architecture Skeleton — SchoLang
# Build this AFTER Phase 6 (Supabase is live)
# Every function has a clear step — fill in the implementation yourself

# ── Dependencies to add to requirements.txt ──────────────────────────────────
# pgvector          — vector extension for Supabase PostgreSQL
# openai            — for text-embedding-3-small embeddings
# supabase          — Python Supabase client

# ── Supabase SQL to run once ──────────────────────────────────────────────────
# Run this in your Supabase SQL editor to enable vector support:
#
# CREATE EXTENSION IF NOT EXISTS vector;
#
# CREATE TABLE paper_chunks (
#   id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
#   doi         TEXT NOT NULL,
#   title       TEXT,
#   chunk_text  TEXT NOT NULL,
#   embedding   vector(1536),        -- 1536 dims for text-embedding-3-small
#   source      TEXT,
#   created_at  TIMESTAMPTZ DEFAULT now()
# );
#
# CREATE INDEX ON paper_chunks
# USING ivfflat (embedding vector_cosine_ops)
# WITH (lists = 100);


# ── Step 1 — Chunking ─────────────────────────────────────────────────────────
def chunk_paper(abstract: str, title: str, doi: str) -> list[dict]:
    """
    Split a paper into smaller chunks for embedding.
    For now — abstract is short enough to be one chunk.
    When you add full text later, split into 200-word overlapping chunks.

    Returns list of dicts:
    [{ "doi": ..., "title": ..., "chunk_text": ... }]
    """
    # TODO: implement chunking logic
    # For abstract-only Phase 1 of RAG — return single chunk
    pass


# ── Step 2 — Embedding ────────────────────────────────────────────────────────
async def embed_text(text: str) -> list[float]:
    """
    Convert text into a vector embedding using OpenAI text-embedding-3-small.
    Returns a list of 1536 floats.

    Use: openai.embeddings.create(model="text-embedding-3-small", input=text)
    """
    # TODO: call OpenAI embeddings API
    pass


# ── Step 3 — Store in Supabase ────────────────────────────────────────────────
async def store_chunk(chunk: dict, embedding: list[float]) -> None:
    """
    Store a chunk and its embedding in the paper_chunks table in Supabase.
    Call this every time a new paper is fetched and summarised.

    INSERT INTO paper_chunks (doi, title, chunk_text, embedding, source)
    VALUES (...) ON CONFLICT DO NOTHING
    """
    # TODO: insert into Supabase paper_chunks table
    pass


# ── Step 4 — Semantic Search ──────────────────────────────────────────────────
async def semantic_search(query: str, limit: int = 10) -> list[dict]:
    """
    Main RAG search function.
    1. Embed the user's query
    2. Find most similar chunks in Supabase using cosine similarity
    3. Return top K results

    Supabase query:
    SELECT doi, title, chunk_text,
           1 - (embedding <=> query_vector) AS similarity
    FROM paper_chunks
    ORDER BY similarity DESC
    LIMIT {limit}
    """
    # Step 4a: embed the query
    query_embedding = await embed_text(query)

    # Step 4b: search Supabase
    # TODO: call Supabase RPC or raw SQL with pgvector cosine similarity
    pass


# ── Step 5 — RAG Route in main.py ────────────────────────────────────────────
# Add this route to main.py after this file is implemented:
#
# @app.post("/rag-search")
# async def rag_search(request: SearchRequest):
#     """
#     Semantic search over locally cached papers.
#     Falls back to live API search if no cached results found.
#     """
#     results = await semantic_search(request.query, request.limit)
#     if not results:
#         # fallback to live search
#         return await search(request)
#     return results


# ── Step 6 — Pipeline Integration ────────────────────────────────────────────
# After every /search call, in the background:
# 1. For each paper returned — chunk it
# 2. Embed each chunk
# 3. Store in Supabase
# This builds your local knowledge base automatically over time
# Use FastAPI BackgroundTasks for this — non-blocking

# from fastapi import BackgroundTasks
#
# @app.post("/search")
# async def search(request: SearchRequest, background: BackgroundTasks):
#     papers = ... (existing search logic)
#     for paper in papers:
#         background.add_task(index_paper, paper)  # runs after response is sent
#     return papers
#
# async def index_paper(paper):
#     chunks = chunk_paper(paper.abstract, paper.title, paper.doi)
#     for chunk in chunks:
#         embedding = await embed_text(chunk["chunk_text"])
#         await store_chunk(chunk, embedding)
