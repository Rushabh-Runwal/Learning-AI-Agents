"""
Research Assistant Agent - Main Entry Point
Day 9: LLM Selection & Control Logic with Google ADK
"""

import os
from research_assistant.agent import create_research_assistant


def main():
    """Main function to run the Research Assistant."""
    
    print("\n🔬 RESEARCH ASSISTANT AGENT (Google ADK)")
    print("Day 9: LLM Selection & Control Logic")
    print("-" * 50)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n⚠️  GOOGLE_API_KEY not set!")
        print("Get your key: https://aistudio.google.com/app/apikey")
        print("Then: export GOOGLE_API_KEY='your-key-here'\n")
        return
    
    # Create the research assistant
    assistant = create_research_assistant(api_key=api_key)
    
    # Example queries
    examples = [
        "What are the latest developments in quantum computing?",
        "How does climate change affect ocean ecosystems?",
        "What are the ethical implications of AI in healthcare?",
        "Explain the current state of fusion energy research"
    ]
    
    print("\n📚 Example Topics:")
    for i, example in enumerate(examples, 1):
        print(f"   {i}. {example}")
    print(f"   {len(examples) + 1}. Enter custom query")
    
    while True:
        try:
            choice = input(f"\nSelect (1-{len(examples) + 1}): ").strip()
            
            if choice == str(len(examples) + 1):
                query = input("Enter your research query: ").strip()
                if not query:
                    print("❌ Query cannot be empty!")
                    continue
            elif choice.isdigit() and 1 <= int(choice) <= len(examples):
                query = examples[int(choice) - 1]
            else:
                print("❌ Invalid choice!")
                continue
            
            print(f"\n🚀 Researching: {query}\n")
            
            # Conduct research
            results = assistant.conduct_research(query, verbose=True)
            
            # Display final report
            print("\n" + "="*70)
            print("📄 FINAL REPORT")
            print("="*70 + "\n")
            print(results.get("final_report", "No report generated"))
            print("\n" + "="*70)
            
            # Ask if user wants another query
            another = input("\n🔄 Research another topic? (y/n): ").strip().lower()
            if another != 'y':
                print("\n👋 Goodbye!\n")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
