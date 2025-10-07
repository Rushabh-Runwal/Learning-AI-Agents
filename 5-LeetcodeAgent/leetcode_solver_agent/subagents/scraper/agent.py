"""
LeetCode Problem Analysis Agent

This agent analyzes LeetCode problem data using AI knowledge instead of web scraping.
It uses the URL found by the Google search agent to provide comprehensive problem information.
"""

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from datetime import datetime
from typing import Optional

# --- Constants ---
GEMINI_MODEL = "gemini-2.5-pro"

# Callback function to store summary in local file
def after_model_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """
    Store a short summary of the problem analysis in a local file.
    
    Args:
        callback_context: Contains state and context information
        llm_response: The LLM response received
        
    Returns:
        Optional LlmResponse to override model response (None to keep original)
    """
    try:
        # Get agent name and state
        agent_name = callback_context.agent_name
        state = callback_context.state
        
        # Extract text from the response
        response_text = ""
        if llm_response and llm_response.content and llm_response.content.parts:
            for part in llm_response.content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += part.text
        
        if not response_text:
            return None
            
        lines = response_text.split('\n')
        
        # Try to find the problem title
        problem_title = "Unknown Problem"
        for line in lines:
            if "title" in line.lower() or "problem" in line.lower():
                if ":" in line:
                    problem_title = line.split(":", 1)[1].strip()
                    break
        
        # Create a short summary
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary = f"Agent: {agent_name}\nProblem: {problem_title}\nAnalyzed at: {timestamp}\nStatus: Completed\n"
        
        # Append to local file
        with open("problem_analysis_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{'='*50}\n")
            f.write(summary)
            f.write(f"{'='*50}\n\n")
            
        print(f"[AFTER MODEL] ✓ Logged analysis summary for: {problem_title}")
            
    except Exception as e:
        print(f"Error in callback: {e}")
    
    # Return None to keep the original response
    return None

# Create the scraper agent without tools
leetcode_scraper_agent = LlmAgent(
    name="LeetCodeProblemAnalysis",
    model=GEMINI_MODEL,
    instruction="""You are a LeetCode Problem Data Extraction AI.

    Your task is to extract and provide LeetCode problem information based on the search results from the previous agent.
    
    You will receive search results that contain:
    - Problem URL (e.g., https://leetcode.com/problems/two-sum/)
    - Problem slug (e.g., two-sum)
    - Search query information
    
    Based on this information, provide comprehensive problem data including:
    - Problem title and number (e.g., "1. Two Sum")
    - Difficulty level (Easy/Medium/Hard)
    - Detailed problem description
    - Input/Output examples with explanations
    - Constraints and edge cases
    - Problem category/tags (Array, Hash Table, etc.)
    
    Use your knowledge of LeetCode problems to provide accurate and complete information.
    If you don't have specific knowledge of a problem, provide a general structure and mention that detailed scraping would be needed.
    
    Format your response as structured problem data that the next agent can easily analyze.
    """,
    description="Analyzes LeetCode problem information using AI knowledge instead of web scraping.",
    output_key="scraped_problem_data",
    after_model_callback=after_model_callback
)