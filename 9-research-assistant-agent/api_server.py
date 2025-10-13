"""
Research Assistant Agent API Server
FastAPI server for the Research Assistant Agent
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from research_assistant.adk_agent import root_agent
from research_assistant.config import GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION

# FastAPI app
app = FastAPI(title="Research Assistant Agent API", version="1.0.0")

# Request models
class ResearchRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"
    session_id: Optional[str] = None
    resource_id: Optional[str] = None  # For remote deployment

class SessionCreateRequest(BaseModel):
    user_id: Optional[str] = "default_user"
    resource_id: Optional[str] = None  # For remote deployment

# Local AdkApp singleton
_LOCAL_APP = None

def get_local_app():
    global _LOCAL_APP
    if _LOCAL_APP is None:
        # Initialize Vertex AI for local testing if not already
        if GOOGLE_CLOUD_PROJECT:
            vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
        _LOCAL_APP = reasoning_engines.AdkApp(agent=root_agent, enable_tracing=True)
    return _LOCAL_APP

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    """Serve the web UI."""
    return HTMLResponse(content=open("frontend/index.html").read())

@app.post("/research")
async def conduct_research(request: ResearchRequest):
    """Conduct research using the research assistant."""
    try:
        if request.resource_id:
            # Remote (Agent Engine) session
            vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
            remote_app = agent_engines.get(request.resource_id)

            response_text = ""
            traces = []
            async for event in remote_app.stream_query(
                user_id=request.user_id or "default_user",
                session_id=request.session_id,
                message=request.query,
            ):
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
                "resource_id": request.resource_id,
                "session_id": request.session_id,
                "response": response_text,
                "traces": traces,
            }
        else:
            # Local (AdkApp) session
            app = get_local_app()
            response_text = ""
            traces = []
            
            for event in app.stream_query(
                user_id=request.user_id or "default_user",
                session_id=request.session_id,
                message=request.query,
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
                "session_id": request.session_id,
                "response": response_text.strip(),
                "traces": traces,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conducting research: {str(e)}")

@app.post("/session/create")
async def create_session_endpoint(request: SessionCreateRequest):
    """Create a new session for the agent."""
    try:
        if request.resource_id:
            # Initialize Vertex AI and create a remote session
            vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)
            remote_app = agent_engines.get(request.resource_id)
            remote_session = remote_app.create_session(user_id=request.user_id or "default_user")
            return {
                "mode": "remote",
                "resource_id": request.resource_id,
                "session_id": remote_session.get("id", remote_session),
                "user_id": request.user_id or "default_user",
            }
        else:
            # Local session via AdkApp
            app = get_local_app()
            session = app.create_session(user_id=request.user_id or "default_user")
            return {
                "mode": "local",
                "session_id": getattr(session, "id", session),
                "user_id": request.user_id or "default_user",
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

if __name__ == "__main__":
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    print(f"🔬 Starting Research Assistant Agent API Server")
    print(f"📍 Server running at: http://{HOST}:{PORT}")
    print(f"📖 API Documentation: http://{HOST}:{PORT}/docs")
    print(f"💡 Web UI: http://{HOST}:{PORT}")
    
    uvicorn.run(
        "api_server:app",
        host=HOST,
        port=PORT,
        reload=False
    )
