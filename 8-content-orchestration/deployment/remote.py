"""
Remote deployment script for Content Orchestration Agent on Vertex AI
Handles deployment, session management, and cleanup using Vertex AI Agent Engines
"""

import os
import sys
import vertexai
from absl import app, flags
from dotenv import load_dotenv
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from content_orchestration import root_agent

FLAGS = flags.FLAGS
flags.DEFINE_string("project_id", None, "GCP project ID.")
flags.DEFINE_string("location", None, "GCP location.")
flags.DEFINE_string("bucket", None, "GCP staging bucket.")
flags.DEFINE_string("resource_id", None, "Agent Engine resource ID.")
flags.DEFINE_string("user_id", "default_user", "User ID for session operations.")
flags.DEFINE_string("session_id", None, "Session ID for operations.")
flags.DEFINE_bool("create", False, "Creates a new deployment.")
flags.DEFINE_bool("delete", False, "Deletes an existing deployment.")
flags.DEFINE_bool("list", False, "Lists all deployments.")
flags.DEFINE_bool("create_session", False, "Creates a new session.")
flags.DEFINE_bool("list_sessions", False, "Lists all sessions for a user.")
flags.DEFINE_bool("get_session", False, "Gets a specific session.")
flags.DEFINE_bool("send", False, "Sends a message to the deployed agent.")
flags.DEFINE_string(
    "message",
    "Create a quiz about Python with 5 questions",
    "Message to send to the agent.",
)
flags.mark_bool_flags_as_mutual_exclusive(
    [
        "create",
        "delete",
        "list",
        "create_session",
        "list_sessions",
        "get_session",
        "send",
    ]
)


def create_deployment():
    """Deploy the agent to Vertex AI"""
    print("\n🔄 Deploying agent to Vertex AI...")
    print("⏳ This may take several minutes...")
    
    try:
        # Wrap the agent in AdkApp
        adk_app = reasoning_engines.AdkApp(
            agent=root_agent,
            enable_tracing=True,
        )
        
        # Deploy to Agent Engine
        remote_app = agent_engines.create(
            agent_engine=adk_app,
            requirements=[
                "google-cloud-aiplatform[adk,agent_engines]",
                "google-adk>=1.16.0",
                "google-generativeai>=0.8.5",
                "python-dotenv>=1.1.0",
            ],
            extra_packages=["./content_orchestration"],
        )
        
        print(f"\n✅ Agent deployed successfully!")
        print(f"📋 Resource ID: {remote_app.resource_name}")
        print(f"\n💡 Next steps:")
        print(f"   1. Create a session:    poetry run deploy-remote --create_session --resource_id={remote_app.resource_name}")
        print(f"   2. Send messages:       poetry run deploy-remote --send --resource_id={remote_app.resource_name} --session_id=<id> --message='Your message'")
        print(f"   3. Clean up when done:  poetry run deploy-remote --delete --resource_id={remote_app.resource_name}")
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        raise


def delete_deployment(resource_id: str):
    """Delete the deployed agent"""
    print(f"\n🔄 Deleting deployment: {resource_id}")
    print("⏳ This may take a moment...")
    
    try:
        remote_app = agent_engines.get(resource_id)
        remote_app.delete(force=True)
        print(f"✅ Deployment deleted successfully!")
    except Exception as e:
        print(f"❌ Error deleting deployment: {e}")
        raise


def list_deployments():
    """List all deployments"""
    print("\n🔄 Fetching deployments...")
    
    try:
        deployments_iter = agent_engines.list()
        deployments = list(deployments_iter)
        if len(deployments) == 0:
            print("📭 No deployments found")
            print("\n💡 Create a deployment with:")
            print("   poetry run deploy-remote --create")
            return
        
        print(f"✅ Found {len(deployments)} deployment(s):")
        for deployment in deployments:
            print(f"  📋 {deployment.resource_name}")
    except Exception as e:
        print(f"❌ Error listing deployments: {e}")


def create_session(resource_id: str, user_id: str):
    """Create a new session for the deployed agent"""
    print(f"\n🔄 Creating session on deployment: {resource_id}")
    print(f"👤 User ID: {user_id}")
    
    try:
        remote_app = agent_engines.get(resource_id)
        remote_session = remote_app.create_session(user_id=user_id)
        
        print(f"✅ Session created successfully!")
        print(f"  📋 Session ID: {remote_session.get('id', remote_session)}")
        if 'user_id' in remote_session:
            print(f"  👤 User ID: {remote_session['user_id']}")
        if 'app_name' in remote_session:
            print(f"  📱 App name: {remote_session['app_name']}")
        if 'last_update_time' in remote_session:
            print(f"  🕐 Last update: {remote_session['last_update_time']}")
        print(f"\n💡 Send a message with:")
        print(f"   poetry run deploy-remote --send --resource_id={resource_id} --session_id={remote_session['id']} --user_id={user_id} --message='Your message'")
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        raise


def list_sessions(resource_id: str, user_id: str):
    """List all sessions for a deployment"""
    print(f"\n🔄 Fetching sessions for deployment: {resource_id}")
    print(f"👤 User ID: {user_id}")
    
    try:
        remote_app = agent_engines.get(resource_id)
        sessions = remote_app.list_sessions(user_id=user_id)
        
        if not sessions:
            print("📭 No active sessions found")
            print("\n💡 Create a new session with:")
            print(f"   poetry run deploy-remote --create_session --resource_id={resource_id} --user_id={user_id}")
            return
        
        print(f"✅ Found {len(sessions)} session(s):")
        for session in sessions:
            print(f"  📋 Session ID: {session['id']}")
    except Exception as e:
        print(f"❌ Error fetching sessions: {e}")


def get_session(resource_id: str, user_id: str, session_id: str):
    """Get details of a specific session"""
    print(f"\n🔄 Fetching session: {session_id}")
    
    try:
        remote_app = agent_engines.get(resource_id)
        session = remote_app.get_session(user_id=user_id, session_id=session_id)
        
        print(f"✅ Session found!")
        print(f"  📋 Session ID: {session['id']}")
        print(f"  👤 User ID: {session['user_id']}")
        print(f"  📱 App name: {session['app_name']}")
        print(f"  🕐 Last update: {session.get('last_update_time', 'N/A')}")
    except Exception as e:
        print(f"❌ Error fetching session: {e}")


def send_message(resource_id: str, user_id: str, session_id: str, message: str):
    """Send a message to a session on the deployed agent"""
    print(f"\n📤 Sending message to session: {session_id}")
    print(f"💬 Message: {message}\n")
    
    try:
        remote_app = agent_engines.get(resource_id)
        
        print("🤖 Agent response:\n")
        print("-" * 80)
        any_output = False

        for event in remote_app.stream_query(
            user_id=user_id,
            session_id=session_id,
            message=message,
        ):
            any_output = True
            # Pretty-print common event structures
            try:
                if isinstance(event, dict):
                    content = event.get("content")
                    # Text parts from model
                    if content and isinstance(content, dict):
                        parts = content.get("parts", [])
                        for part in parts:
                            # Text output
                            if isinstance(part, dict) and "text" in part:
                                print(part["text"])  # print text directly
                            # Tool function call (debug)
                            if isinstance(part, dict) and "function_call" in part:
                                fc = part["function_call"]
                                name = fc.get("name")
                                args = fc.get("args")
                                print(f"\n[tool call] {name}({args})")
                            # Tool function response
                            if isinstance(part, dict) and "function_response" in part:
                                fr = part["function_response"]
                                name = fr.get("name")
                                resp = fr.get("response")
                                print(f"\n[tool result] {name}: {resp}")
                    # Fallback: if no structured content, dump minimal
                    else:
                        print(event)
                else:
                    print(event)
            except Exception as pe:
                # If pretty printing fails, print raw
                print(event)
        
        print("\n" + "-" * 80)
        if any_output:
            print("✅ Message sent successfully!")
        else:
            print("⚠️  No output received from agent. Check resource_id, session_id, and logs.")
    except Exception as e:
        print(f"❌ Error sending message: {e}")


def main(argv=None):
    """Main function that can be called directly or through app.run()"""
    # Parse flags first
    if argv is None:
        argv = flags.FLAGS(sys.argv)
    else:
        argv = flags.FLAGS(argv)
    
    load_dotenv()
    
    # Print header
    print("\n" + "=" * 80)
    print("🚀 Content Orchestration Agent - Vertex AI Deployment")
    print("=" * 80)
    
    # Get configuration from flags or environment variables
    project_id = (
        FLAGS.project_id if FLAGS.project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    location = FLAGS.location if FLAGS.location else os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket = FLAGS.bucket if FLAGS.bucket else os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")
    user_id = FLAGS.user_id
    
    # Validate required configuration
    if not project_id:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        print("   Set it in .env or pass --project_id=<id>")
        return
    elif not location:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        print("   Set it in .env or pass --location=<location>")
        return
    elif not bucket:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_STAGING_BUCKET")
        print("   Set it in .env or pass --bucket=gs://<bucket-name>")
        return
    
    # Initialize Vertex AI
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=bucket,
    )
    
    # Handle commands
    if FLAGS.create:
        create_deployment()
    
    elif FLAGS.delete:
        if not FLAGS.resource_id:
            print("❌ Error: --resource_id is required for --delete")
            return
        delete_deployment(FLAGS.resource_id)
    
    elif FLAGS.list:
        list_deployments()
    
    elif FLAGS.create_session:
        if not FLAGS.resource_id:
            print("❌ Error: --resource_id is required for --create_session")
            return
        create_session(FLAGS.resource_id, user_id)
    
    elif FLAGS.list_sessions:
        if not FLAGS.resource_id:
            print("❌ Error: --resource_id is required for --list_sessions")
            return
        list_sessions(FLAGS.resource_id, user_id)
    
    elif FLAGS.get_session:
        if not FLAGS.resource_id:
            print("❌ Error: --resource_id is required for --get_session")
            return
        if not FLAGS.session_id:
            print("❌ Error: --session_id is required for --get_session")
            return
        get_session(FLAGS.resource_id, user_id, FLAGS.session_id)
    
    elif FLAGS.send:
        if not FLAGS.resource_id:
            print("❌ Error: --resource_id is required for --send")
            return
        if not FLAGS.session_id:
            print("❌ Error: --session_id is required for --send")
            return
        send_message(FLAGS.resource_id, user_id, FLAGS.session_id, FLAGS.message)
    
    else:
        print("\n💡 Quick Start Examples:")
        print("   1. Deploy agent:        poetry run deploy-remote --create")
        print("   2. List deployments:    poetry run deploy-remote --list")
        print("   3. Create session:      poetry run deploy-remote --create_session --resource_id=<id>")
        print("   4. List sessions:       poetry run deploy-remote --list_sessions --resource_id=<id>")
        print("   5. Send message:        poetry run deploy-remote --send --resource_id=<id> --session_id=<sid> --message='Create content about AI'")
        print("   6. Delete deployment:   poetry run deploy-remote --delete --resource_id=<id>")
        print("\n💡 Optional flags:")
        print("   --user_id=<id>         User ID for sessions (default: default_user)")
        print("   --project_id=<id>      Override GOOGLE_CLOUD_PROJECT")
        print("   --location=<loc>       Override GOOGLE_CLOUD_LOCATION")
        print("   --bucket=<gs://...>    Override GOOGLE_CLOUD_STAGING_BUCKET")


if __name__ == "__main__":
    app.run(main)

