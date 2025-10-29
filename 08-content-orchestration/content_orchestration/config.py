"""Configuration for the Content Orchestration Agent"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Vertex AI Configuration
USE_VERTEX_AI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE"
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
GOOGLE_CLOUD_STAGING_BUCKET = os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validate configuration based on mode
# Heuristic: If running in GCP context (project present) and no API key, prefer Vertex AI automatically
if not USE_VERTEX_AI and GOOGLE_CLOUD_PROJECT and not GOOGLE_API_KEY:
    USE_VERTEX_AI = True

if not USE_VERTEX_AI:
    # Only require GOOGLE_API_KEY if explicitly not using Vertex AI
    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is required when not using Vertex AI. "
            "Get your API key from https://makersuite.google.com/app/apikey or "
            "set GOOGLE_GENAI_USE_VERTEXAI=TRUE to use Vertex AI"
        )

# Model Configuration
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "gemini-2.5-flash")
CONTENT_GENERATOR_MODEL = os.getenv("CONTENT_GENERATOR_MODEL", "gemini-2.5-flash")

# Server Configuration
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

# Content Generation Defaults
DEFAULT_DIFFICULTY = "intermediate"
DEFAULT_LENGTH = "medium"
DEFAULT_QUIZ_QUESTIONS = 10

