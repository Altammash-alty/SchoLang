from idea_prompt import idea_prompt
from model import idea_model


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

async def generate_ideas(title: str, abstract: str, language: str = "en") -> list:

    lang_name = LANGUAGE_NAMES.get(language, "English")
    
    prompt=idea_prompt.invoke({'lang_name':lang_name,'title':title,'abstract':abstract})
    try:
        response = idea_model.invoke([HumanMessage(content=prompt)])

        raw          = response.content
        ideas        = []
        current_idea = {}

        for line in raw.split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.startswith("PROJECT") and line.endswith(":"):
                if current_idea:
                    ideas.append(current_idea)
                current_idea = {}

            elif line.startswith("TITLE:"):
                current_idea["title"] = line.replace("TITLE:", "").strip()

            elif line.startswith("DESCRIPTION:"):
                current_idea["description"] = line.replace("DESCRIPTION:", "").strip()

            elif line.startswith("TECH STACK:"):
                raw_stack = line.replace("TECH STACK:", "").strip()
                current_idea["tech_stack"] = [t.strip() for t in raw_stack.split(",")]

            elif line.startswith("DIFFICULTY:"):
                current_idea["difficulty"] = line.replace("DIFFICULTY:", "").strip()

            elif line.startswith("BUILD TIME:"):
                current_idea["build_time"] = line.replace("BUILD TIME:", "").strip()

            elif line.startswith("COMPETITION ANGLE:"):
                current_idea["competition_angle"] = line.replace("COMPETITION ANGLE:", "").strip()

        if current_idea:
            ideas.append(current_idea)

        return ideas

    except Exception as e:
        print(f"Claude ideas error: {e}")
        return []