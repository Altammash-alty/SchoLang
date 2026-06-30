from langchain.huggingface import HuggingFacePipeline , HuggingFaceEndpoint 
from prompt import prompt

repo_id="unsloth/GLM-5.2-GGUF"


llm = HuggingFaceEndpoint(
    repo_id = repo_id , 
    task = "summarization",
    temperature = 2.0,



)


result = llm.invoke(prompt)