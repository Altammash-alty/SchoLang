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


SUMMARY:
Write a plain-language summary in 3-4 sentences. No jargon. Anyone should understand this.

KEY FINDINGS:
- Finding 1
- Finding 2
- Finding 3

METHODOLOGY:
One sentence describing how the study was conducted.

LIMITATIONS:
One sentence describing the main limitation of this research.
"""

try:
    response = llm.invoke([HumanMessage(content=prompt)])
    raw = response.content

    