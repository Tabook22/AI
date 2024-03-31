import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun

# Instantiate the tool
search_tool= DuckDuckGoSearchRun()

load_dotenv
#Create A Team Members

researcher=Agent(
    role="Senior Research Anayst",
    goal="Uncover cuttiong-edge developments in AI and data science",
    backstory="""
you work at leading tech think tank, 
your expertise lies in identifying emerging trends,
you have a knack for dissecting complex data and presenting actionable insights.
""",
verbose=True,
allow_delegation=False,
#llm="gpt-3.5-turbo",
tools=[search_tool]

)

writer =Agent(
    role="Tech Content Strategist",
    goal="Craft complelling content on tech advancements",
    backstory="""
You are a nenowned Content Strategist, know for you insightful and engagin articles.
you transform complex concepts inot complelling narratives.
 """,
    verbose=True,
    allow_delegation=False,
)

#Tasks
task1=Task(
    description="""
Conduct a comperhensive analysis of the latest advancements in AI
Identify key trends, breaktrhough technologies, and potential industry impacts.
your final answe MUST be a full analysis report
""",
agent=researcher,
expected_output="A detailed analysis report on the latest AI advancements."
)

task2= Task(
    description="""
Using the insights  provided, develop an engaging blog
post that highlights the most significatnt AI advancements.
you post should be informative yet accesible, catering to a tech-savvy audience.
Make it soudn cool, avoid complex words so it doesn't  sound like AI.
your fianl answer MUST be the full blog post of at least 4 paragrahos.
""",
agent=writer,
 expected_output="A blog post draft with at least 12 paragraphs."
)

task3 = Task(
    description="Search for the top tech news articles and provide the titles and URLs.",
    agent=researcher,
    expected_output="A list of the top 5 tech news articles with titles and URLs."
)

#Create Crew
crew=Crew(
    agents=[researcher, writer],
    tasks=[task1, task2, task3],
    verbose=2
)

#start work
result=crew.kickoff()
print(result)

'''
# Save the result to a text file
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(result)
'''
# Create the 'outputs' directory if it doesn't exist
os.makedirs('outputs', exist_ok=True)

# Save the result to a text file in the 'outputs' directory
with open('outputs/ai_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(result)