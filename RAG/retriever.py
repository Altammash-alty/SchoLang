from langchian_core.prompt import PromptTemplate



prompt="""You are an expert academic search engine.

Given a user query, your job is to retrieve the best 20 papers based on the user query by understanding the query and papers on the basis of keywords given in the user query and also the semantic meaning . Calculate the semantic scores also for the papers that are retrieved based on the query and papers.

USER QUERY: {query}


"""

