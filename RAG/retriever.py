from langchian_core import




retriever = vector_store.as_retriever(search_type="mmr", k=5)

retriever.get_