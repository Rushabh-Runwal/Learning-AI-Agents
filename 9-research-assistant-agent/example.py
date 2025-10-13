"""
Example usage of Research Assistant Agent with Google ADK
"""

import os
from research_assistant.agent import create_research_assistant, quick_research


def example_basic_usage():
    """Example 1: Basic usage."""
    print("="*70)
    print("Example 1: Basic Usage")
    print("="*70)
    
    # Create assistant
    assistant = create_research_assistant()
    
    # Conduct research
    results = assistant.conduct_research(
        "What is quantum entanglement?",
        verbose=True
    )
    
    # Access different parts
    print("\n📊 Results structure:")
    print(f"- Query: {results['query']}")
    print(f"- Search results: {len(results.get('search_results', ''))} chars")
    print(f"- Analysis: {len(results.get('analysis', ''))} chars")
    print(f"- Final report: {len(results.get('final_report', ''))} chars")


def example_quick_research():
    """Example 2: Quick research function."""
    print("\n" + "="*70)
    print("Example 2: Quick Research")
    print("="*70)
    
    # Quick research - just get the final report
    report = quick_research("What are neural networks?")
    
    print("\n📄 Final Report:")
    print(report[:500] + "...")


def example_with_api_key():
    """Example 3: Explicit API key."""
    print("\n" + "="*70)
    print("Example 3: With Explicit API Key")
    print("="*70)
    
    # Pass API key explicitly
    api_key = os.getenv("GOOGLE_API_KEY")
    
    assistant = create_research_assistant(api_key=api_key)
    results = assistant.conduct_research("What is machine learning?")
    
    print(f"\n✅ Research completed on: {results['query']}")


def example_error_handling():
    """Example 4: Error handling."""
    print("\n" + "="*70)
    print("Example 4: Error Handling")
    print("="*70)
    
    try:
        assistant = create_research_assistant()
        results = assistant.conduct_research("Example query", verbose=False)
        
        if "error" in results.get("final_report", "").lower():
            print("⚠️  Error occurred during research")
        else:
            print("✅ Research successful")
    except Exception as e:
        print(f"❌ Exception caught: {e}")


if __name__ == "__main__":
    print("\n🔬 RESEARCH ASSISTANT EXAMPLES (Google ADK)\n")
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Set GOOGLE_API_KEY environment variable first!")
        print("export GOOGLE_API_KEY='your-key-here'\n")
        exit(1)
    
    # Run examples
    try:
        example_basic_usage()
        # example_quick_research()  # Uncomment to run
        # example_with_api_key()     # Uncomment to run
        # example_error_handling()   # Uncomment to run
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

