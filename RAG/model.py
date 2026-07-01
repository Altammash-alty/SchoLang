from langgraph import StateGraph
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()


repo_id=''


retriever_model=HuggingFaceEndpoint