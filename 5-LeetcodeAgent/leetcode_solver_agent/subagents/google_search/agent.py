"""
Google Search Agent

This agent searches for LeetCode problems using Google search.
It takes a problem name/description and finds the corresponding LeetCode URL.
"""

from google.adk.agents import LlmAgent
from .tools import search_leetcode_problem, fallback_leetcode_search

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the Google search agent
google_search_agent = LlmAgent(
    name="GoogleSearchAgent",
    model=GEMINI_MODEL,
    instruction="""You are a LeetCode Problem Search AI.
    
    Your task is to find LeetCode problems based on the user's search query or problem description.
    
    Process:
    1. First, try to search for the problem using search_leetcode_problem tool
    2. If that fails or returns no results, use fallback_leetcode_search tool
    3. Provide the user with the found LeetCode URL and problem information
    
    The user might provide:
    - Problem names like "Two Sum", "Add Two Numbers"  
    - Problem descriptions like "find two numbers that add up to target"
    - Partial problem names or keywords
    
    Your response should include:
    - Whether the search was successful
    - The LeetCode problem URL found
    - The problem slug extracted
    - Any additional context about the search process
    
    If no problem is found, suggest alternative search terms or ask for clarification.
    
    Store the problem URL and slug in a format that the next agent (scraper) can use.
    """,
    description="Searches for LeetCode problems using Google search and provides URLs for scraping.",
    tools=[search_leetcode_problem, fallback_leetcode_search],
    output_key="search_result"
)