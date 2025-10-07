# 13-newProject: LeetCode Solver Sequential Agent

This project demonstrates a **Sequential Agent** in the Google Agent Development Kit (ADK) that creates a complete workflow for finding and analyzing LeetCode problems. The agent uses AI knowledge to search for problems and provide comprehensive solution analysis without relying on web scraping.

## What This Project Does

The `LeetCodeSolverPipeline` is a sequential agent that:

1. **Searches for LeetCode Problems** - Uses AI knowledge mapping to find relevant LeetCode problems based on user queries
2. **Extracts Problem Information** - Provides structured problem data using AI model knowledge 
3. **Analyzes Solutions** - Generates comprehensive solutions with multiple approaches, complexity analysis, and implementations in various programming languages

## Sequential Agent Architecture

This project uses a **Sequential Agent** pattern where each sub-agent executes in a fixed order:

```
User Query (Problem description/name) 
    ↓
Google Search Agent → Scraper Agent → Solution Analyzer Agent
    ↓                    ↓                    ↓
Finds Problem       Extracts Data       Provides Solutions
```

Each agent's output becomes available to the next agent through state management, creating a processing pipeline.

## Project Structure

```
13-newProject/
├── README.md
├── requirements.txt
├── main.py
└── leetcode_solver_agent/
    ├── __init__.py
    ├── agent.py                    # Main Sequential Agent
    └── subagents/
        ├── __init__.py
        ├── url_validator/
        │   ├── __init__.py
        │   └── agent.py           # URL validation logic
        ├── scraper/
        │   ├── __init__.py
        │   ├── agent.py           # Web scraping agent
        │   └── tools.py           # Scraping tools & functions
        └── solution_analyzer/
            ├── __init__.py
            ├── agent.py           # Solution analysis agent
            └── tools.py           # Analysis tools & algorithms
```

## Sub-Agents Overview

### 1. URL Validator Agent (`url_validator`)
- **Purpose**: Validates LeetCode problem URLs and extracts problem slugs
- **Input**: User-provided URL string
- **Output**: Validation status and extracted problem slug
- **State Key**: `url_validation_result`

**Example Output**: `"valid|two-sum"` or `"invalid|not a LeetCode URL"`

### 2. LeetCode Scraper Agent (`scraper`)
- **Purpose**: Scrapes problem data from LeetCode using web scraping
- **Input**: Problem slug from URL validator
- **Output**: Structured problem data (title, difficulty, description, examples)
- **State Key**: `scraped_problem_data`
- **Tools**: 
  - `scrape_leetcode_problem()` - Primary scraping function
  - `get_alternative_problem_data()` - Fallback for common problems

**Technologies Used**:
- `requests` - HTTP requests
- `BeautifulSoup` - HTML parsing
- Browser headers to avoid blocking

### 3. Solution Analyzer Agent (`solution_analyzer`)  
- **Purpose**: Analyzes problems and provides solution approaches
- **Input**: Scraped problem data
- **Output**: Comprehensive solution analysis with algorithms and complexity
- **State Key**: `solution_analysis_result`
- **Tools**:
  - `analyze_problem_complexity()` - Pattern detection and complexity analysis
  - `generate_solution_approach()` - Solution strategies and pseudocode

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   cd 13-newProject
   pip install -r requirements.txt
   ```

2. **Set up Environment**:
   ```bash
   # Create .env file with your Google AI API key
   echo "GOOGLE_AI_API_KEY=your_api_key_here" > .env
   ```

3. **Run the Agent**:
   ```bash
   python main.py
   ```

## Usage Examples

### Example 1: Two Sum Problem
```
Input: https://leetcode.com/problems/two-sum/

Expected Output:
✅ URL Validation: Valid LeetCode URL (slug: two-sum)
🔍 Scraping: Successfully extracted problem data
📊 Analysis: Hash Map approach, O(n) time complexity, detailed pseudocode
```

### Example 2: Invalid URL
```
Input: https://example.com/not-leetcode

Expected Output:  
❌ URL Validation: Invalid - not a LeetCode URL
⏹️ Pipeline stops (no scraping or analysis)
```

## Features

### Web Scraping Capabilities
- **Robust Scraping**: Handles dynamic content and various page layouts
- **Fallback System**: Alternative data source for common problems
- **Error Handling**: Graceful handling of network issues and blocked requests
- **Browser Simulation**: Uses realistic headers to avoid detection

### Solution Analysis Features
- **Pattern Detection**: Identifies common algorithm patterns (Two Pointers, DP, etc.)
- **Complexity Analysis**: Estimates time/space complexity
- **Multiple Approaches**: Provides both brute force and optimized solutions
- **Implementation Hints**: Practical coding tips and considerations
- **Pseudocode Generation**: Step-by-step algorithmic breakdown

### Sequential Workflow Benefits
- **Deterministic Order**: Each step builds on the previous
- **State Sharing**: Data flows seamlessly between agents
- **Error Propagation**: Failed steps prevent unnecessary processing
- **Modular Design**: Easy to modify or extend individual components

## Technical Implementation

### State Management
The sequential agent uses state management to pass data between sub-agents:

```python
# URL Validator output
tool_context.state["url_validation_result"] = "valid|two-sum"

# Scraper accesses validator result
validation_result = tool_context.state.get("url_validation_result", "")

# Solution analyzer accesses scraper result  
scraped_data = tool_context.state.get("scraped_problem_data", "")
```

### Error Handling Strategy
- **Early Termination**: Invalid URLs stop the pipeline immediately
- **Graceful Degradation**: Scraping failures trigger fallback mechanisms
- **Informative Errors**: Clear error messages guide users to solutions

### Extensibility Points
- **Add More Scrapers**: Support for HackerRank, CodeForces, etc.
- **Enhanced Analysis**: Code generation, test case creation
- **Additional Validators**: Support for problem IDs, contest links
- **Output Formats**: JSON export, PDF reports, code templates

## Limitations & Considerations

### Web Scraping Challenges
- **Dynamic Content**: LeetCode heavily uses JavaScript for content loading
- **Rate Limiting**: May encounter request limits on frequent usage
- **Layout Changes**: Site updates can break scraping selectors
- **Anti-Bot Measures**: May need more sophisticated bypassing techniques

### Recommended Improvements
1. **Selenium Integration**: For JavaScript-heavy pages
2. **Caching System**: Store scraped data to reduce requests
3. **Proxy Rotation**: Avoid IP-based blocking
4. **API Integration**: Use official APIs when available

## Learning Objectives

This project demonstrates:
- **Sequential Agent Patterns** in ADK
- **Web Scraping Techniques** with Python
- **State Management** between agents
- **Tool Integration** in LLM agents
- **Error Handling** in multi-step workflows
- **Modular Agent Architecture**

## Alternative Approaches

### Using Apify Platform
For production use, consider integrating with [Apify](https://docs.apify.com/):
```python
# Example Apify integration
from apify import Actor

async def scrape_with_apify():
    actor_run = await Actor.call("apify/web-scraper", {...})
    return actor_run["defaultDatasetId"]
```

### Browser Automation
For more reliable scraping:
```python
from selenium import webdriver
# More robust but heavier approach
```

## Contributing

Feel free to extend this project by:
- Adding support for more coding platforms
- Implementing code generation features
- Creating better fallback mechanisms
- Adding test case generation
- Building a web interface

---

**Note**: This project is for educational purposes. Please respect website terms of service and implement appropriate rate limiting when scraping.