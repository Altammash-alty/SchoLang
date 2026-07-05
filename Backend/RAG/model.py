from langgraph import StateGraph
from langchain_huggingface import HuggingFaceEndpoint
from retriever import final_prompt 
from dotenv import load_dotenv

load_dotenv()


repo_id='BAAI/bge-m3'


retriever_model=HuggingFaceEndpoint(
    repo_id=repo_id,
    task='text',
    temperature=0.16062005
)


result = retriever_model.invoke(final_prompt)
papers=result['papers']
score=result['scores']
