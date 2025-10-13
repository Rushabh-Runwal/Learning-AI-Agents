"""
Search Agent - Fast information gathering using Gemini Flash with Google ADK
"""

import google.generativeai as genai
from research_assistant.tools.search_tools import SEARCH_TOOLS, TOOL_FUNCTIONS


class SearchAgent:
    """Search agent using Gemini Flash for fast information gathering."""
    
    def __init__(self, api_key: str = None):
        """Initialize search agent with Gemini Flash model."""
        if api_key:
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            tools=SEARCH_TOOLS,
            system_instruction="""You are a specialized search agent focused on quickly finding 
            relevant information. Your responsibilities:
            - Break down queries into specific search terms
            - Search multiple sources for diverse perspectives
            - Extract and organize key facts
            - Prioritize recent and authoritative sources
            - Focus on gathering facts, not analysis
            
            Use the available search tools effectively."""
        )
    
    def search(self, query: str) -> str:
        """
        Gather information using search tools.
        
        Args:
            query: Research query
            
        Returns:
            Gathered information as string
        """
        print("   Gathering information...")
        
        prompt = f"""Research Query: {query}

Please:
1. Identify 3-5 specific search queries to gather comprehensive information
2. Use the search tools to find relevant information
3. Organize findings into clear categories
4. Highlight key facts and sources

Return structured information."""
        
        chat = self.model.start_chat(enable_automatic_function_calling=True)
        
        # Send message and handle function calls
        response = chat.send_message(prompt)
        
        # Handle any function calls
        while response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            function_args = dict(function_call.args)
            
            # Execute the function
            if function_name in TOOL_FUNCTIONS:
                result = TOOL_FUNCTIONS[function_name](**function_args)
                
                # Send result back to model
                response = chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=function_name,
                                response={"result": result}
                            )
                        )]
                    )
                )
        
        return response.text


def create_search_agent(api_key: str = None) -> SearchAgent:
    """Factory function to create search agent."""
    return SearchAgent(api_key=api_key)


def search_information(query: str, agent: SearchAgent = None, api_key: str = None) -> str:
    """Convenience function to search information."""
    if agent is None:
        agent = create_search_agent(api_key=api_key)
    return agent.search(query)
