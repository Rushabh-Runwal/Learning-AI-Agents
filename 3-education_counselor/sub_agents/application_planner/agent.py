"""Risk Analysis Agent for providing the final risk evaluation"""

from google.adk import Agent
from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.0-flash"

application_planner = Agent(
    model=MODEL,
    name="application_planner",
    instruction=prompt.APPLICATION_PLANNER_SYSTEM_PROMPT,
    output_key="plan_output",
    tools=[google_search],
)
