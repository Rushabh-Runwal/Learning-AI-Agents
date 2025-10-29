"""Main course generator agent with sequential workflow"""

from google.adk.agents import Agent, SequentialAgent, LoopAgent

from .sub_agents.topic_planner import topic_planner_agent
from .sub_agents.game_generator import game_generator_agent
from .sub_agents.validator import validator_agent
from .prompts import COURSE_GENERATOR_SYSTEM_PROMPT

MODEL = "gemini-2.5-pro"

# Create validator as a loop agent that keeps fixing until validation passes
validator_loop_agent = LoopAgent(
    name="validator_loop",
    sub_agents=[validator_agent],
    max_iterations=3,
    description="Validates and fixes generated games until they pass all checks",
)

# Create the sequential workflow: Topic Planning → Game Generation → Validation Loop
course_generator_agent = SequentialAgent(
    name="course_generator",
    description="Sequential workflow for generating interactive educational content",
    sub_agents=[
        topic_planner_agent,      # Step 1: Plan the learning structure
        game_generator_agent,     # Step 2: Generate game files
        validator_loop_agent,     # Step 3: Validate and fix (loops until valid)
    ],
)

root_agent = course_generator_agent