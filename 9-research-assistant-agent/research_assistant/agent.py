"""
Research Assistant Agent - Main orchestrator using Google ADK
Sequential workflow: Search → Analyze → Synthesize
"""

import os
from typing import Dict, Any
import google.generativeai as genai

from research_assistant.subagents.search_agent.agent import (
    create_search_agent,
    search_information
)
from research_assistant.subagents.analyzer_agent.agent import (
    create_analyzer_agent,
    analyze_information
)
from research_assistant.subagents.synthesizer_agent.agent import (
    create_synthesizer_agent,
    synthesize_research
)


class ResearchAssistant:
    """
    Research Assistant with strategic LLM selection using Google ADK:
    - Gemini Flash for fast searches
    - Gemini Pro for deep analysis and synthesis
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Research Assistant with specialized sub-agents.
        
        Args:
            api_key: Google API key (optional, can use GOOGLE_API_KEY env var)
        """
        print("🔬 Initializing Research Assistant (Google ADK)...")
        
        # Configure API key
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        # Create specialized sub-agents
        self.search_agent = create_search_agent(api_key=self.api_key)
        self.analyzer_agent = create_analyzer_agent(api_key=self.api_key)
        self.synthesizer_agent = create_synthesizer_agent(api_key=self.api_key)
        
        print("✅ Ready!")
    
    def conduct_research(self, query: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Conduct research using sequential workflow:
        1. Search (Gemini Flash) - Fast information gathering
        2. Analyze (Gemini Pro) - Deep analysis
        3. Synthesize (Gemini Pro) - Report generation
        
        Args:
            query: Research query
            verbose: Print progress updates
            
        Returns:
            Dictionary with all research outputs
        """
        
        if verbose:
            print("\n" + "="*70)
            print(f"📋 Query: {query}")
            print("="*70)
        
        results = {"query": query}
        
        # STAGE 1: Search (Gemini Flash)
        if verbose:
            print("\n🔍 STAGE 1: Search (Gemini Flash)")
        
        try:
            search_results = self.search_agent.search(query)
            results["search_results"] = search_results
            if verbose:
                print("✅ Search complete")
        except Exception as e:
            print(f"❌ Search error: {e}")
            results["search_results"] = f"Error: {e}"
            return results
        
        # STAGE 2: Analysis (Gemini Pro)
        if verbose:
            print("\n🔬 STAGE 2: Analysis (Gemini Pro)")
        
        try:
            analysis = self.analyzer_agent.analyze(search_results, query)
            results["analysis"] = analysis
            if verbose:
                print("✅ Analysis complete")
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            results["analysis"] = f"Error: {e}"
            return results
        
        # STAGE 3: Synthesis (Gemini Pro)
        if verbose:
            print("\n📝 STAGE 3: Synthesis (Gemini Pro)")
        
        try:
            final_report = self.synthesizer_agent.synthesize(
                query, 
                search_results, 
                analysis
            )
            results["final_report"] = final_report
            if verbose:
                print("✅ Synthesis complete\n" + "="*70)
        except Exception as e:
            print(f"❌ Synthesis error: {e}")
            results["final_report"] = f"Error: {e}"
        
        return results
    
    def get_final_report(self, query: str) -> str:
        """
        Get just the final report.
        
        Args:
            query: Research query
            
        Returns:
            Final research report
        """
        results = self.conduct_research(query, verbose=True)
        return results.get("final_report", "No report generated")


def create_research_assistant(api_key: str = None) -> ResearchAssistant:
    """
    Create a Research Assistant instance.
    
    Args:
        api_key: Google API key (optional)
        
    Returns:
        Configured ResearchAssistant
    """
    return ResearchAssistant(api_key=api_key)


def quick_research(query: str, api_key: str = None) -> str:
    """
    Quick research - returns final report.
    
    Args:
        query: Research query
        api_key: Google API key (optional)
        
    Returns:
        Final research report
    """
    assistant = create_research_assistant(api_key=api_key)
    return assistant.get_final_report(query)
