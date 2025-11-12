# System Health Agent

A comprehensive system health monitoring agent built with Google's ADK that gathers and analyzes system information using parallel processing.

## Overview

The System Health Agent monitors your system's vital signs by collecting real-time information about:
- **CPU**: Usage, core count, and performance metrics
- **Memory**: RAM usage, availability, and swap information  
- **Disk**: Storage usage and free space analysis

## Architecture

- **Parallel Information Gathering**: CPU, Memory, and Disk agents run simultaneously for efficient data collection
- **AI-Powered Analysis**: Uses Gemini 2.0 Flash model to synthesize data into comprehensive health reports

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Google API key in `.env`:
```bash
GOOGLE_API_KEY=your_api_key_here
```

3. Run the agent:
```bash
adk web
```

## Usage Examples

```
Check my system health
```

```
Provide a comprehensive system report with recommendations
```

```
Is my system running out of memory or disk space?
```

## Key Features

- Real-time system monitoring using `psutil`
- Parallel data collection for improved performance
- AI-powered report synthesis and recommendations
- Independent sub-agent architecture

Part of the AI Agent Series project. 
