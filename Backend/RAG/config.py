from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

EMBEDDING_MODEL = "BAAI/bge-m3"

GENERATION_MODEL = "Qwen/Qwen2.5-7B-Instruct"

VECTOR_DB = "./RAG/vector_store"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K = 10

RERANK_K = 5