# 🤖 AI Engineering Portfolio

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Agents%20SDK-green.svg)

**A curated collection of AI engineering projects showcasing practical applications of artificial intelligence, machine learning, and modern AI frameworks.**

[Projects](#-projects) • [Getting Started](#-getting-started) • [Project Structure](#-project-structure)

</div>

---

## 📋 Overview

This repository serves as my **AI Engineering Portfolio**, housing a collection of production-ready AI projects that demonstrate various aspects of artificial intelligence engineering, from conversational AI agents to machine learning applications.

Each project in this portfolio is designed to showcase:
- **Real-world problem solving** with AI technologies
- **Production-ready code** with proper architecture and error handling
- **Modern AI frameworks** and best practices
- **Documentation and maintainability**

---

## ✨ Projects

### 🤖 [Interview Bot v1.1](./interview_bot_v1.1/)

**An intelligent career chatbot built with OpenAI Agents SDK**

A production-ready AI career chatbot that acts as a digital representative during job interviews. Built using the **OpenAI Agents SDK**, it leverages advanced agent orchestration to handle conversations, automatically manage tool calls, and ensure response quality through an integrated evaluation system.

**Key Features:**
- Agent-based architecture with automatic tool handling
- Quality assurance through built-in evaluator agent
- Safety checks and content moderation
- Interactive Gradio interface

**Tech Stack:** OpenAI Agents SDK, GPT-4o-mini, Gradio, Pydantic

[View Project Details →](./interview_bot_v1.1/README_SDK.md)

---

### 🔬 [Deep Research System v1.5](./deep_research_v1.5/)

**Autonomous multi-agent research system with iterative quality improvement**

An advanced, production-ready multi-agent AI system that autonomously conducts comprehensive research, generates high-quality reports, and delivers them via email. Built using the **OpenAI Agents SDK**, it demonstrates sophisticated agentic workflows, strategic model selection, and iterative quality improvement patterns.

**Key Features:**
- **Agents-as-Tools Architecture**: Specialized agents converted into reusable tools orchestrated by a central manager
- **Evaluator-Optimizer Pattern**: Iterative refinement loop with quality scoring (≥0.90 threshold)
- **Strategic Model Selection**: GPT-4o-mini for generation tasks, GPT-4.1 for critical evaluation
- **Autonomous Workflow**: Query clarification → Research planning → Web search → Report generation → Quality evaluation → Iterative refinement → Email delivery
- **Comprehensive Error Handling**: Robust error handling at every stage with graceful degradation
- **Cost-Optimized**: Reduces API costs by up to 80% through strategic model selection

**Tech Stack:** OpenAI Agents SDK, GPT-4o-mini, GPT-4.1, Gradio, Pydantic, SMTP

[View Project Details →](./deep_research_v1.5/README.md)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- OpenAI API key (for projects using OpenAI)

### Repository Structure

Each project in this portfolio is self-contained with its own:
- `README.md` - Project-specific documentation
- `requirements.txt` - Python dependencies
- Source code and configuration files

### Exploring Projects

1. **Browse the project directories** to see available projects
2. **Read individual project READMEs** for detailed setup instructions
3. **Follow project-specific installation guides** in each project folder

---

## 📁 Project Structure

```
ai_engineering_projects/
│
├── README.md                    # This file - Portfolio overview
├── requirements.txt             # Root-level dependencies (if any)
├── pyproject.toml              # Python project configuration
│
├── interview_bot_v1.1/         # Interview Bot Project
│   ├── chat_bot.py            # Main application
│   ├── requirements.txt       # Project dependencies
│   └── README_SDK.md         # Project documentation
│
├── deep_research_v1.5/         # Deep Research System Project
│   ├── deep_research.py       # Main Gradio application
│   ├── orchestrator.py        # Multi-agent orchestration
│   ├── research_manager_agent.py  # Research manager agent
│   ├── evaluator_optimizer_agent.py  # Quality evaluation agent
│   ├── final_report_agent.py  # Report formatting agent
│   ├── email_agent.py         # Email delivery agent
│   ├── clarifier_agent.py     # Query clarification agent
│   ├── tool_agents/           # Specialized tool agents
│   ├── requirements.txt       # Project dependencies
│   └── README.md             # Project documentation
│
└── [Future Projects...]        # Additional projects will be added here
```

---

## 🎯 Portfolio Goals

This portfolio is designed to demonstrate:

1. **AI Engineering Expertise**: Practical applications of cutting-edge AI technologies
2. **Production Readiness**: Code quality, architecture, and best practices
3. **Problem-Solving Skills**: Real-world solutions to complex challenges
4. **Continuous Learning**: Evolving projects that incorporate new technologies and techniques

---

## 🛠️ Tech Stack Overview

Projects in this portfolio utilize various technologies including:

| Technology | Purpose |
|-----------|---------|
| **OpenAI Agents SDK** | Agent orchestration and tool management |
| **GPT Models** | Large language model integration (GPT-4o-mini, GPT-4.1) |
| **Gradio** | Interactive UI development |
| **Python** | Primary programming language |
| **Pydantic** | Data validation and structured outputs |
| **SMTP** | Email delivery and notification |

*Tech stack varies by project - see individual project READMEs for specifics*

---

## 📝 Project Guidelines

Each project in this portfolio follows these principles:

- ✅ **Well-documented** with comprehensive README files
- ✅ **Production-ready** with proper error handling and logging
- ✅ **Modular architecture** for maintainability and extensibility
- ✅ **Best practices** following Python and AI engineering standards

---

## 🔮 Future Projects

This portfolio is actively growing. Upcoming projects may include:

- Machine learning model implementations
- AI-powered automation tools
- Advanced agent systems
- Data analysis and visualization projects
- Integration projects combining multiple AI services

*Check back regularly for new additions!*

---

## 👤 Author

**Joshua Johnston**

- Portfolio: TBC
- LinkedIn: www.linkedin.com/in/joshua-johnston-5800a613b
- Email: j.johnston371@hotmail.com

---

## 🙏 Acknowledgments

- OpenAI for providing excellent AI tools and frameworks
- The open-source community for inspiration and support
- All contributors and maintainers of the libraries used in these projects

---

<div align="center">

**Built with ❤️ for AI Engineering**

⭐ Star this repo if you find it useful!

*Last updated: 2024*

</div>
