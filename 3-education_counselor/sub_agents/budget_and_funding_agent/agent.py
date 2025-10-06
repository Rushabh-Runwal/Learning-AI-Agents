"""Pathway_analyst_agent for developing educational pathway strategies"""

from google.adk import Agent
from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.0-flash"

budget_and_funding_agent = Agent(
    model=MODEL,
    name="budget_and_funding_agent",
    instruction=prompt.BUDGETING_AND_FUNDING_SYSTEM_PROMPT,
    output_key="budget_output",
    tools=[google_search],
)
