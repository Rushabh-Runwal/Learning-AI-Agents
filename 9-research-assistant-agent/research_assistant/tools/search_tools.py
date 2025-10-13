"""
Search tools for information gathering - Google ADK compatible
"""

import requests
from typing import List, Dict, Any


def web_search(query: str, num_results: int = 5) -> dict:
    """
    Web search tool for Google ADK agents.
    Returns mock results - integrate with real search API in production.
    
    Args:
        query: Search query string
        num_results: Number of results to return
        
    Returns:
        Dictionary with search results
    """
    print(f"🔍 Searching: {query}")
    
    results = [
        {
            "title": f"Result {i+1}: {query}",
            "snippet": f"Relevant information about {query} from source {i+1}",
            "url": f"https://example.com/result{i+1}"
        }
        for i in range(num_results)
    ]
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }


def fetch_webpage(url: str) -> dict:
    """
    Fetch webpage content.
    
    Args:
        url: URL to fetch
        
    Returns:
        Dictionary with content and metadata
    """
    try:
        print(f"📄 Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        return {
            "url": url,
            "content": response.text[:5000],
            "status": "success"
        }
    except Exception as e:
        return {
            "url": url,
            "content": "",
            "status": "error",
            "error": str(e)
        }


def search_academic(query: str) -> dict:
    """
    Search academic sources.
    Returns mock results - integrate with arXiv, Semantic Scholar in production.
    
    Args:
        query: Search query
        
    Returns:
        Dictionary with academic papers
    """
    print(f"🎓 Academic search: {query}")
    
    return {
        "query": query,
        "papers": [
            {
                "title": f"Research Paper on {query}",
                "authors": ["Research Team"],
                "abstract": f"Academic study discussing {query} and its implications",
                "url": "https://arxiv.org/example",
                "year": "2024"
            }
        ]
    }


# Tool declarations for Google ADK
SEARCH_TOOLS = [
    {
        "function_declarations": [
            {
                "name": "web_search",
                "description": "Search the web for information on a given query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "Number of results to return (default: 5)"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "fetch_webpage",
                "description": "Fetch content from a specific webpage URL",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to fetch"
                        }
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "search_academic",
                "description": "Search academic sources like arXiv and research papers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The academic search query"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    }
]


# Function mapping for tool execution
TOOL_FUNCTIONS = {
    "web_search": web_search,
    "fetch_webpage": fetch_webpage,
    "search_academic": search_academic
}
