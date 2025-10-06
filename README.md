# 31 AI Agents in 31 Days 🤖

A collection of AI agents built with Google's Agent Development Kit (ADK), showcasing different use cases and architectures for intelligent automation.

## 🚀 Projects Overview

This repository contains 4 distinct AI agent implementations, each demonstrating different capabilities and architectural patterns:

### 1. 🏠 [Renovation Agent](./1-renovation-agent/)
**Smart Home Renovation Planning**
- AI-powered renovation planning and cost estimation
- Professional PDF proposal generation
- Google Cloud Storage integration
- Uses Gemini 2.5 Pro for intelligent recommendations

### 2. 🤖 [Personal Assistant Agent](./2-personal_assistant/)
**Multi-Functional AI Assistant**
- Web search and real-time information retrieval
- Currency exchange rate lookup
- Wikipedia knowledge base integration
- Hotel search and travel assistance
- Extensible multi-tool architecture

### 3. 🎓 [Education Counselor Agent](./3-education_counselor/)
**Personalized Education Guidance**
- Specialized for Indian students' educational pathways
- Multi-agent architecture with specialized sub-agents
- Program matching and application planning
- Budget analysis and funding guidance
- Compliance and eligibility verification

### 4. 🛒 [Ecommerce Cart Agent](./4-ecommerce-cart-agent/)
**Stateful Shopping Experience**
- Complete ecommerce shopping cart system
- Multi-agent coordination for different shopping phases
- Persistent state management
- Product catalog, inventory, and order tracking
- Full checkout and order management flow

## 🛠️ Tech Stack

- **Google Agent Development Kit (ADK)** - Core agent framework
- **Gemini AI Models** - 2.0 Flash, 2.5 Flash, 2.5 Pro
- **Google Cloud Platform** - Storage, authentication, and deployment
- **LangChain** - Third-party tool integrations
- **Python** - Primary development language

## 🏗️ Architecture Patterns

Each project demonstrates different AI agent patterns:

- **Single Agent**: Simple, focused functionality
- **Multi-Agent Systems**: Coordinated specialist agents
- **Stateful Agents**: Persistent data and session management
- **Tool Integration**: External APIs and services
- **Document Generation**: PDF reports and proposals

## 🚀 Getting Started

Each project has its own setup instructions in its respective README. General setup:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rushabh-Runwal/31-AI-Agents-in-31-Days.git
   cd 31-AI-Agents-in-31-Days
   ```

2. **Set up environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt  # For individual projects
   ```

4. **Configure APIs**:
   - Set up Google Cloud credentials
   - Configure API keys for external services
   - Review individual project setup instructions

## 📁 Repository Structure

```
31-AI-Agents-in-31-Days/
├── 1-renovation-agent/          # Home renovation planning agent
├── 2-personal_assistant/        # Multi-tool personal assistant
├── 3-education_counselor/       # Educational pathway guidance
├── 4-ecommerce-cart-agent/     # Stateful shopping cart system
├── .gitignore                   # Python/AI project exclusions
├── pyproject.toml              # Project configuration
└── README.md                   # This overview
```

## 🎯 Use Cases

These agents demonstrate practical applications for:

- **Business Automation**: Customer service, sales support, consultation
- **Personal Productivity**: Research, planning, task management
- **Education Technology**: Personalized guidance, application assistance
- **E-commerce**: Shopping assistance, order management
- **Professional Services**: Proposal generation, client consultation

## 🤝 Contributing

Each agent project is self-contained and can be extended independently. Feel free to:

- Add new tools and integrations
- Improve existing agent capabilities
- Create new specialized sub-agents
- Enhance the user interface and experience

## 📝 License

Open source - feel free to use these examples for learning and building your own AI agents!

---

**Built with ❤️ using Google Agent Development Kit**