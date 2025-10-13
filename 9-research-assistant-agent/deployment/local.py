#!/usr/bin/env python3
"""
Research Assistant Agent - Local Deployment Script
Test the agent locally using Vertex AI
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from research_assistant.adk_agent import root_agent
from research_assistant.config import GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION

def test_local_agent():
    """Test the research assistant agent locally."""
    print("🔬 Testing Research Assistant Agent Locally")
    print("=" * 50)
    
    try:
        # Initialize Vertex AI
        import vertexai
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        
        # Create local app
        from vertexai.preview import reasoning_engines
        app = reasoning_engines.AdkApp(agent=root_agent, enable_tracing=True)
        
        print("✅ Agent initialized successfully!")
        
        # Test queries
        test_queries = [
            "What are the latest developments in quantum computing?",
            "How does climate change affect ocean ecosystems?",
            "What are the ethical implications of AI in healthcare?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test Query {i}: {query}")
            print("-" * 50)
            
            try:
                # Create session
                session = app.create_session(user_id="test_user")
                print(f"📋 Session created: {session.id}")
                
                # Send message
                response_text = ""
                for event in app.stream_query(
                    user_id="test_user",
                    session_id=session.id,
                    message=query,
                ):
                    if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response_text += part.text
                            elif hasattr(part, 'function_call'):
                                print(f"🔧 Tool call: {part.function_call.name}")
                            elif hasattr(part, 'function_response'):
                                print(f"✅ Tool response: {part.function_response.name}")
                
                print(f"📄 Response: {response_text[:200]}...")
                print("✅ Test completed successfully!")
                
            except Exception as e:
                print(f"❌ Test failed: {e}")
        
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test Research Assistant Agent locally")
    parser.add_argument("--test", action="store_true", help="Run local tests")
    
    args = parser.parse_args()
    
    if args.test:
        success = test_local_agent()
        sys.exit(0 if success else 1)
    else:
        print("Usage: python local.py --test")
        sys.exit(1)

if __name__ == "__main__":
    main()
