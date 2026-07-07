from langchain_core.prompts import PromptTemplate

from .embeddings import vector_store

query_expansion_prompt = PromptTemplate(
    template="""
You are an expert academic researcher.

Rewrite the user's query into three alternative search queries.

Keep the meaning identical.

Query:

{query}

Return only three rewritten queries.
""",
    input_variables=["query"],
)

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 10,
        "fetch_k": 30,
        "lambda_mult": 0.5,
    },
)