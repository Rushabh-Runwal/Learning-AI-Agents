#!/usr/bin/env python3
"""
Test script for the deployed Agent Engine.
"""

from vertexai import agent_engines
import os
from dotenv import load_dotenv

load_dotenv()

USER_ID = "test_user_123"

# Get the deployed agent engine
REMOTE_APP = agent_engines.get(os.getenv("AGENT_ENGINE_RESOURCE_NAME"))

# Create a session
session = REMOTE_APP.create_session(user_id=USER_ID)
session_id = session["id"]
print(f"✅ Created session: {session_id}")

# Test query
message = "List available burger menu please"
print(f"\n📤 Sending message: {message}\n")

# Stream query and print responses
for event in REMOTE_APP.stream_query(
    user_id=USER_ID,
    session_id=session_id,
    message=message,
):
    parts = event.get("content", {}).get("parts", [])
    if parts:
        for part in parts:
            if part.get("function_call"):
                print(f"🛠️  Tool Call: {part.get('function_call').get('name')}")
                print(f"   Args: {part.get('function_call').get('args')}")
            elif part.get("function_response"):
                print(f"⚡ Tool Response: {part.get('function_response')}")
            elif part.get("text"):
                print(f"💬 Agent: {part.get('text')}")

print("\n✅ Test completed successfully!")
