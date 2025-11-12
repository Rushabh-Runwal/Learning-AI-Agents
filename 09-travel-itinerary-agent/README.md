# Project 9: Travel Itinerary Planner - Multi-Agent System

A production-ready multi-agent system built with **Google ADK** and **Apify APIs** that demonstrates enterprise-grade AI agent orchestration. This project teaches three critical concepts for building real-world AI systems:

1. **Choosing the Right LLM** - Strategic model selection based on task complexity and cost optimization
2. **Defining Agent Control Logic** - Tool integration, routing, and multi-agent coordination
3. **Defining Core Instructions & Features** - Specialized agent roles with clear responsibilities

## 🏗️ Architecture

### Multi-Agent System Design

```
┌─────────────────────────────────────┐
│        Orchestrator Agent           │
│     (gemini-2.5-pro)               │
│  Complex reasoning & coordination   │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│Research │ │ Budget  │ │Synthesizer│
│(flash-  │ │(flash-  │ │(flash-   │
│ lite)   │ │ lite)   │ │ lite)    │
└─────────┘ └─────────┘ └─────────┘
    │         │         │
    ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Flights │ │ Hotels  │ │Activities│
│(flash + │ │(flash + │ │(flash + │
│ tools)  │ │ tools)  │ │ tools)  │
└─────────┘ └─────────┘ └─────────┘
```

### Agent Specialization

| Agent | Model | Purpose | Tools |
|-------|-------|---------|-------|
| **Orchestrator** | `gemini-2.5-pro` | Complex multi-agent coordination | None (delegates) |
| **Destination Research** | `gemini-2.5-flash-lite` | Destination recommendations | None |
| **Budget Planner** | `gemini-2.5-flash-lite` | Budget breakdown | None |
| **Flights Agent** | `gemini-2.5-flash` | Flight search & analysis | Apify Flights API |
| **Hotels Agent** | `gemini-2.5-flash` | Hotel search & analysis | Apify Hotels API |
| **Activities Agent** | `gemini-2.5-flash` | Activity recommendations | Apify Activities API |
| **Synthesizer** | `gemini-2.5-flash-lite` | Itinerary consolidation | None |

## 🧠 Key Concepts Demonstrated

### 1. Choosing the Right LLM

**Model Selection Strategy:**
- **Gemini 2.5 Pro**: For complex orchestration requiring advanced reasoning
- **Gemini 2.5 Flash**: For agentic tasks with tool usage (flights, hotels, activities)
- **Gemini 2.5 Flash-Lite**: For simple text generation tasks (research, budget, synthesis)

**Rationale:**
- Larger models for complex multi-step reasoning and coordination
- Medium models for tool-using agents that need balanced performance
- Smaller models for straightforward text generation to optimize costs

### 2. Defining Agent Control Logic

**Tool Integration:**
```python
# Example: Flights Agent with Apify integration
flights_agent = LlmAgent(
    name="flights_agent",
    model="gemini-2.5-flash",
    tools=[flights_lookup],  # Apify API tool
    instruction="Use flights_lookup to fetch real options..."
)
```

**Agent Coordination:**
```python
# Orchestrator coordinates all sub-agents
orchestrator = LlmAgent(
    name="itinerary_orchestrator",
    model="gemini-2.5-pro",
    sub_agents=[destination_research_agent, budget_planner_agent, ...]
)
```

### 3. Defining Core Instructions & Features

**Specialized Agent Instructions:**
- Each agent has specific, focused instructions
- Clear input/output expectations
- Tool usage guidance where applicable

**Feature Capabilities:**
- Real-time data via Apify APIs
- Multi-agent coordination
- Cost-optimized model selection
- Comprehensive travel planning

## 🚀 Setup & Usage

### Prerequisites

1. **Google API Key**: Get your free API key from [Google AI Studio](https://aistudio.google.com/)
2. **Apify API Token**: Sign up at [Apify Console](https://console.apify.com/) and get your token from Account Settings → Integrations → API Token

### Installation

```bash
# Navigate to project directory
cd 9-travel-itinerary-agent

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies included:**
- `google-adk>=1.16.0` - Google Agent Development Kit
- `google-genai>=1.41.0` - Google Gemini AI library
- `google-cloud-aiplatform>=1.112.0` - Vertex AI platform
- `apify-client>=1.8.0` - Apify API client
- `python-dotenv>=1.0.0` - Environment variable management
- `pydantic>=2.0.0` - Data validation
- `requests>=2.32.0` - HTTP requests

### Configuration

Set your API credentials as environment variables:

```bash
# Option 1: Export in your shell
export GOOGLE_API_KEY="your-google-api-key-here"
export APIFY_API_TOKEN="your-apify-token-here"

# Option 2: Create a .env file (recommended for development)
cat > .env << EOF
GOOGLE_API_KEY=your-google-api-key-here
APIFY_API_TOKEN=your-apify-token-here
EOF
```

**Note**: The Apify token is pre-configured in the code with a fallback, but it's recommended to set your own token via environment variable for production use.

### Running the System

**Interactive Mode (Requires valid API keys)**
```bash
# Set environment variables
export GOOGLE_API_KEY="your-google-api-key"
export APIFY_API_TOKEN="your-apify-token"

# Run the interactive system
python main.py
```

**Note**: The system uses Google ADK with proper session management and async processing. Make sure you have valid API keys set up before running.

### Example Usage

```
🌍 Travel Itinerary Planner - Multi-Agent System
============================================================
✅ Environment configured

This multi-agent system coordinates specialized agents:
  📍 Destination Research (Gemini 2.5 Flash-Lite)
  💰 Budget Planning (Gemini 2.5 Flash-Lite)
  ✈️  Flights Agent (Gemini 2.5 Flash + Apify)
  🏨 Hotels Agent (Gemini 2.5 Flash + Apify)
  🎭 Activities Agent (Gemini 2.5 Flash + Apify)
  📝 Itinerary Synthesizer (Gemini 2.5 Flash-Lite)
  🎯 Root Agent (Gemini 2.5 Pro)
============================================================
Created new session: e24d4f69-9219-49ef-b8cb-35dec9e4b8cd

Welcome to the Travel Itinerary Planner!
Tell me about your travel preferences (destination, dates, budget, interests)
Type 'exit' or 'quit' to stop.

You: I want to visit Tokyo in April 2026 for 10 days with a budget of $4000. 
  I'm interested in culture, food, technology, and nature.

🤖 Processing your request...
   The root agent is coordinating with specialized agents...
============================================================

TRAVEL AGENT:
[The multi-agent system would coordinate and provide a comprehensive travel itinerary here]
```

The system will:
1. Research suitable destinations and neighborhoods
2. Plan a realistic budget breakdown
3. Search real flights via Apify
4. Find hotel options via Apify
5. Discover activities and events via Apify
6. Synthesize everything into a coherent itinerary

## 🔧 Technical Implementation

### Apify Integration

The system integrates with three production-grade Apify actors using the official Python client:

#### 1. **Flights Actor** (`23hq58TAuJyQtdGCf`)
- Real-time flight search from Booking.com
- Supports one-way and round-trip searches
- Filters by cabin class, number of passengers, direct flights
- Returns detailed pricing, airlines, routes, and layover info

#### 2. **Hotels Actor** (`pK2iIKVVxERtpwXMy`)
- Hotel search from Expedia, Hotels.com, and variants
- Supports flexible date searches
- Filters by amenities, star rating, price range, traveler type
- Returns detailed property info, pricing, reviews, and availability

#### 3. **Events/Activities Actor** (`PVOL6Qt15hukudGiu`)
- Event search from Ticketmaster
- Supports location-based and date-based filtering
- Categories: concerts, sports, arts, family events
- Returns event details, dates, venues, and ticket info

### Tool Architecture

Using the official Apify Python client for reliability and maintainability:

```python
from apify_client import ApifyClient

def flights_lookup(from_location: str, to_location: str, 
                   departure_date: str, ...) -> dict:
    """Search flights via Apify actor."""
    client = ApifyClient(APIFY_API_TOKEN)
    
    run_input = {
        "tripType": "ONEWAY",
        "fromLocationQuery": from_location,
        "toLocationQuery": to_location,
        "departureDate": departure_date,
        "numberOfAdults": 1,
        "cabinClass": "ECONOMY",
        "sortType": "BEST",
        "maxItems": 10,
    }
    
    # Run actor and wait for completion
    run = client.actor("23hq58TAuJyQtdGCf").call(run_input=run_input)
    
    # Fetch results from dataset
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    
    return {"flights": items, "count": len(items)}
```

**Key Benefits:**
- ✅ Synchronous API calls with automatic waiting
- ✅ Built-in error handling and retries
- ✅ Dataset iteration with pagination support
- ✅ Type-safe actor inputs and outputs

## 📁 Project Structure (ADK Standard)

```
9-travel-itinerary-agent/
├── agent/                       # Main agent directory (ADK standard)
│   ├── __init__.py
│   ├── agent.py                 # Root agent definition (Gemini 2.5 Pro)
│   ├── .env                     # Environment variables
│   ├── sub_agents/              # Specialized sub-agents
│   │   ├── __init__.py
│   │   ├── destination_research.py    # Gemini 2.5 Flash-Lite
│   │   ├── budget_planner.py          # Gemini 2.5 Flash-Lite
│   │   ├── flights_agent.py           # Gemini 2.5 Flash + tools
│   │   ├── hotels_agent.py            # Gemini 2.5 Flash + tools
│   │   ├── activities_agent.py        # Gemini 2.5 Flash + tools
│   │   └── synthesizer.py             # Gemini 2.5 Flash-Lite
│   └── tools/                   # Apify actor integrations
│       ├── __init__.py
│       ├── flights_lookup.py    # Actor: 23hq58TAuJyQtdGCf
│       ├── hotels_lookup.py     # Actor: pK2iIKVVxERtpwXMy
│       └── activities_lookup.py # Actor: PVOL6Qt15hukudGiu
├── main.py                      # CLI entry point (demo mode)
├── requirements.txt             # Dependencies
├── pyproject.toml               # Project metadata (ADK standard)
└── README.md                    # This documentation
```

## 🎯 Learning Outcomes

This project demonstrates:

1. **Strategic Model Selection**: Choosing appropriate LLM sizes based on task complexity
2. **Tool Integration**: Connecting external APIs to agent capabilities
3. **Multi-Agent Coordination**: Orchestrating specialized agents for complex workflows
4. **Cost Optimization**: Balancing performance and cost through model selection
5. **Real-World Application**: Building practical AI systems with external data sources

## 🔗 References

- **Google ADK**: [PyPI Package](https://pypi.org/project/google-adk/) | [Documentation](https://github.com/google/adk-python)
- **Gemini API**: [Model Documentation](https://ai.google.dev/gemini-api/docs/models) | [Pricing](https://ai.google.dev/pricing)
- **Apify Platform**: [Python Client Docs](https://docs.apify.com/api/client/python/) | [Actor Store](https://console.apify.com/actors)
- **Actors Used**:
  - [Flights Actor](https://console.apify.com/actors/23hq58TAuJyQtdGCf) - Booking.com flight scraper
  - [Hotels Actor](https://console.apify.com/actors/pK2iIKVVxERtpwXMy) - Expedia/Hotels.com scraper
  - [Events Actor](https://console.apify.com/actors/PVOL6Qt15hukudGiu) - Ticketmaster event finder

## 🤝 Contributing

This is an educational project demonstrating multi-agent systems. Feel free to:
- Fork and experiment with different agent configurations
- Try different Gemini models and compare performance
- Add new agents (e.g., visa requirements, weather forecasting)
- Integrate additional Apify actors for more data sources

## 📝 License

This project is part of the AI Agent Series learning series.
