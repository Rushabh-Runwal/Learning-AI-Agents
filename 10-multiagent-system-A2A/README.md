# Day 10: Multi-Agent System with Google ADK and A2A Protocol

Building a multi-agent AI system using Google's Agent Development Kit with Agent-to-Agent (A2A) communication protocol.

## Overview

This project demonstrates how to build a sophisticated multi-agent system that coordinates multiple specialized agents to generate and score images based on text descriptions. The system uses sequential and loop patterns to iteratively refine image generation until quality thresholds are met.

## Architecture

The system consists of:

- **Image Generation Prompt Agent**: Creates optimal prompts for image generation
- **Image Generation Agent**: Uses Imagen 3 to generate images
- **Scoring Agent**: Evaluates image quality against defined criteria
- **Checker Agent**: Determines loop termination based on quality scores or iteration limits
- **Loop Agent**: Orchestrates the iterative refinement process

## Key Features

- Sequential agent execution for ordered task processing
- Loop agent pattern for iterative refinement
- A2A protocol for agent-to-agent communication
- Integration with Google's Imagen 3 for image generation
- Configurable quality thresholds and iteration limits

## Technologies Used

- Google Agent Development Kit (ADK)
- Google Generative AI
- Imagen 3
- A2A Protocol
- Python 3.12

## Video Tutorial

Watch the complete walkthrough:
[Day 10: Multi-Agent Systems with Google ADK](https://www.youtube.com/watch?v=iTIcdSiFjaM&list=PL68NYUAEHLCEq-W9FEkCQeM0ZOGWI5dNa)

## Setup

1. Install Python 3.10 or higher
2. Install dependencies:
   ```bash
   cd multiagenthandson
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GCS_BUCKET_NAME=your-bucket-name
   ```

4. Set up Google Cloud authentication:
   ```bash
   gcloud auth application-default login
   ```

## Running the Agent

Start the ADK web server:

```bash
cd multiagenthandson
adk web .
```

Access the web UI at http://localhost:8000

## Project Structure

```
10-multiagent-system-A2A/
├── multiagenthandson/
│   ├── image_scoring/
│   │   ├── agent.py              # Main agent definitions
│   │   ├── checker_agent.py      # Loop termination logic
│   │   ├── config.py             # Configuration
│   │   └── sub_agents/           # Specialized sub-agents
│   │       ├── prompt/           # Prompt generation
│   │       ├── image/            # Image generation
│   │       └── scoring/          # Image scoring
│   └── requirements.txt
└── README.md
```

## Learning Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [A2A Protocol Specification](https://a2a-protocol.org/latest/)
- [Codelabs Tutorial](https://codelabs.developers.google.com/codelabs/create-multi-agents-adk-a2a)

## Part of Series

This is Day 10 of the 31 Days, 31 AI Agents series, exploring different AI agent architectures and patterns.
