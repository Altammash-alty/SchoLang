from langchain.core.prompts import PromptTemplate , HumanMessage , AIMessage , SystemMessage
from langchainn.core import PydanticOutputParser , PromptOutputParser 
from model import sum_model
from summary_prompt import summary_prompt
from idea_prompt import idea_prompt



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
    prompt = summary_prompt.invoke({'lang_name':lang_name,'abstract':abstract})

try:
    response = sum_model.invoke([HumanMessage(content=prompt)])
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




