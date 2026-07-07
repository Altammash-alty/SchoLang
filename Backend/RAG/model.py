from langchain_huggingface import HuggingFaceEndpoint

from .config import (
    HF_TOKEN,
    GENERATION_MODEL,
)

rag_model = HuggingFaceEndpoint(
    repo_id=GENERATION_MODEL,
    huggingfacehub_api_token=HF_TOKEN,
    task="text-generation",
    temperature=0.2,
    max_new_tokens=512,
)

query_expansion_model = HuggingFaceEndpoint(
    repo_id=GENERATION_MODEL,
    huggingfacehub_api_token=HF_TOKEN,
    task="text-generation",
    temperature=0.1,
    max_new_tokens=128,
)