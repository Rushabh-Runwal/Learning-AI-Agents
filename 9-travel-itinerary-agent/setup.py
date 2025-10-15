#!/usr/bin/env python3
"""Setup script for Travel Itinerary Planner."""

import os
import subprocess
import sys
from pathlib import Path


def create_env_file():
    """Create .env file with template values."""
    env_content = """# Google Gemini API Configuration
# Get your API key from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your-google-api-key-here

# Apify API Configuration
# Get your token from: https://console.apify.com/account/integrations
APIFY_API_TOKEN=your-apify-token-here

# Optional: Use Vertex AI instead of Gemini API
# GOOGLE_GENAI_USE_VERTEXAI=TRUE
# GOOGLE_CLOUD_PROJECT=your-project-id
# GOOGLE_CLOUD_LOCATION=us-central1
"""
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file with template values")
        print("   Please update with your actual API keys")
    else:
        print("ℹ️  .env file already exists")


def install_dependencies():
    """Install required dependencies."""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def test_imports():
    """Test if all imports work correctly."""
    try:
        print("🧪 Testing imports...")
        from agent import root_agent
        print("✅ Agent imports successful")
        print(f"   Root agent: {root_agent.name}")
        print(f"   Model: {root_agent.model}")
        print(f"   Sub-agents: {len(root_agent.sub_agents)}")
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🌍 Travel Itinerary Planner Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("agent").exists() or not Path("requirements.txt").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Setup failed during import testing")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update .env file with your actual API keys")
    print("2. Run: python main.py")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
