"""
FastAPI server for Content Orchestration Agent
Provides REST API and web UI for the ADK agent
"""

import os
import asyncio
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from content_orchestration import root_agent
from content_orchestration.config import GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION

# Vertex AI Agent Engine SDK
import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

# Local AdkApp singleton
_LOCAL_APP = None


def get_local_app():
    global _LOCAL_APP
    if _LOCAL_APP is None:
        # Initialize Vertex AI if project info is available (optional for local)
        if GOOGLE_CLOUD_PROJECT:
            vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        _LOCAL_APP = reasoning_engines.AdkApp(agent=root_agent, enable_tracing=True)
    return _LOCAL_APP

# Configuration
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

# Create FastAPI app
app = FastAPI(
    title="Content Orchestration Agent API",
    description="API for generating educational content using Google ADK",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ContentRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"


class SessionCreateRequest(BaseModel):
    resource_id: Optional[str] = None  # If provided, create session on Agent Engine
    user_id: Optional[str] = "default_user"


class SendRequest(BaseModel):
    message: str
    session_id: str
    resource_id: Optional[str] = None  # If provided, send to Agent Engine
    user_id: Optional[str] = "default_user"


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web UI"""
    try:
        with open("frontend/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Content Orchestration Agent API</h1><p>Visit /docs for API documentation</p>"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "content-orchestration-agent",
        "version": "1.0.0"
    }


@app.get("/capabilities")
async def get_capabilities():
    """Get agent capabilities"""
    return {
        "agent_name": "Content Orchestration Agent",
        "description": "Generates educational content including reading materials, quizzes, videos, and games",
        "capabilities": [
            "Generate reading materials",
            "Create quizzes",
            "Write video scripts",
            "Design educational games"
        ]
    }


@app.post("/generate")
async def generate_content(request: ContentRequest):
    """
    Generate content using the ADK agent
    
    Args:
        request: ContentRequest with query and optional user_id
        
    Returns:
        Generated content response
    """
    try:
        # Call the agent
        response_text = ""
        async for event in root_agent.run(request.query):
            # Extract text from the event
            if hasattr(event, 'content'):
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
            elif isinstance(event, dict):
                if 'content' in event and 'parts' in event['content']:
                    for part in event['content']['parts']:
                        if 'text' in part:
                            response_text += part['text']
        
        return {
            "response": response_text,
            "user_id": request.user_id,
            "query": request.query
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")


@app.post("/session/create")
async def create_session(req: SessionCreateRequest):
    """Create a session either locally or on Agent Engine if resource_id is provided."""
    try:
        if req.resource_id:
            # Initialize Vertex AI and create a remote session
            vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
            remote_app = agent_engines.get(req.resource_id)
            remote_session = remote_app.create_session(user_id=req.user_id or "default_user")
            return {
                "mode": "remote",
                "resource_id": req.resource_id,
                "session_id": remote_session.get("id", remote_session),
                "user_id": req.user_id or "default_user",
            }
        else:
            # Local session via AdkApp
            app = get_local_app()
            session = app.create_session(user_id=req.user_id or "default_user")
            return {
                "mode": "local",
                "session_id": getattr(session, "id", session),
                "user_id": req.user_id or "default_user",
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")


@app.post("/send")
async def send_message(req: SendRequest):
    """Send a message to an existing session (local or remote)."""
    try:
        # Remote (Agent Engine)
        if req.resource_id:
            vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
            remote_app = agent_engines.get(req.resource_id)

            response_text = ""
            traces = []
            async for event in remote_app.stream_query(
                user_id=req.user_id or "default_user",
                session_id=req.session_id,
                message=req.message,
            ):
                # Debug: print event structure
                print(f"DEBUG REMOTE: Event type: {type(event)}")
                print(f"DEBUG REMOTE: Event content: {event}")
                
                if isinstance(event, dict) and "content" in event and isinstance(event["content"], dict):
                    for part in event["content"].get("parts", []):
                        if isinstance(part, dict):
                            if "text" in part and part["text"]:
                                response_text += part["text"]
                            elif "function_call" in part:
                                traces.append({
                                    "type": "tool_call",
                                    "name": part["function_call"].get("name", "unknown"),
                                    "args": part["function_call"].get("args", {}),
                                    "timestamp": event.get("timestamp", "")
                                })
                            elif "function_response" in part:
                                # Extract the actual content from tool response
                                tool_response = part["function_response"].get("response", "")
                                if isinstance(tool_response, dict) and 'result' in tool_response:
                                    # If response has a 'result' field, use that as the main response
                                    response_text += tool_response['result']
                                
                                traces.append({
                                    "type": "tool_response",
                                    "name": part["function_response"].get("name", "unknown"),
                                    "response": tool_response,
                                    "timestamp": event.get("timestamp", "")
                                })
            return {
                "mode": "remote",
                "resource_id": req.resource_id,
                "session_id": req.session_id,
                "response": response_text,
                "traces": traces,
            }

        # Local (AdkApp) session
        app = get_local_app()
        response_text = ""
        traces = []
        
        for event in app.stream_query(
            user_id=req.user_id or "default_user",
            session_id=req.session_id,
            message=req.message,
        ):
            # Handle different event structures from AdkApp
            if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                # Vertex AI event structure
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text += part.text
                    elif hasattr(part, 'function_call'):
                        traces.append({
                            "type": "tool_call",
                            "name": part.function_call.name,
                            "args": part.function_call.args,
                            "timestamp": getattr(event, 'timestamp', '')
                        })
                    elif hasattr(part, 'function_response'):
                        # Extract the actual content from tool response
                        tool_response = part.function_response.response
                        if isinstance(tool_response, dict) and 'result' in tool_response:
                            # If response has a 'result' field, use that as the main response
                            response_text += tool_response['result']
                        
                        traces.append({
                            "type": "tool_response",
                            "name": part.function_response.name,
                            "response": tool_response,
                            "timestamp": getattr(event, 'timestamp', '')
                        })
            elif isinstance(event, dict):
                # Dictionary event structure
                if "content" in event and isinstance(event["content"], dict):
                    for part in event["content"].get("parts", []):
                        if isinstance(part, dict):
                            if "text" in part and part["text"]:
                                response_text += part["text"]
                            elif "function_call" in part:
                                traces.append({
                                    "type": "tool_call",
                                    "name": part["function_call"].get("name", "unknown"),
                                    "args": part["function_call"].get("args", {}),
                                    "timestamp": event.get("timestamp", "")
                                })
                            elif "function_response" in part:
                                # Extract the actual content from tool response
                                tool_response = part["function_response"].get("response", "")
                                if isinstance(tool_response, dict) and 'result' in tool_response:
                                    # If response has a 'result' field, use that as the main response
                                    response_text += tool_response['result']
                                
                                traces.append({
                                    "type": "tool_response",
                                    "name": part["function_response"].get("name", "unknown"),
                                    "response": tool_response,
                                    "timestamp": event.get("timestamp", "")
                                })
            else:
                # Fallback for other event types
                if hasattr(event, 'text'):
                    response_text += str(event.text)
                elif isinstance(event, str):
                    response_text += event
        
        return {
            "mode": "local",
            "session_id": req.session_id,
            "response": response_text.strip(),
            "traces": traces,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")


if __name__ == "__main__":
    print(f"🚀 Starting Content Orchestration Agent API Server")
    print(f"📍 Server running at: http://{HOST}:{PORT}")
    print(f"📖 API Documentation: http://{HOST}:{PORT}/docs")
    print(f"💡 Web UI: http://{HOST}:{PORT}")
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info"
    )

