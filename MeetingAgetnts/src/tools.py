import os
from exa_py import Exa
from langchain.agents import tool

class ExaSearchToolSet():

    # First Tool
    @tool
    def search(query:str):
        """Searh for a webpage based on the query"""
        return ExaSearchToolSet._exa().search(f"{query}", use_autoprompt=True, num_results=3), 
        
    # Second Tool
    @tool
    def find_similar(url, str):
        """Sear for webpages similar to a given URL
        the url passed in should be a URL returned from 'search' function.
        """

        return ExaSearchToolSet._exa().find_similar(url, num_results=3)

    # Third Tool
    @tool
    def get_contents(ids: str):
        """Get the contents of a webpage.
        the ids of webpages must be passe in as a list, a list of ids returned from 'Search' function.
        """
        print(" ids from param:", ids)  

        ids=eval(ids) #convert the string into an actual object

        contents =str(ExaSearchToolSet._exa().get_contents(ids))
        contents=contents.split("URL:")
        contents=[content[:1000] for content in contents] 
        return "\n\n".join(contents) #this is going to return the content in a string
       
    #this function will return a list of all the tools or function above, and we are going to use them
    #and through it we assigned the tools to our agents
    def tools():
        return [
            ExaSearchToolSet.search,
            ExaSearchToolSet.find_similar,
            ExaSearchToolSet.get_contents
        ]

    def _exa():
        return Exa(api_key=os.environ.get('EXA_API_KEY'))
