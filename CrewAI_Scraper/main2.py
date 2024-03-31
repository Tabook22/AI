"New AI Agent Example"
#source: https://www.youtube.com/watch?v=8R7QOJgGyIQ&t=814s
#source: https://github.com/mberman84/crewai_yt
#packages needed: crewai,crewai-tools, langchain, langchain-community, openai,duckduckgo_search 


import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
# Assuming crewai_tools and langchain_community are correctly installed and imported
from crewai_tools import WebsiteSearchTool
from textwrap import dedent
from tools.scraper_tools import ScraperTool

# Load environment variables
load_dotenv()

scrape_tool = ScraperTool().scrape

class NewsletterCrew:
    def __init__(self, urls):
        self.urls = urls

    def run(self):
        # Define the scraper agent
        scraper = Agent(
            role="Summarizer of Websites",
            goal="Ask the user for a list of URLs, then go to each one of the given websites, scrape the content and provide the full content to the writer agent, so it can then summarize",
            backstory="""
            You work at a leading tech think tank,
            Your expertise is taking URLs and getting just the text-based content of them
            """,
            verbose=True,
            allow_delegation=False,
            tools=[scrape_tool]
        )

        # Define the writer agent
        writer = Agent(
            role="Tech Content Summarizer and Writer",
            goal="Craft compelling short-form content on AI advancements based on long-form text passed to you",
            backstory="""
            You are a renowned content creator, known for your insightful and engaging articles.
            You transform complex concepts into compelling narratives.
            """,
            verbose=True,
            allow_delegation=True,
        )

        # Define tasks
        task1 = Task(
            description=f"""Take a list of websites that contain AI content, read/scrape the content, 
            and then pass it to the writer agent to develop a short and compelling and interesting short-form summary of text about AI.
            Here are the URLs from the user that you need to scrape: {self.urls} """,
            agent=scraper,
            expected_output="An interesting and compelling AI content from the scraped URL content."
        )

        task2 = Task(
            description="""
            Based on the text provided by the scraper agent
            """,
            agent=writer,
            expected_output="A summary of the key points from the scraped URL content."
        )

        # Initialize and run the Crew
        newsletter_crew = Crew(
            agents=[scraper, writer],
            tasks=[task1, task2],
            verbose=2,
        )

        newsletter_crew.kickoff()

if __name__ == "__main__":
    print("## Welcome to Newsletter Writer")
    urls = input(
        dedent("""
        What is the URL you want to summarize?
        """)
    )

    # Instantiate NewsletterCrew with the provided URLs and run it
    newsletter_crew = NewsletterCrew(urls)
    newsletter_crew.run()

    print("\n\n====================================================================")
    print("## Here is the Result")
    # You would add logic here to display results based on how your Crew and Tasks are set up
