from langchain.huggingface import HuggingFacePipeline , HuggingFaceEndpoint 

repo_id=""


llm = HuggingFaceEndpoint(
    repo_id = repo_id , 
    task = "summ",
    temperature = 2.0
)