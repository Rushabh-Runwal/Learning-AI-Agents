#!/usr/bin/env python3
"""
LeetCode Solver Sequential Agent Runner

This script runs the LeetCo            print("👋 Goodbye! Happy coding!")
            break
        except Exception as e:solver pipeline that:
1. Validates LeetCode problem URLs
2. Scrapes problem data 
3. Provides solution analysis

Usage:
    python main.py
"""

import asyncio
from dotenv import load_dotenv

from leetcode_solver_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk import types

# Load environment variables
load_dotenv()

def main():
    """Main function to run the LeetCode solver agent."""
    
    # Initialize session service
    session_service = InMemorySessionService()
    
    # Create initial session state
    initial_state = {
        "search_result": "",
        "scraped_problem_data": "",
        "solution_analysis_result": "",
        "user_id": "leetcode_user_001",
        "user_message": ""
    }
    
    # Session configuration
    APP_NAME = "LeetCode Solver"
    USER_ID = "leetcode_user_001"
    
    # Create new session
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )
    SESSION_ID = session.id
    
    print("🚀 LeetCode Solver Sequential Agent")
    print("=" * 50)
    print("This agent will help you analyze LeetCode problems!")
    print("Simply describe the problem you want to solve, and I'll find and analyze it.")
    print("Examples:")
    print("  - 'Two Sum'")
    print("  - 'find two numbers that add up to target'")
    print("  - 'Add Two Numbers linked list'")
    print("Type 'exit' to quit.\n")
    
    # Create runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("� Enter problem name or description: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye! Happy coding!")
                break
                
            if not user_input:
                print("⚠️  Please enter a problem name/description or 'exit' to quit.")
                continue
            
            print(f"\n🔄 Processing: {user_input}")
            print("-" * 50)
            
            # Store user input in session state for the Google search agent to access
            current_session = session_service.get_session(APP_NAME, USER_ID, SESSION_ID)
            current_session.state["user_message"] = user_input
            
            # Run the sequential agent pipeline
            asyncio.run(run_agent_pipeline(runner, USER_ID, SESSION_ID, user_input))
            
            print("\n" + "=" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Happy coding!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again with a different problem description.")

async def run_agent_pipeline(runner, user_id, session_id, query):
    """Run the agent pipeline asynchronously."""
    
    # Create message content
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    try:
        # Process the query through the sequential pipeline
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id, 
            new_message=content
        ):
            # Handle agent responses
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text:
                        print(f"🤖 {event.author}: {part.text.strip()}")
            else:
                # Show intermediate progress for non-final responses
                if hasattr(event, 'author') and event.author:
                    print(f"⚙️  {event.author}: Processing...")
                    
    except Exception as e:
        print(f"❌ Pipeline Error: {e}")
        print("The agent encountered an issue. Please try again.")

def display_session_state(runner, app_name, user_id, session_id):
    """Display current session state for debugging."""
    try:
        session = runner.session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        print("\n📊 Session State:")
        print("-" * 30)
        for key, value in session.state.items():
            if key in ['search_result', 'scraped_problem_data', 'solution_analysis_result'] and value:
                print(f"✅ {key}: Available")
            elif key in ['search_result', 'scraped_problem_data', 'solution_analysis_result']:
                print(f"⏳ {key}: Pending")
        print("-" * 30)
        
    except Exception as e:
        print(f"⚠️  Could not display session state: {e}")

if __name__ == "__main__":
    main()