from langchain.core.prompts import PromptTemplate , HumanMessage , AIMessage , SystemMessage
from langchainn.core import PydanticOutputParser , PromptOutputParser 

template  = """
You are an expert reseracher in the world with knowledge for almost everything . You are a Polymatch and and excelle

"""
input_variables = ["query"]
partial_variables = ["context"]

final_prompt = PromptTemplate(
    template = template ,
    input_variables = input_variables,
    partial_variables = partial_variables
)


