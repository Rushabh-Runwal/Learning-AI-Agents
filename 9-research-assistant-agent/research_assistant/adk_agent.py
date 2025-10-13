"""
Research Assistant ADK Agent Wrapper
Converts the Research Assistant into an ADK-compatible agent
"""

from google.adk.agents import Agent
from research_assistant.agent import ResearchAssistant
from research_assistant.config import (
    USE_VERTEX_AI, 
    GOOGLE_CLOUD_PROJECT, 
    GOOGLE_CLOUD_LOCATION,
    SEARCH_MODEL,
    ANALYSIS_MODEL,
    SYNTHESIS_MODEL
)

# Import search tools
from research_assistant.tools.search_tools import TOOL_FUNCTIONS

def create_research_assistant_agent():
    """
    Create an ADK-compatible Research Assistant agent.
    
    Returns:
        Agent: ADK agent instance
    """
    
    # Initialize the research assistant
    research_assistant = ResearchAssistant()
    
    def conduct_research(query: str) -> str:
        """
        Conduct research using the research assistant.
        
        Args:
            query: Research query
            
        Returns:
            Final research report
        """
        try:
            results = research_assistant.conduct_research(query, verbose=False)
            return results.get("final_report", "No report generated")
        except Exception as e:
            return f"Error conducting research: {str(e)}"
    
    # Create the ADK agent
    agent = Agent(
        name="research_assistant",
        model=ANALYSIS_MODEL,  # Use the analysis model as the main model
        description="AI Research Assistant that conducts comprehensive research using search, analysis, and synthesis",
        instruction="""You are a specialized AI Research Assistant that helps users conduct thorough research on any topic. 

Your capabilities include:
1. **Search**: Finding relevant information from multiple sources
2. **Analysis**: Deep analysis of gathered information
3. **Synthesis**: Creating comprehensive research reports

When a user asks a research question:
1. Use the search tools to gather information
2. Analyze the information for insights and patterns
3. Synthesize everything into a comprehensive report

Always provide well-structured, factual, and comprehensive research reports with proper citations and sources.""",
        tools=list(TOOL_FUNCTIONS.values()) + [conduct_research]
    )
    
    return agent

# Create the root agent instance
root_agent = create_research_assistant_agent()
