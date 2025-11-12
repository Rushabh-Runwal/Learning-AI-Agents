# Project 8: Content Orchestration Agent

An AI-powered content orchestration agent built with **Google's Agent Development Kit (ADK) 1.16.0** that generates comprehensive educational content on any topic.

## 🌟 Features

- **📚 Reading Material**: Comprehensive articles with structured sections
- **📝 Quizzes**: Interactive multiple-choice assessments (5-20 questions)
- **🎥 Video Content**: Complete video scripts with timestamps and visual suggestions
- **🎮 Educational Games**: Interactive game designs with implementation guides
- **☁️ Vertex AI Deployment**: Deploy to Google Cloud for production use

## 🚀 Quick Start

### Local Development

#### 1. Setup

```bash
cd 8-content-orchestration
poetry install
```

Or with pip:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Configure API Key

Create a `.env` file:
```bash
GOOGLE_API_KEY=your_api_key_here
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

#### 3. Run

```bash
python api_server.py
```

Open: **http://localhost:8000**

### Vertex AI Deployment

For production deployment to Google Cloud Vertex AI, see the comprehensive [DEPLOYMENT.md](DEPLOYMENT.md) guide.

**Quick deployment:**
```bash
# Configure .env for Vertex AI
cp .env.example .env
# Edit .env with your Google Cloud settings

# Deploy to Vertex AI
poetry run deploy-remote --create

# Create a session and start using
poetry run deploy-remote --create_session --resource_id=<your-resource-id>
```

## 🎯 Usage Examples

Try these:
- "Create content about Photosynthesis"
- "Generate a quiz on Python with 10 questions"
- "Make a video script about Machine Learning"
- "Design an educational game about the Solar System"

## 📦 Project Structure

```
8-content-orchestration-agent/
├── api_server.py              # FastAPI server
├── content_orchestration_agent/
│   ├── agent.py               # ADK orchestration agent
│   ├── config.py              # Configuration
│   └── tools/                 # 4 content generators
├── frontend/index.html        # Web UI
└── requirements.txt           # Dependencies
```

## 🔧 Configuration

Optional environment variables:

```bash
ORCHESTRATOR_MODEL=gemini-2.5-flash
CONTENT_GENERATOR_MODEL=gemini-2.5-flash
PORT=8000
```

## 🐛 Troubleshooting

**Port in use?**
```bash
lsof -i :8000
kill -9 <PID>
```

**API Key not set?**
```bash
echo "GOOGLE_API_KEY=your_key" > .env
```

## 📖 Learn More

- **Google ADK**: https://github.com/google/adk-python
- **ADK Docs**: https://google.github.io/adk-docs/
- **Get API Key**: https://makersuite.google.com/app/apikey
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Vertex AI**: https://cloud.google.com/vertex-ai

## 🚢 Deployment Options

### Local Testing
```bash
poetry run deploy-local --create_session
poetry run deploy-local --send --session_id=<id> --message="Create content about AI"
```

### Production (Vertex AI)
```bash
poetry run deploy-remote --create
poetry run deploy-remote --create_session --resource_id=<id>
poetry run deploy-remote --send --resource_id=<id> --session_id=<sid> --message="Your query"
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.

---

**Project 8 of AI Agent Series** - Building production-grade AI agents!

