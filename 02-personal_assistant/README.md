# Personal Assistant Agent 🤖

📹 **[Watch Tutorial](https://youtube.com/shorts/B8-KWbuXszc?si=gNyk_ioOiV64vVSi)** 

## What it does

- **Web Search**: Google search capabilities for real-time information
- **Currency Exchange**: Get current foreign exchange rates
- **Wikipedia Lookup**: Access Wikipedia articles and information
- **Hotel Search**: Find and compare hotel options
- **Task Coordination**: Manages multiple tools through a unified interface

## Features

✅ **Multi-Tool Integration**: Combines custom functions, agents, and third-party tools  
✅ **Real-time Data**: Live currency rates and web search results  
✅ **Travel Assistance**: Hotel search and travel-related queries  
✅ **Knowledge Base**: Wikipedia integration for quick facts  
✅ **Extensible Architecture**: Easy to add new tools and capabilities  

## Components

- **Custom Functions**: Foreign exchange rate lookup
- **Sub-Agents**: Specialized Google search and hotel search agents
- **Third-party Tools**: LangChain Wikipedia integration
- **Root Agent**: Central coordinator using Gemini 2.5 Flash

## Tech Stack

- Google Agent Development Kit (ADK)
- LangChain for Wikipedia integration
- Custom API integrations
- Gemini 2.5 Flash AI model

## Setup

1. Install dependencies:
   ```bash
   pip install google-adk langchain wikipedia
   ```

2. Configure API keys for external services

3. Run the assistant:
   ```bash
   python agent.py
   ```

## Usage

Ask the assistant about:
- Current exchange rates
- General knowledge questions
- Web search queries
- Hotel recommendations