"""
Local deployment script for Content Orchestration Agent
Allows testing the agent locally before deploying to Vertex AI
"""

import os
import sys
import vertexai
from dotenv import load_dotenv
from vertexai.preview import reasoning_engines

from content_orchestration import root_agent


def init_local_app():
    """Initialize the local ADK app with Vertex AI"""
    load_dotenv()
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    
    if not project_id:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        sys.exit(1)
    elif not location:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        sys.exit(1)
    
    # Initialize Vertex AI
    print(f"🔧 Initializing Vertex AI with project={project_id}, location={location}")
    vertexai.init(
        project=project_id,
        location=location,
    )
    
    # Create the local app instance
    print("📦 Creating local app instance...")
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )
    
    return app


def create_session(user_id: str = "test_user"):
    """Create a new session for the agent"""
    print("\n🔄 Creating new session...")
    app = init_local_app()
    
    session = app.create_session(user_id=user_id)
    print(f"✅ Session created successfully!")
    print(f"  📋 Session ID: {session.id}")
    print(f"  👤 User ID: {session.user_id}")
    print(f"  📱 App name: {session.app_name}")
    print(f"\n💡 Use this session ID to send messages:")
    print(f"   poetry run deploy-local --send --session_id={session.id} --user_id={user_id} --message='Your message'")
    return session


def list_sessions(user_id: str = "test_user"):
    """List all active sessions"""
    print("\n🔄 Fetching sessions...")
    app = init_local_app()
    
    sessions = app.list_sessions(user_id=user_id)
    
    # Handle different response formats
    session_list = []
    if hasattr(sessions, "sessions"):
        session_list = sessions.sessions
    elif hasattr(sessions, "session_ids"):
        session_list = sessions.session_ids
    elif isinstance(sessions, list):
        session_list = sessions
    
    if not session_list:
        print("📭 No active sessions found")
        print("\n💡 Create a new session with:")
        print("   poetry run deploy-local --create_session")
        return
    
    print(f"✅ Found {len(session_list)} session(s):")
    for session in session_list:
        if isinstance(session, dict):
            print(f"  📋 Session ID: {session.get('id', session)}")
        else:
            print(f"  📋 Session ID: {session}")


def send_message(user_id: str, session_id: str, message: str):
    """Send a message to a session"""
    print(f"\n📤 Sending message to session: {session_id}")
    print(f"💬 Message: {message}\n")
    
    app = init_local_app()
    
    print("🤖 Agent response:\n")
    print("-" * 80)
    
    for event in app.stream_query(
        user_id=user_id,
        session_id=session_id,
        message=message,
    ):
        print(event)
    
    print("\n" + "-" * 80)
    print("✅ Message sent successfully!")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Local deployment tool for Content Orchestration Agent"
    )
    
    parser.add_argument(
        '--create_session',
        action='store_true',
        help='Create a new session'
    )
    
    parser.add_argument(
        '--list_sessions',
        action='store_true',
        help='List all active sessions'
    )
    
    parser.add_argument(
        '--send',
        action='store_true',
        help='Send a message to a session'
    )
    
    parser.add_argument(
        '--user_id',
        type=str,
        default='test_user',
        help='User ID for operations (default: test_user)'
    )
    
    parser.add_argument(
        '--session_id',
        type=str,
        help='Session ID for operations'
    )
    
    parser.add_argument(
        '--message',
        type=str,
        help='Message to send to the agent'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("\n" + "=" * 80)
    print("🚀 Content Orchestration Agent - Local Testing")
    print("=" * 80)
    
    # Handle commands
    if args.create_session:
        create_session(args.user_id)
    
    elif args.list_sessions:
        list_sessions(args.user_id)
    
    elif args.send:
        if not args.session_id or not args.message:
            print("❌ Error: --session_id and --message are required for --send")
            return
        send_message(args.user_id, args.session_id, args.message)
    
    else:
        parser.print_help()
        print("\n💡 Quick Start Examples:")
        print("   1. Create a session:    poetry run deploy-local --create_session")
        print("   2. List sessions:       poetry run deploy-local --list_sessions")
        print("   3. Send a message:      poetry run deploy-local --send --session_id=<id> --message='Create content about Python'")
        print("\n💡 Optional flags:")
        print("   --user_id=<id>         User ID for sessions (default: test_user)")


if __name__ == "__main__":
    main()

