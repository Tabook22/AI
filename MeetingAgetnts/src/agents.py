from textwrap import dedent
from crewai import Agent
from tools import ExaSearchToolSet

class MeetingPrepAgents():

    # Each function is an agent and we can call the function and it will return the agent
    def research_agent(self):
        return Agent(
            role=" Research Specialist",
            goal=dedent("""
                Conduct thorough research on people and companies involved in the meeting
                """),
            tools=ExaSearchToolSet.tools(), #Get the tool function for the class ExaSearchToolSet
            backstory=dedent("""\
                As a Research Specilist, you mission is to uncover detailed information
                about the individuals and entities participating in the meeting. Your insights will lay the groundwork for stargegic meeting preparation
                """),
                verbose=True

        )
    
    def industry_analysis_agent(self):
        return Agent(
            role="Industyr Analysis",
            goal=dedent("""\
                Analyze the current industry trends, challenges, and opportunities,
                """),
            tools=ExaSearchToolSet.tools(), #Get the tool function for the class ExaSearchToolSet
            backstory=dedent("""\
                As an Industry Analyst, your analysis will identify key trends,
                             challenges facing the industry, and potential opportunities that
                             could be leveraged during the meeting for the strategic advantage.
                """),
                verbose=True
        )
    
    def meeting_strategy_agent(self):
        return Agent(
            role="Meeting Startegy Advisor",
            goal=dedent("""\
               Develop talking points, questins, and stargegic anagles for the meeting
                """),
            backstory=dedent("""\
                As a Strategy Advisor, you expertise will guide the development of talking points, 
                             insightful questions, and strategic angles
                             to ensure the meeting's objective are achieved.
                """),
                verbose=True
        )
    
    def summary_and_briefing_agent(self):
        return Agent(
            role="Briefing Coordinator",
            goal=dedent("""\
            Compiling all gathered information into a concise, informative briefing document
                """),
            backstory=dedent("""\
                 As the briefing Coordinator, your role is to consolidate the research, analysis, and stargegic insights.
                 """),
            verbose=True
        )