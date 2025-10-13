"""
Configuration for Research Assistant Agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Vertex AI Configuration (optional)
USE_VERTEX_AI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE"
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
GOOGLE_CLOUD_STAGING_BUCKET = os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Configuration
SEARCH_MODEL = "gemini-2.0-flash-exp"  # Fast search
ANALYSIS_MODEL = "gemini-2.5-flash"    # Deep analysis
SYNTHESIS_MODEL = "gemini-2.5-flash"   # Report generation

# Validate configuration based on mode
# When deployed to Vertex AI, the environment variables may not be available
# So we only validate if GOOGLE_GENAI_USE_VERTEXAI is explicitly set to FALSE
if USE_VERTEX_AI or (GOOGLE_CLOUD_PROJECT and not GOOGLE_API_KEY):
    # When using Vertex AI, project validation is optional as it can be auto-detected
    # and GOOGLE_API_KEY is not needed.
    pass
elif os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").upper() == "FALSE":
    # Only require GOOGLE_API_KEY if explicitly not using Vertex AI
    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is required when not using Vertex AI. "
            "Get your API key from https://makersuite.google.com/app/apikey or "
            "set GOOGLE_GENAI_USE_VERTEXAI=TRUE to use Vertex AI"
        )
