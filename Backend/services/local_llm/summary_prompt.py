from langchain_core.prompt import PromptTemplate

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
summary_prompt = PromptTemplate(
    template=prompt,
    input_variables=["lang_name", "abstract"],
    output_parser=PydanticOutputParser(pydantic_object=PaperSummary)
)