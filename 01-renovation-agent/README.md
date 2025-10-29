# Renovation Agent 🏠

📹 **[Watch Tutorial](https://youtube.com/shorts/5DEWZtV1N4o?si=P2rrU3Dx1T6Dls-A)** 

A Google Cloud-based AI agent that helps with home renovation planning and proposal generation.

## What it does

- **Renovation Planning**: Analyzes renovation requirements and provides detailed plans
- **Cost Estimation**: Calculates renovation costs based on project scope and materials
- **Proposal Generation**: Creates professional PDF proposals for renovation projects
- **Cloud Integration**: Leverages Google Cloud Storage for document management

## Features

✅ **Smart Planning**: AI-powered renovation recommendations  
✅ **Cost Analysis**: Detailed breakdown of renovation expenses  
✅ **PDF Reports**: Professional proposal document generation  
✅ **Cloud Storage**: Secure document storage and retrieval  

## Tech Stack

- Google Agent Development Kit (ADK)
- Google Cloud Storage
- ReportLab for PDF generation
- Gemini 2.5 Pro AI model

## Setup

1. Set up environment variables:
   ```bash
   GOOGLE_API_KEY=your_api_key
   STORAGE_BUCKET=your_bucket
   GOOGLE_CLOUD_PROJECT=your_project
   GOOGLE_CLOUD_LOCATION=your_location
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the agent:
   ```bash
   python agent.py
   ```