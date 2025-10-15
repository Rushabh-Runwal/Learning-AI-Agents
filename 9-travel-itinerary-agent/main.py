"""Main entry point for the Travel Itinerary Planner multi-agent system."""

import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

# Load environment variables from .env file
load_dotenv()

# Initialize session service
session_service = InMemorySessionService()

# Initial state for travel planning
# Memory initialization callback will set up the full memory structure
initial_state = {
    "user_name": "Traveler",
}

# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"
    WHITE = "\033[37m"


async def process_agent_response(event):
    """Process and display agent response events."""
    final_response = None
    
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                text_content = part.text.strip()
                
                if event.is_final_response():
                    final_response = text_content
                    print(f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}TRAVEL AGENT:{Colors.RESET}")
                    print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
                    break
                else:
                    print(f"  {Colors.YELLOW}Processing: {text_content[:50]}...{Colors.RESET}")

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the travel agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"{Colors.RED}ERROR during agent run: {e}{Colors.RESET}")

    return final_response_text


async def main_async():
    """Main async function for the travel itinerary planner."""
    print("🌍 Travel Itinerary Planner - Multi-Agent System")
    print("=" * 60)

    # Validate environment variables
    google_api_key = os.getenv("GOOGLE_API_KEY")
    apify_api_token = os.getenv("APIFY_API_TOKEN")

    missing_keys = []
    if not google_api_key:
        missing_keys.append("GOOGLE_API_KEY")
    if not apify_api_token:
        missing_keys.append("APIFY_API_TOKEN")

    if missing_keys:
        print("❌ Missing required environment variables:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nPlease set the following environment variables:")
        print("   export GOOGLE_API_KEY='your-google-api-key'")
        print("   export APIFY_API_TOKEN='your-apify-token'")
        print("\nOr create a .env file with these values.")
        return

    print("✅ Environment configured")
    print("\nThis multi-agent system coordinates specialized agents:")
    print("  📍 Destination Research (Gemini 2.5 Flash-Lite)")
    print("  💰 Budget Planning (Gemini 2.5 Flash-Lite)")
    print("  ✈️  Flights Agent (Gemini 2.5 Flash + Apify)")
    print("  🏨 Hotels Agent (Gemini 2.5 Flash + Apify)")
    print("  🎭 Activities Agent (Gemini 2.5 Flash + Apify)")
    print("  📝 Itinerary Synthesizer (Gemini 2.5 Flash-Lite)")
    print("  🎯 Root Agent (Gemini 2.5 Pro)")
    print("\n" + "=" * 60)

    # Setup session
    APP_NAME = "Travel Itinerary Planner"
    USER_ID = "traveler_001"

    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    # Create runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print(f"\n{Colors.GREEN}Welcome to the Travel Itinerary Planner!{Colors.RESET}")
    print("Tell me about your travel preferences (destination, dates, budget, interests)")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input(f"{Colors.BG_GREEN}You:{Colors.RESET} ")

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input.strip():
            print("Please enter your travel preferences.")
            continue

        print(f"\n{Colors.BLUE}🤖 Processing your request...{Colors.RESET}")
        print("   The root agent is coordinating with specialized agents...")
        print("=" * 60)

        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    # Display final session state
    final_session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(f"\n{Colors.CYAN}Final Session State:{Colors.RESET}")
    for key, value in final_session.state.items():
        if key != "interaction_history":  # Skip long history
            print(f"{key}: {value}")


def main():
    """Main entry point."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
