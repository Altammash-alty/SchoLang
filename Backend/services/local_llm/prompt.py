from langchain.core.prompts import PromptTemplate , HumanMessage , AIMessage , SystemMessage
from langchainn.core import PydanticOutputParser , PromptOutputParser 

LANGUAGE_NAMES = {
    "en": "English",
    "zh": "Chinese",
    "hi": "Hindi",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
    "nl": "Dutch",
    "fr": "French",
}

async def summarise_paper(abstract: str, language: str = "en") -> dict:
    lang_name = LANGUAGE_NAMES.get(language, "English")
    prompt = f"""
You are a research assistant. Read this academic paper abstract and extract key information.

 Respond entirely in {lang_name}. Do not use any other language in your response.


Abstract:
{abstract}

Return your response in exactly this format — no extra text before or after:





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


