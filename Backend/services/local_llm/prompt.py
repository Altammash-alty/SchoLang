from langchain.core.prompts import PromptTemplate , HumanMessage , AIMessage , SystemMessage
from langchainn.core import PydanticOutputParser , PromptOutputParser 

template  = """
You are an expert reseracher in the world with knowledge for almost everything . You are a Polymatch and and excelle

"""

final_prompt = PromptTemplate(
    template = template ,
    input_variables = ["query"]
)
