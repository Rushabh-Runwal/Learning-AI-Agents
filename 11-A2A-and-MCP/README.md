# Day 11: Understanding A2A and MCP Protocols

Building interoperable AI agents using Agent-to-Agent (A2A) and Model Context Protocol (MCP).

## Overview

This project demonstrates two foundational protocols for modern AI agent systems through a practical currency conversion agent. The implementation shows how A2A enables standardized agent communication while MCP provides access to external tools and data.

## What Are These Protocols?

### Agent-to-Agent (A2A) Protocol
A standardized protocol for agent-to-agent communication that enables:
- Unified message format for agent interactions
- Task state management (working, input-required, complete)
- Multi-turn conversation support
- Context preservation across interactions
- Agent discovery through structured cards

### Model Context Protocol (MCP)
A protocol for connecting AI systems to external tools and data:
- Client-server architecture for tool execution
- Standardized tool registration and invocation
- Integration with LLM systems
- Real-time data access without retraining

## Architecture

The currency agent demonstrates both protocols working together:

1. **MCP Server**: Provides exchange rate tool via FastMCP
2. **A2A Agent**: Exposes currency conversion capabilities via A2A protocol
3. **ADK Integration**: Uses Google's Agent Development Kit for agent orchestration

## Key Features

- Real-time currency exchange rate queries
- Support for 30+ currencies via Frankfurter API
- Multi-turn conversations with context
- Structured task state management
- Both single-turn and conversational patterns
- A2A-compliant agent card for discovery

## Video Tutorial

Watch the complete walkthrough:
[Understanding A2A and MCP Protocols](https://youtube.com/shorts/FrmSNtDcBus)

## Setup

1. **Prerequisites**:
   - Python 3.10 or higher
   - uv package manager
   - Google Cloud account (for ADK)

2. **Install dependencies**:
   ```bash
   cd currency-agent
   uv sync
   ```

3. **Configure environment**:
   Create a `.env` file:
   ```bash
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   MCP_SERVER_URL=http://localhost:8081/mcp
   PORT=8081
   ```

4. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth application-default login
   ```

## Running the Project

### Start the MCP Server

```bash
uv run python mcp-server/server.py
```

The server will start on http://0.0.0.0:8081/mcp

### Test the MCP Server

```bash
uv run python mcp-server/test_server.py
```

### Run the A2A Agent

```bash
uv run adk web currency_agent
```

Access the web UI at http://localhost:8000

### Test the A2A Client

```bash
uv run python currency_agent/test_client.py
```

## Project Structure

```
11-A2A-and-MCP/
├── currency-agent/
│   ├── currency_agent/
│   │   ├── agent.py              # A2A agent with MCP integration
│   │   └── test_client.py        # A2A client example
│   ├── mcp-server/
│   │   ├── server.py             # MCP server implementation
│   │   └── test_server.py        # MCP client test
│   ├── .env                      # Environment configuration
│   ├── pyproject.toml            # Project dependencies
│   └── README.md
└── README.md
```

## Example Usage

### Single-turn Query

```python
# A2A client request
{
  "text": "How much is 100 USD in EUR?"
}

# Response with exchange rate and task completion
```

### Multi-turn Conversation

```python
# First turn
"What's the exchange rate for USD to EUR?"

# Follow-up
"How about 500 USD?"
```

## Technologies Used

- **A2A SDK**: Agent-to-agent communication
- **FastMCP**: MCP server framework
- **Google ADK**: Agent Development Kit
- **Python asyncio**: Asynchronous operations
- **Frankfurter API**: Exchange rate data
- **Python 3.13**: Latest Python features

## Learning Resources

- [A2A Protocol Documentation](https://a2a-protocol.org/latest/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://gofastmcp.com/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)

## Key Concepts Demonstrated

1. **Protocol Integration**: Combining A2A and MCP for complete agent functionality
2. **Task State Management**: Tracking conversation progress with A2A states
3. **Tool Invocation**: Using MCP for external API calls
4. **Context Preservation**: Maintaining conversation history across turns
5. **Error Handling**: Graceful handling of API failures and invalid inputs

## Part of Series

This is Day 11 of the 31 Days, 31 AI Agents series, exploring different AI agent architectures and protocols.

**Previous Days:**
- Day 10: Multi-Agent Systems with Google ADK
- Day 9: Travel Itinerary Agent
- [See full series](https://github.com/Rushabh-Runwal/Learning-AI-Agents)
