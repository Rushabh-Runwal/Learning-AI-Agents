"""Implementation_analyst_agent for developing implementation strategies for educational pathways"""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.0-flash"

eligibility_and_compliance_agent = Agent(
    model=MODEL,
    name="eligibility_and_compliance_agent",
    instruction=prompt.ELIGIBILITY_AND_COMPLIANCE_SYSTEM_PROMPT,
    output_key="eligibility_output",
    tools=[google_search],
)
