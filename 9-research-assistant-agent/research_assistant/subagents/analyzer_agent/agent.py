"""
Analyzer Agent - Deep analysis using Gemini Pro with Google ADK
"""

import google.generativeai as genai


class AnalyzerAgent:
    """Analyzer agent using Gemini Pro for deep reasoning."""
    
    def __init__(self, api_key: str = None):
        """Initialize analyzer agent with Gemini Pro model."""
        if api_key:
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-thinking-exp-01-21",
            system_instruction="""You are a specialized research analyst with deep reasoning capabilities.
            Your responsibilities:
            - Analyze information critically and objectively
            - Look for patterns, contradictions, and connections
            - Evaluate quality and credibility of sources
            - Identify key insights and their implications
            - Note gaps or areas needing further investigation
            - Consider multiple perspectives
            - Provide evidence-based conclusions
            
            Excel at deep thinking and nuanced analysis."""
        )
    
    def analyze(self, gathered_info: str, original_query: str) -> str:
        """
        Deeply analyze gathered information.
        
        Args:
            gathered_info: Information from search agent
            original_query: Original research query
            
        Returns:
            Analysis as string
        """
        print("   Analyzing information...")
        
        prompt = f"""Original Query: {original_query}

Gathered Information:
{gathered_info}

Perform deep analysis covering:
1. Key Insights - Most important findings
2. Patterns & Trends - What emerges from the data
3. Critical Evaluation - Credibility and significance  
4. Connections - Links between information
5. Gaps - Missing information
6. Implications - Broader impact

Provide thorough, evidence-based analysis."""
        
        response = self.model.generate_content(prompt)
        return response.text


def create_analyzer_agent(api_key: str = None) -> AnalyzerAgent:
    """Factory function to create analyzer agent."""
    return AnalyzerAgent(api_key=api_key)


def analyze_information(
    gathered_info: str, 
    original_query: str, 
    agent: AnalyzerAgent = None,
    api_key: str = None
) -> str:
    """Convenience function to analyze information."""
    if agent is None:
        agent = create_analyzer_agent(api_key=api_key)
    return agent.analyze(gathered_info, original_query)
