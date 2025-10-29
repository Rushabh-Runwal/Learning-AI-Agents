"""
LeetCode Solver Sequential Agent

This agent demonstrates a sequential workflow for:
1. Searching for LeetCode problems using Google search
2. Analyzing problem data using AI knowledge 
3. Providing comprehensive solution approaches and analysis

The agent executes subagents in a predefined order, passing data between them
using state management.
"""

from google.adk.agents import SequentialAgent

from .subagents.google_search.agent import google_search_agent
from .subagents.scraper.agent import leetcode_scraper_agent  
from .subagents.solution_analyzer.agent import solution_analyzer_agent

# Create the sequential agent
root_agent = SequentialAgent(
    name="LeetCodeSolverPipeline",
    sub_agents=[google_search_agent, leetcode_scraper_agent, solution_analyzer_agent],
    description="A pipeline that searches for LeetCode problems, analyzes problem data, and provides comprehensive solution analysis",
)