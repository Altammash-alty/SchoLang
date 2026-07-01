from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter



splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

text_splitted=splitter.create_documents([])

embeddings=HuggingFaceEmbeddings(model="BAAI/bge-m3", encode_kwargs={"normalize_embeddings": True})
vector_store=ChromaDB.from_documents(documents=text_splitted, embedding=embeddings, persist_directory="./vector_store")