from langchain.core.prompts import PromptTemplate , HumanMessage , AIMessage , SystemMessage
from langchainn.core import PydanticOutputParser , PromptOutputParser 



async def summarise_paper(abstract: str, language: str = "en") -> dict:


    
template  = """
You are an excellent 

"""
input_variables = ["query"]
partial_variables = ["context"]

final_prompt = PromptTemplate(
    template = template ,
    input_variables = input_variables,
    partial_variables = partial_variables
)


