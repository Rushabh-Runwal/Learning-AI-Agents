"""
Synthesizer Agent - Comprehensive synthesis using Gemini Pro with Google ADK
"""

import google.generativeai as genai


class SynthesizerAgent:
    """Synthesizer agent using Gemini Pro for report generation."""
    
    def __init__(self, api_key: str = None):
        """Initialize synthesizer agent with Gemini Pro model."""
        if api_key:
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-thinking-exp-01-21",
            system_instruction="""You are a specialized research synthesizer that creates 
            comprehensive, cohesive research reports. Your responsibilities:
            - Create clear, logical structure
            - Integrate information from search and analysis
            - Write in professional, academic tone
            - Use clear headings and sections
            - Include specific examples and evidence
            - Provide actionable insights
            - Cite sources appropriately
            - Directly address the original query
            
            Excel at creating well-structured research outputs."""
        )
    
    def synthesize(
        self, 
        original_query: str, 
        gathered_info: str, 
        analysis: str
    ) -> str:
        """
        Create comprehensive research report.
        
        Args:
            original_query: Original research query
            gathered_info: Information from search agent
            analysis: Analysis from analyzer agent
            
        Returns:
            Synthesized report as string
        """
        print("   Creating report...")
        
        prompt = f"""Research Query: {original_query}

Gathered Information:
{gathered_info}

Analysis:
{analysis}

Create a comprehensive research report with:
1. **Executive Summary** - Brief overview
2. **Introduction & Context** - Background
3. **Key Findings** - Detailed presentation
4. **Analysis & Insights** - Deep insights
5. **Discussion & Implications** - Significance
6. **Recommendations** - Actionable steps
7. **Conclusion** - Key takeaways
8. **Key Sources** - References

Write professionally and comprehensively."""
        
        response = self.model.generate_content(prompt)
        return response.text


def create_synthesizer_agent(api_key: str = None) -> SynthesizerAgent:
    """Factory function to create synthesizer agent."""
    return SynthesizerAgent(api_key=api_key)


def synthesize_research(
    original_query: str,
    gathered_info: str,
    analysis: str,
    agent: SynthesizerAgent = None,
    api_key: str = None
) -> str:
    """Convenience function to synthesize research."""
    if agent is None:
        agent = create_synthesizer_agent(api_key=api_key)
    return agent.synthesize(original_query, gathered_info, analysis)
