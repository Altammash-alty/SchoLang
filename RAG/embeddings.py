from langchain_huggingface import HuggingFaceEmbeddings

embeddings=HuggingFaceEmbeddings(model="intfloat/multilingual-e5-small", encode_kwargs={"normalize_embeddings": True})
vector_store=ChromaDB.from_documents(documents=text_splitted, embedding=embeddings, persist_directory="./vector_store")