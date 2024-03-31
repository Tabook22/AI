from textwrap import dedent
from crewai import Task

class MeetingPrepTasks():

    # Each task in a function, and we can call teh function and it will return the task
    def research_task(self, agent, meeting_participants, meeting_context):
        return Task(
            description= dedent(f"""\
              Conduct comprehensive research on each of the individuals and companies
                involved in the upcoming meeting. Gather information on recent
                news, achievements, professional background, and any relevant
                business activities.
            Participants: {meeting_participants}
            Meeting Context:{meeting_context}"""),
            expected_output=dedent("""\
            A detailed report summarizing key findings about each participant
            and company, highlighting information that could be relevant for the meeting.
                                   """),
            async_execution=True,
            agent=agent
        )
    
    def industry_analysis_task(self, agent, meeting_participants, meeting_context):
        return Task(
            description= dedent(f"""\
            Analyze the current industry trends, callanges, and opportunities
                                relevant to the meeting's context. Consider market reports, recent
                                developments, and expert opinions to provide a comperehensive overviewo fthe industry landscape.
            Participants: {meeting_participants}
            Meeting Context:{meeting_context}"""),
            expected_output=dedent("""\
            AAn insightful analysis that identifies majro trends, potential callenges, and strategic oportuniteis.
                                   """),
            async_execution=True,
            agent=agent
        )
    
    def meeting_strategy_task(self,agent, meeting_context, meeting_objective):
        return Task(
            description=dedent(f"""\
            develop startegic talking points, questions, and discussion angles form teh meeting based on the research and industry analysis doducted
            
            Meeting Contecx: {meeting_context}
            Meeting Objective: {meeting_objective}
            """),
            expected_output=dedent("""\
            Complete report with a list of key talking points, startegic questions
                                   to ask to help achieve the meetings objective during the meeting.    
            """),
            agent=agent
        )
    
    def summary_and_briefing_task(self, agent, meeting_context, meeting_objective):
        return Task(
            description=dedent(f"""\
                Compile all the research findings, industry analysis, and startegic talking points into a concise, comprehnesive briefing document for the meeting.
                ensure the brefing is easy to digst and equips the meeting particpant with all necessary information and startegies

                Meeting Context: {meeting_context}
                Meeting Objective: {meeting_objective}
                """),
            expected_output=dedent("""\""""),
            agent=agent
            
        )