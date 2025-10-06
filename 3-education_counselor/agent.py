"""Education Path Advisor: provide personalized educational pathway guidance for Indian students"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.program_matcher_agent import program_matcher_agent 
from .sub_agents.application_planner import application_planner
# from .sub_agents.eligibility_and_compliance_agent import eligibility_and_compliance_agent
from .sub_agents.budget_and_funding_agent import budget_and_funding_agent

MODEL = "gemini-2.0-flash"


education_counselor = Agent(
    name="education_counselor",
    model=MODEL,
    description=('Coordinator agent for the Education Path Advisor, helping users navigate their educational journey.'),
    instruction=prompt.EDUCATION_COUNSELOR_SYSTEM_PROMPT,
    output_key="education_counselor",
    sub_agents=[
        program_matcher_agent,
        # eligibility_and_compliance_agent,
        application_planner,
        budget_and_funding_agent,
    ],
)

root_agent = education_counselor
