from langgraph import SequenceGraph
from langchain_huggingface import HuggingFaceEndpoint





sum_repo_id='Qwen/Qwen3-VL-8B-Instruct'

sum_model=HuggingFaceEndpoint(
    repo_id = sum_repo_id ,
    task = "summarization",
    temperature = 0.16062005,
    max_new_tokens=1024,
    trust_remote_code=True
)




idea_repo_id='unsloth/GLM-5.2-GGUF'
idea_model=HuggingFaceEndpoint(
    repo_id = idea_repo_id ,
    task = "text-generation",
    temperature = 2.0,
    max_new_tokens=1024,
    trust_remote_code=True
)

workflow=SequenceGraph()