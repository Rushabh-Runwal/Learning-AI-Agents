# 🔬 Research Assistant Agent

**Day 9: LLM Selection & Control Logic with Google ADK**

An intelligent research assistant built with **Google Agent Development Kit (ADK)** that strategically uses different Gemini models:
- **Gemini 2.0 Flash** for fast information gathering
- **Gemini 2.0 Pro** for deep analysis and synthesis

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Google API key
export GOOGLE_API_KEY='your-google-api-key'

# Run the assistant
python main.py
```

Get your API key at: https://aistudio.google.com/app/apikey

## 🎯 Sequential Workflow

```
Search Agent (Flash) → Analyzer Agent (Pro) → Synthesizer Agent (Pro)
       ↓                      ↓                        ↓
  Fast Gathering        Deep Analysis        Comprehensive Report
```

## 💡 Usage Examples

### Interactive Mode
```bash
python main.py
```

### Programmatic Use
```python
from research_assistant.agent import create_research_assistant

assistant = create_research_assistant()
results = assistant.conduct_research(
    "What are the latest developments in quantum computing?"
)

print(results["final_report"])
```

### Quick Research
```python
from research_assistant.agent import quick_research

report = quick_research("How does CRISPR work?")
print(report)
```

## 🏗️ Architecture with Google ADK

```
Research Assistant (Main Orchestrator)
├── Search Agent (Gemini Flash)
│   ├── Model: gemini-2.0-flash-exp
│   ├── Tools: web_search, fetch_webpage, search_academic
│   └── Purpose: Fast information gathering
│
├── Analyzer Agent (Gemini Pro)
│   ├── Model: gemini-2.0-flash-thinking-exp-01-21
│   └── Purpose: Deep reasoning and analysis
│
└── Synthesizer Agent (Gemini Pro)
    ├── Model: gemini-2.0-flash-thinking-exp-01-21
    └── Purpose: Comprehensive report generation
```

## 🔧 Google ADK Features Used

### 1. **Function Calling (Tools)**
The Search Agent uses Google ADK's function calling to access search tools:
```python
tools = [{
    "function_declarations": [{
        "name": "web_search",
        "description": "Search the web for information",
        "parameters": {...}
    }]
}]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    tools=tools
)
```

### 2. **System Instructions**
Each agent has specialized system instructions:
```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-thinking-exp-01-21",
    system_instruction="You are a specialized research analyst..."
)
```

### 3. **Chat Sessions**
Search agent uses chat sessions for multi-turn function calling:
```python
chat = model.start_chat(enable_automatic_function_calling=True)
response = chat.send_message(prompt)
```

## 🎨 Key Design Patterns

### 1. **Model Selection Strategy**
- **Fast Model (Flash)** for retrieval and search tasks
  - Lower latency
  - Cost-effective
  - Perfect for tool usage

- **Advanced Model (Pro)** for reasoning tasks
  - Deep thinking capabilities
  - Better analysis quality
  - Superior synthesis

### 2. **Sequential Agent Pattern**
Each stage builds on the previous:
1. **Search** → Gather raw information
2. **Analyze** → Extract insights
3. **Synthesize** → Create comprehensive report

### 3. **Tool-Augmented Generation**
Search agent is augmented with custom tools for real-world data access

## 📁 Project Structure

```
9-research-assistant-agent/
├── main.py                          # CLI interface
├── requirements.txt                 # Google ADK dependencies
├── research_assistant/
│   ├── agent.py                     # Main orchestrator
│   ├── subagents/
│   │   ├── search_agent/
│   │   │   └── agent.py            # Fast search (Flash + Tools)
│   │   ├── analyzer_agent/
│   │   │   └── agent.py            # Deep analysis (Pro)
│   │   └── synthesizer_agent/
│   │       └── agent.py            # Synthesis (Pro)
│   └── tools/
│       └── search_tools.py         # Function declarations
```

## 🎯 Use Cases

- **Academic Research**: Literature reviews and analysis
- **Market Research**: Competitive analysis and trends
- **Technical Investigation**: Deep dives into technical topics
- **Due Diligence**: Comprehensive analysis for decisions
- **Learning**: Understanding complex topics
- **Content Creation**: Research for articles and blogs

## 🔧 Customization

### Add Custom Tools

```python
# In research_assistant/tools/search_tools.py

def custom_tool(param: str) -> dict:
    """Your custom tool implementation."""
    return {"result": "data"}

# Add to TOOL_FUNCTIONS
TOOL_FUNCTIONS["custom_tool"] = custom_tool

# Add declaration to SEARCH_TOOLS
SEARCH_TOOLS[0]["function_declarations"].append({
    "name": "custom_tool",
    "description": "Description",
    "parameters": {...}
})
```

### Modify Agent Behavior

```python
# Change system instructions
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction="Your custom instructions here..."
)
```

## 📚 Google ADK Benefits

1. **Native Integration**: Direct integration with Gemini models
2. **Function Calling**: Built-in support for tool usage
3. **Streaming**: Support for streaming responses
4. **System Instructions**: Clear agent behavior definition
5. **Type Safety**: Structured parameter definitions
6. **Cost Efficiency**: Model selection for optimization

## 💡 Why Google ADK?

- **Official SDK**: Direct from Google
- **Best Performance**: Optimized for Gemini models
- **Latest Features**: Access to newest capabilities
- **Reliability**: Production-ready and maintained
- **Flexibility**: Easy customization and extension

## 🚧 Production Enhancements

To make this production-ready:

1. **Integrate Real Search APIs**
   - Google Custom Search API
   - Serper API
   - Tavily AI

2. **Add Web Scraping**
   - BeautifulSoup for content extraction
   - Playwright for dynamic content

3. **Academic Sources**
   - arXiv API
   - Semantic Scholar
   - PubMed

4. **Caching**
   - Cache search results
   - Avoid redundant API calls

5. **Error Handling**
   - Retry logic
   - Fallback mechanisms
   - Rate limiting

## 📚 Dependencies

```
google-genai>=0.3.0         # Google Agent Development Kit
google-generativeai>=0.8.3  # Gemini models
requests>=2.31.0            # HTTP requests
python-dotenv>=1.0.0        # Environment variables
```

---

**Day 9 of 31 Days of AI Agents** 🚀

*Built with Google Agent Development Kit (ADK)*
