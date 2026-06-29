from langchain.huggingface import HuggingFacePipeline , HuggingFaceEndpoint 

repo_id=""


llm = HuggingFaceEndpoint(
    repo_id = repo_id , 
    task = "summarization",
    temperature = 2.0,
    
)