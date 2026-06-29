from langchain.huggingface import HuggingFacePipeline , HuggingFaceEndpoint 
from prompt import prompt

repo_id=""


llm = HuggingFaceEndpoint(
    repo_id = repo_id , 
    task = "summarization",
    temperature = 2.0,



)


result = ll.invoke(prompt)