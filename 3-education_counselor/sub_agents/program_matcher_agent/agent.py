"""Education data analyst agent for finding educational information using Google search"""

from google.adk import Agent
from google.adk.tools import google_search
from .sub_agents.eligibility_and_compliance_agent import eligibility_and_compliance_agent
from google.adk.tools import agent_tool

from . import prompt

MODEL = "gemini-2.5-pro"

program_matcher_agent = Agent(
    model=MODEL,
    name="program_matcher_agent",
    instruction=prompt.PROGRAM_MATCHER_SYSTEM_PROMPT,
    output_key="program_match_output",
    tools=[ 
        agent_tool.AgentTool(agent=eligibility_and_compliance_agent)
    ],
)
