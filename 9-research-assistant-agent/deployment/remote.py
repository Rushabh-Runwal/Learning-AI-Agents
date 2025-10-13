#!/usr/bin/env python3
"""
Research Assistant Agent - Remote Deployment Script
Deploy the agent to Vertex AI Agent Engines
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from research_assistant.adk_agent import root_agent
from research_assistant.config import (
    GOOGLE_CLOUD_PROJECT, 
    GOOGLE_CLOUD_LOCATION, 
    GOOGLE_CLOUD_STAGING_BUCKET
)

def create_deployment():
    """Create a new deployment of the research assistant agent."""
    print("🚀 Creating Research Assistant Agent Deployment")
    print("=" * 60)
    
    try:
        # Initialize Vertex AI
        import vertexai
        from vertexai import agent_engines
        
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        
        # Create deployment
        print("📦 Creating deployment...")
        deployment = vertexai.agent_engines.create(
            agent=root_agent,
            display_name="research-assistant-agent",
            description="AI Research Assistant for comprehensive research using search, analysis, and synthesis",
            requirements=[
                "google-adk==1.16.0",
                "google-generativeai>=0.8.5",
                "python-dotenv>=1.1.0",
                "requests>=2.31.0",
                "beautifulsoup4>=4.12.0",
                "lxml>=5.1.0"
            ],
            extra_packages=[
                "research_assistant",
                "research_assistant.subagents",
                "research_assistant.subagents.search_agent",
                "research_assistant.subagents.analyzer_agent", 
                "research_assistant.subagents.synthesizer_agent",
                "research_assistant.tools"
            ],
            staging_bucket=GOOGLE_CLOUD_STAGING_BUCKET
        )
        
        print("✅ Deployment created successfully!")
        print(f"📋 Resource ID: {deployment.resource_name}")
        print(f"🌐 Location: {deployment.location}")
        print(f"📅 Created: {deployment.create_time}")
        
        return deployment.resource_name
        
    except Exception as e:
        print(f"❌ Error creating deployment: {e}")
        return None

def delete_deployment(resource_id: str):
    """Delete a deployment."""
    print(f"🗑️  Deleting deployment: {resource_id}")
    
    try:
        import vertexai
        from vertexai import agent_engines
        
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        
        # Delete deployment
        agent_engines.delete(resource_id)
        print("✅ Deployment deleted successfully!")
        
    except Exception as e:
        print(f"❌ Error deleting deployment: {e}")

def list_deployments():
    """List all deployments."""
    print("📋 Listing Research Assistant Deployments")
    print("=" * 50)
    
    try:
        import vertexai
        from vertexai import agent_engines
        
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        
        # List deployments
        deployments = list(agent_engines.list())
        
        if not deployments:
            print("No deployments found.")
            return
        
        print(f"✅ Found {len(deployments)} deployment(s):")
        for i, deployment in enumerate(deployments, 1):
            print(f"  {i}. {deployment.resource_name}")
            print(f"     Display Name: {deployment.display_name}")
            print(f"     Created: {deployment.create_time}")
            print(f"     State: {deployment.state}")
            print()
        
    except Exception as e:
        print(f"❌ Error listing deployments: {e}")

def create_session(resource_id: str, user_id: str = "default_user"):
    """Create a session on the deployed agent."""
    print(f"🔄 Creating session on deployment: {resource_id}")
    print(f"👤 User ID: {user_id}")
    
    try:
        import vertexai
        from vertexai import agent_engines
        
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        
        # Get the deployed agent
        remote_app = agent_engines.get(resource_id)
        
        # Create session
        session = remote_app.create_session(user_id=user_id)
        
        print("✅ Session created successfully!")
        print(f"📋 Session ID: {session.get('id', session)}")
        if 'user_id' in session:
            print(f"👤 User ID: {session['user_id']}")
        if 'app_name' in session:
            print(f"📱 App Name: {session['app_name']}")
        if 'last_update_time' in session:
            print(f"🕒 Last Update: {session['last_update_time']}")
        
        return session
        
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        return None

def list_sessions(resource_id: str):
    """List sessions for a deployment."""
    print(f"📋 Listing sessions for deployment: {resource_id}")
    
    try:
        import vertexai
        from vertexai import agent_engines
        
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        
        # Get the deployed agent
        remote_app = agent_engines.get(resource_id)
        
        # List sessions
        sessions = list(remote_app.list_sessions())
        
        if not sessions:
            print("No sessions found.")
            return
        
        print(f"✅ Found {len(sessions)} session(s):")
        for i, session in enumerate(sessions, 1):
            print(f"  {i}. Session ID: {session.get('id', 'Unknown')}")
            print(f"     User ID: {session.get('user_id', 'Unknown')}")
            print(f"     Created: {session.get('create_time', 'Unknown')}")
            print()
        
    except Exception as e:
        print(f"❌ Error listing sessions: {e}")

def get_session(resource_id: str, session_id: str):
    """Get details of a specific session."""
    print(f"🔍 Getting session details: {session_id}")
    
    try:
        import vertexai
        from vertexai import agent_engines
        
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        
        # Get the deployed agent
        remote_app = agent_engines.get(resource_id)
        
        # Get session
        session = remote_app.get_session(session_id)
        
        print("✅ Session details:")
        print(f"📋 Session ID: {session.get('id', 'Unknown')}")
        print(f"👤 User ID: {session.get('user_id', 'Unknown')}")
        print(f"📱 App Name: {session.get('app_name', 'Unknown')}")
        print(f"🕒 Created: {session.get('create_time', 'Unknown')}")
        print(f"🕒 Last Update: {session.get('last_update_time', 'Unknown')}")
        
        return session
        
    except Exception as e:
        print(f"❌ Error getting session: {e}")
        return None

def send_message(resource_id: str, user_id: str, session_id: str, message: str):
    """Send a message to a session on the deployed agent."""
    print(f"\n📤 Sending message to session: {session_id}")
    print(f"💬 Message: {message}\n")
    
    try:
        import vertexai
        from vertexai import agent_engines
        
        vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        
        # Get the deployed agent
        remote_app = agent_engines.get(resource_id)
        
        print("🤖 Agent response:\n")
        print("-" * 80)
        
        for event in remote_app.stream_query(
            user_id=user_id,
            session_id=session_id,
            message=message,
        ):
            # Print all parts of the content, including tool calls and results
            if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        print(part.text)
                    elif hasattr(part, 'function_call'):
                        print(f"[tool call] {part.function_call.name}({part.function_call.args})")
                    elif hasattr(part, 'function_response'):
                        print(f"[tool result] {part.function_response.name}: {part.function_response.response}")
            elif isinstance(event, dict) and 'content' in event and 'parts' in event['content']:
                for part in event['content']['parts']:
                    if 'text' in part:
                        print(part['text'])
                    elif 'function_call' in part:
                        print(f"[tool call] {part['function_call']['name']}({part['function_call']['args']})")
                    elif 'function_response' in part:
                        print(f"[tool result] {part['function_response']['name']}: {part['function_response']['response']}")
            else:
                print(event)  # Fallback for other event types
        
        print("\n" + "-" * 80)
        print("✅ Message sent successfully!")
        
    except Exception as e:
        print(f"❌ Error sending message: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Research Assistant Agent Deployment")
    parser.add_argument("--create", action="store_true", help="Create new deployment")
    parser.add_argument("--delete", action="store_true", help="Delete deployment")
    parser.add_argument("--list", action="store_true", help="List deployments")
    parser.add_argument("--create_session", action="store_true", help="Create session")
    parser.add_argument("--list_sessions", action="store_true", help="List sessions")
    parser.add_argument("--get_session", action="store_true", help="Get session details")
    parser.add_argument("--send", action="store_true", help="Send message")
    
    parser.add_argument("--resource_id", type=str, help="Resource ID for operations")
    parser.add_argument("--session_id", type=str, help="Session ID for operations")
    parser.add_argument("--user_id", type=str, default="default_user", help="User ID")
    parser.add_argument("--message", type=str, help="Message to send")
    
    args = parser.parse_args()
    
    print("🔬 Research Assistant Agent - Vertex AI Deployment")
    print("=" * 60)
    
    if args.create:
        resource_id = create_deployment()
        if resource_id:
            print(f"\n💡 Next steps:")
            print(f"   1. Create session: python remote.py --create_session --resource_id={resource_id}")
            print(f"   2. Send message: python remote.py --send --resource_id={resource_id} --session_id=<session_id> --message='Your research query'")
    elif args.delete:
        if not args.resource_id:
            print("❌ --resource_id is required for delete operation")
            sys.exit(1)
        delete_deployment(args.resource_id)
    elif args.list:
        list_deployments()
    elif args.create_session:
        if not args.resource_id:
            print("❌ --resource_id is required for create_session operation")
            sys.exit(1)
        create_session(args.resource_id, args.user_id)
    elif args.list_sessions:
        if not args.resource_id:
            print("❌ --resource_id is required for list_sessions operation")
            sys.exit(1)
        list_sessions(args.resource_id)
    elif args.get_session:
        if not args.resource_id or not args.session_id:
            print("❌ --resource_id and --session_id are required for get_session operation")
            sys.exit(1)
        get_session(args.resource_id, args.session_id)
    elif args.send:
        if not all([args.resource_id, args.session_id, args.message]):
            print("❌ --resource_id, --session_id, and --message are required for send operation")
            sys.exit(1)
        send_message(args.resource_id, args.user_id, args.session_id, args.message)
    else:
        print("💡 Quick Start Examples:")
        print("   1. Deploy agent:        python remote.py --create")
        print("   2. List deployments:    python remote.py --list")
        print("   3. Create session:      python remote.py --create_session --resource_id=<id>")
        print("   4. List sessions:       python remote.py --list_sessions --resource_id=<id>")
        print("   5. Send message:        python remote.py --send --resource_id=<id> --session_id=<sid> --message='Research query'")
        print("   6. Delete deployment:   python remote.py --delete --resource_id=<id>")
        print("\n💡 Optional flags:")
        print("   --user_id=<id>         User ID for sessions (default: default_user)")
        print("   --project_id=<id>      Override GOOGLE_CLOUD_PROJECT")
        print("   --location=<loc>       Override GOOGLE_CLOUD_LOCATION")
        print("   --bucket=<gs://...>    Override GOOGLE_CLOUD_STAGING_BUCKET")

if __name__ == "__main__":
    main()
