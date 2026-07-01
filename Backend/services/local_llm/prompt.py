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

    result = {
        "summary":     "",
        "findings":    [],
        "methodology": "",
        "limitations": ""
    }

    current_section = None

    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("SUMMARY:"):
            current_section = "summary"
        elif line.startswith("KEY FINDINGS:"):
            current_section = "findings"
        elif line.startswith("METHODOLOGY:"):
            current_section = "methodology"
        elif line.startswith("LIMITATIONS:"):
            current_section = "limitations"
        else:
            if current_section == "summary":
                result["summary"] += line + " "
            elif current_section == "findings" and line.startswith("-"):
                result["findings"].append(line[1:].strip())
            elif current_section == "methodology":
                result["methodology"] += line + " "
            elif current_section == "limitations":
                result["limitations"] += line + " "

    result["summary"]     = result["summary"].strip()
    result["methodology"] = result["methodology"].strip()
    result["limitations"] = result["limitations"].strip()

    return result

except Exception as e:
    print(f"Local LLM summarise error: {e}")
    return {"summary": "", "findings": [], "methodology": "", "limitations": ""}


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


async def generate_ideas(title: str, abstract: str, language: str = "en") -> list:

    lang_name = LANGUAGE_NAMES.get(language, "English")
    
    prompt = f"""

You are a creative engineering mentor. Read this research paper and generate exactly 3
project ideas that a student team could realistically build in 4-8 weeks for a hackathon
or tech fest competition.

Respond entirely in {lang_name}. Do not use any other language in your response.

Paper title: {title}
Paper abstract: {abstract}

Return in exactly this format — nothing else:

PROJECT 1:
TITLE: project name here
DESCRIPTION: 2 sentences explaining what it does and who it helps
TECH STACK: tool1, tool2, tool3, tool4
DIFFICULTY: Beginner or Intermediate or Advanced
BUILD TIME: X weeks
COMPETITION ANGLE: one sentence on what makes it stand out in a competition


PROJECT 2:
TITLE:
DESCRIPTION:
TECH STACK:
DIFFICULTY:
BUILD TIME:
COMPETITION ANGLE:

PROJECT 3:
TITLE:
DESCRIPTION:
TECH STACK:
DIFFICULTY:
BUILD TIME:
COMPETITION ANGLE:
"""

    try:
        message = client.messages.create(
            model      = "claude-sonnet-4-6",
            max_tokens = 1500,
            messages   = [{"role": "user", "content": prompt}]
        )
