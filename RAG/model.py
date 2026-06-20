from langchain_huggingface import HuggingFaceEmbeddings , HuggingFaceEndpoint , HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.document_loaders import 
from langchain_core.embeddings import Embeddings
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2 " , 
    task = "text-generation",
     temperature=1.2,
     max_new_tokens=500,
     huggingface_api_key=os.getenv("HUGGINGFACEHUB_API_KEY"))


prompt = PromptTemplate(
    template="""{
        "instruction": "",
        "input":""
    }""",
    input_variables=[],
    partial_var={}
)

final_prompt=prompt.invoke({})

answer=llm.invoke(final_prompt)