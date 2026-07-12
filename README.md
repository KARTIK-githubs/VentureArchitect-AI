# VentureArchitect AI 🚀

> **Transform your startup idea into a complete, investor-ready business blueprint using a multi-agent AI workflow.**

🌐 **Live Demo:** https://venturearchitect-ai.onrender.com

---

## Overview

VentureArchitect AI is a Flask-based web application that helps entrepreneurs transform early-stage startup ideas into structured business blueprints.

Instead of relying on a single AI response, the application follows a **multi-agent workflow** where five specialized AI agents collaborate to analyze different aspects of a startup. Each agent contributes its expertise, and their outputs are combined into a comprehensive blueprint covering idea validation, market research, business strategy, risk analysis, and investor pitching.

Whether you're validating a new idea or preparing for a startup competition, VentureArchitect AI provides a structured starting point for turning concepts into actionable business plans.

---

## Features

- 🤖 Multi-agent AI workflow coordinated by a Supervisor Agent
- 💡 Startup idea validation and refinement
- 📊 Market research and competitor analysis
- 📈 Business model and revenue strategy generation
- ⚠️ Risk assessment with mitigation strategies
- 🎤 Investor pitch and executive summary generation
- 📋 Interactive blueprint viewer with copy functionality
- 📱 Responsive interface for desktop and mobile devices

---

## Workflow

```text
                     Startup Idea
                          │
                          ▼
                  Supervisor Agent
                          │
      ┌──────────┬─────────┼─────────┬──────────┐
      ▼          ▼         ▼         ▼          ▼
  Idea        Market    Business    Risk    Investor
 Analysis    Research   Strategy   Analysis   Pitch
      │          │         │         │          │
      └──────────┴─────────┴─────────┴──────────┘
                          │
                          ▼
            Comprehensive Startup Blueprint
```

Each agent focuses on a specific responsibility while building upon the previous agent's output, resulting in a structured and coherent business blueprint rather than a single generic response.

---

## Screenshots

### 🏠 Landing Page

![Landing Page](https://github.com/user-attachments/assets/6c2226dc-e729-4201-87de-993ecda86649)

---

### ⚙️ Blueprint Generation

![Blueprint Generation](https://github.com/user-attachments/assets/18b9c94f-ec0f-4983-b0de-74b31dc5b82f)

---

### 📄 Generated Startup Blueprint

![Generated Blueprint](https://github.com/user-attachments/assets/b4d78087-8587-414a-a851-77ed848f89a0)

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python, Flask |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **AI** | IBM watsonx.ai, IBM Granite Models |
| **Deployment** | Render |
| **Version Control** | Git & GitHub |

---

## Project Structure

```text
VentureArchitect-AI/
│
├── app/
│   ├── agents/          # AI agents and workflow
│   ├── routes/          # Flask routes
│   ├── services/        # IBM watsonx integration
│   ├── static/          # CSS & JavaScript
│   └── templates/       # HTML templates
│
├── run.py
├── requirements.txt
├── .env
└── README.md
```

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/KARTIK-githubs/VentureArchitect-AI.git
cd VentureArchitect-AI
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
IBM_API_KEY=your_api_key
IBM_PROJECT_ID=your_project_id
IBM_WATSONX_URL=https://au-syd.ml.cloud.ibm.com

FLASK_SECRET_KEY=your_secret_key
```

Start the application:

```bash
python run.py
```

Visit:

```
http://localhost:5000
```

---

## Why VentureArchitect AI?

Many AI-powered startup assistants generate a single generic response.

VentureArchitect AI follows a **multi-agent workflow**, where specialized AI agents independently analyze different aspects of a startup idea before combining their outputs into a structured business blueprint.

This approach produces more organized, transparent, and actionable results while making the reasoning process easier to follow.

---

## Future Improvements

- 📄 Export blueprints as PDF
- 📊 AI-generated financial forecasting
- 👥 User accounts and blueprint history
- 🤝 Team collaboration workspace
- 🏭 Industry-specific startup templates
- 📑 Automatic pitch deck generation

---

## Author

**Kartik Aggarwal**

B.Tech Information Technology  
Maharaja Surajmal Institute of Technology (MSIT)

GitHub: https://github.com/KARTIK-githubs

---

## Acknowledgements

This project was built using:

- IBM watsonx.ai
- IBM Granite Models
- Flask
- Bootstrap 5
- Render

---

⭐ **If you found this project interesting, consider giving it a star on GitHub!**
