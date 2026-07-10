# VentureArchitect AI 🚀

> **Transform any startup idea into an investor-ready blueprint in minutes.**
> Powered by IBM watsonx.ai and IBM Granite Foundation Models.

---

## Overview

VentureArchitect AI is a production-quality Flask web application that acts as an **AI startup co-founder**. It orchestrates five specialized IBM Granite-powered AI agents through a Supervisor Agent to analyze your raw startup idea and generate a comprehensive, investor-ready startup blueprint.

### What It Generates

| Section | Agent |
|---------|-------|
| Startup Idea Refinement & Problem Statement | Idea Analysis Agent |
| Target Audience & Value Proposition | Idea Analysis Agent |
| Market Size (TAM/SAM/SOM) & Industry Trends | Market Research Agent |
| Customer Segments & Competitor Analysis | Market Research Agent |
| Business Model Canvas (all 9 blocks) | Business Strategy Agent |
| Revenue Strategy & Pricing Tiers | Business Strategy Agent |
| Go-To-Market Strategy & Unit Economics | Business Strategy Agent |
| Risk Analysis Matrix & Mitigation Strategies | Risk Analysis Agent |
| 12-Month Startup Roadmap | Risk Analysis Agent |
| Funding Recommendations | Risk Analysis Agent |
| 60-Second Elevator Pitch | Investor Pitch Agent |
| One-Page Investor Summary | Investor Pitch Agent |
| Investor FAQ & Pre-empted Objections | Investor Pitch Agent |

---

## Architecture

```
VentureArchitect AI/
│
├── run.py                          # Application entry point
├── requirements.txt
├── .env                            # Credentials (never commit)
│
└── app/
    ├── __init__.py                 # Flask application factory
    ├── config.py                   # Configuration classes
    │
    ├── agents/
    │   ├── __init__.py
    │   ├── base_agent.py           # Abstract base class for all agents
    │   ├── supervisor_agent.py     # Orchestrates the full pipeline
    │   ├── idea_analysis_agent.py  # Agent 1: Idea refinement
    │   ├── market_research_agent.py# Agent 2: Market research
    │   ├── business_strategy_agent.py # Agent 3: Business model
    │   ├── risk_analysis_agent.py  # Agent 4: Risk analysis
    │   └── investor_pitch_agent.py # Agent 5: Investor pitch
    │
    ├── services/
    │   ├── __init__.py
    │   └── watsonx_service.py      # IBM watsonx.ai LLM client (singleton)
    │
    ├── routes/
    │   ├── __init__.py
    │   └── main.py                 # Flask routes (pages + API)
    │
    ├── schemas/
    │   ├── __init__.py
    │   └── blueprint_schema.py     # AgentResult, BlueprintContext dataclasses
    │
    ├── templates/
    │   ├── base.html               # Base layout with navbar/footer
    │   ├── index.html              # Landing page + idea input
    │   └── blueprint.html          # Blueprint results page
    │
    └── static/
        ├── css/
        │   └── main.css            # Custom SaaS dark-mode styles
        └── js/
            ├── main.js             # Landing page + progress tracker
            └── blueprint.js        # Blueprint rendering + markdown parser
```

### Agent Pipeline

```
User Idea
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                    Supervisor Agent                      │
│  Orchestrates execution, passes context between agents  │
└──────────┬──────────────────────────────────────────────┘
           │
    ┌──────▼──────┐   context   ┌───────────────┐   context
    │  Agent 1:   │ ──────────► │   Agent 2:    │ ──────────►  ...
    │    Idea     │             │    Market     │
    │  Analysis   │             │   Research    │
    └─────────────┘             └───────────────┘

Each agent receives the startup idea + all prior agent outputs as context.
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- IBM Cloud account with watsonx.ai access
- IBM Project ID and API Key

### 1. Clone / Download

```bash
git clone <repo-url>
cd "VentureArchitect AI"
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Edit the `.env` file in the project root:

```env
# IBM watsonx.ai Credentials
IBM_API_KEY=your_actual_ibm_api_key
IBM_PROJECT_ID=your_actual_project_id
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Flask
FLASK_SECRET_KEY=your-random-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

> ⚠️ **Never commit `.env` to version control.** It is already in `.gitignore`.

### 5. Run the Application

```bash
python run.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Configuration

### Changing the AI Model

In `app/config.py`:

```python
DEFAULT_MODEL_ID = "ibm/granite-3-3-8b-instruct"  # Change to any IBM Granite model
DEFAULT_MAX_NEW_TOKENS = 1500
DEFAULT_TEMPERATURE = 0.7
```

### Customizing Agent Prompts

Each agent has an `AGENT_INSTRUCTIONS` constant at the top of the class. Edit it to change the agent's persona and behavior:

```python
# In app/agents/idea_analysis_agent.py
AGENT_INSTRUCTIONS = """You are an expert startup idea analyst...
# ← Customize this to change the agent's behavior
"""
```

---

## API Reference

### `POST /api/generate`

Generate a complete startup blueprint.

**Request Body:**
```json
{
  "startup_idea": "Your startup idea description here..."
}
```

**Response:**
```json
{
  "success": true,
  "blueprint": {
    "startup_idea": "...",
    "sections": [
      {
        "agent": "Idea Analysis Agent",
        "title": "Startup Idea Analysis",
        "content": "## Refined Concept\n...",
        "success": true,
        "error": null
      }
    ]
  }
}
```

### `GET /api/agents`

Returns metadata about all available agents.

### `GET /health`

Health check endpoint.

---

## Deployment

### Production with Gunicorn

```bash
# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Run with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

```bash
docker build -t venture-architect-ai .
docker run -p 8000:8000 --env-file .env venture-architect-ai
```

### Environment Variables for Production

| Variable | Description |
|----------|-------------|
| `IBM_API_KEY` | IBM Cloud API key |
| `IBM_PROJECT_ID` | IBM watsonx.ai project ID |
| `IBM_WATSONX_URL` | watsonx.ai endpoint URL |
| `FLASK_SECRET_KEY` | Strong random secret key |
| `FLASK_ENV` | Set to `production` |
| `FLASK_DEBUG` | Set to `False` |

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Flask 3.0 |
| AI Platform | IBM watsonx.ai |
| AI Models | IBM Granite 3.3 8B Instruct |
| Frontend | HTML5, Bootstrap 5, Vanilla JS |
| Styling | Custom CSS (Dark Mode SaaS) |
| Config | python-dotenv |
| Production | Gunicorn |

---

## License

MIT License — see LICENSE file.

---

*Built with IBM watsonx.ai · IBM Granite Foundation Models*
