from langchain_core.prompts import PromptTemplate

query_expansion_prompt = PromptTemplate(
    template="""
You are an expert academic researcher.

Generate exactly three alternative search queries.

Original Query:
{query}

Return only the rewritten queries.
""",
    input_variables=["query"],
)

rag_prompt = PromptTemplate(
    template="""
You are SchoLang's academic assistant.

Answer ONLY using the retrieved papers.

Context:

{context}

Question:

{question}

Answer:
""",
    input_variables=["context", "question"],
)