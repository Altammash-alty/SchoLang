from langchain_core.prompts import PromptTemplate

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
idea_prompt=PromptTemplate(
    template=prompt,
    input_variables=["lang_name","title","abstract"]
    )
