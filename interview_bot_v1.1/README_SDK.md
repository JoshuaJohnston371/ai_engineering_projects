# 🤖 AI Career Interview Bot - OpenAI Agents SDK Edition

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Agents%20SDK-green.svg)
![Gradio](https://img.shields.io/badge/Gradio-Interface-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**An intelligent career chatbot built with OpenAI Agents SDK that represents you in job interviews, handles tool calls automatically, and maintains conversation quality through AI-powered evaluation.**

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Tech Stack](#-tech-stack)

</div>

---

## 📋 Overview

This is a production-ready AI career chatbot that acts as your digital representative during job interviews. Built using the **OpenAI Agents SDK**, it leverages advanced agent orchestration to handle conversations, automatically manage tool calls, and ensure response quality through an integrated evaluation system.

The bot can answer questions about your career, skills, and experience while maintaining professional standards. It includes safety checks, quality evaluation, and automatic tool execution for recording user interactions and unknown questions.

### 🎯 Key Highlights

- **Agent-Based Architecture**: Uses OpenAI Agents SDK for intelligent conversation management
- **Automatic Tool Handling**: Tools are executed automatically by the Runner - no manual loops needed
- **Quality Assurance**: Built-in evaluator agent ensures responses meet professional standards
- **Safety First**: Multi-layer safety checks prevent offensive content
- **Production Ready**: Includes error handling, logging, and graceful fallbacks

---

## ✨ Features

### 🧠 Intelligent Agent System
- **Response Agent**: Handles conversations and represents you authentically
- **Evaluator Agent**: Validates response quality and provides feedback
- **Automatic Tool Execution**: SDK Runner handles tool calls seamlessly

### 🛠️ Built-in Tools
- **`record_user_details`**: Captures contact information from interested parties
- **`record_unknown_question`**: Logs questions that couldn't be answered (with push notifications)

### 🛡️ Safety & Quality
- **Safety Classifier**: AI-powered content moderation
- **Response Evaluator**: Ensures professional, accurate responses
- **Automatic Rerun**: Improves responses based on evaluator feedback
- **Strike System**: Progressive warnings for inappropriate behavior

### 💬 Conversation Management
- **Context Preservation**: Maintains full conversation history
- **Gradio Interface**: Beautiful, interactive chat UI
- **Message Format Support**: Handles Gradio's message format natively

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input (Gradio)                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Safety Check (AI Classifier)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         Runner.run_sync() - Agent Orchestration             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Response Agent (with Tools)                  │   │
│  │  • System Prompt with Context                        │   │
│  │  • Automatic Tool Execution                          │   │
│  │  • Conversation Management                           │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         Evaluator Agent - Quality Check                    │
│  • Validates response quality                              │
│  • Provides feedback if unacceptable                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         Rerun (if needed) - No Tools                       │
│  • Improves response based on feedback                     │
│  • Prevents duplicate tool calls                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
                  Final Response
```

### Key Components

1. **Me Class**: Main orchestrator class that manages agents and conversation flow
2. **Response Agent**: Primary agent that handles user interactions
3. **Evaluator Agent**: Validates response quality
4. **Runner**: SDK component that executes agents and handles tool calls
5. **Tool Functions**: Decorated with `@function_tool` for SDK integration

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key
- Pushover account (for notifications - optional)
- Google API key (for Gemini - optional, currently using OpenAI)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd interview_bot_v1.1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PUSHOVER_TOKEN=your_pushover_token_here
   PUSHOVER_USER=your_pushover_user_here
   GOOGLE_API_KEY=your_google_api_key_here  # Optional
   ```

4. **Prepare your profile data**
   
   Create a `me/` directory with:
   - `linkedin.pdf` - Your LinkedIn profile (PDF)
   - `summary.txt` - Brief summary about yourself
   - `resume.txt` - Your resume text

5. **Run the application**
   ```bash
   python app_sdk.py
   ```

6. **Access the interface**
   
   Open your browser to the URL shown in the terminal (typically `http://127.0.0.1:7860`)

---

## 💻 Usage

### Basic Usage

Once the application is running, you can:

1. **Start a conversation** in the Gradio interface
2. **Ask questions** about the person's career, skills, or experience
3. **Provide contact information** - the bot will record it automatically
4. **Ask unknown questions** - the bot will log them and notify you

### Example Interactions

**Career Questions:**
```
User: "What's your experience with machine learning?"
Bot: [Provides detailed answer based on resume/LinkedIn]
```

**Contact Information:**
```
User: "My name is John Doe and my email is john@example.com"
Bot: [Records details and sends push notification]
```

**Unknown Questions:**
```
User: "What's your favorite programming language?"
Bot: [Logs question, sends notification, responds politely]
```

### Tool Execution

Tools are automatically executed by the SDK Runner when the agent decides to use them. No manual intervention required!

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Framework** | OpenAI Agents SDK | Agent orchestration and tool management |
| **LLM** | GPT-4o-mini | Primary language model |
| **UI Framework** | Gradio | Interactive chat interface |
| **Data Validation** | Pydantic | Structured output validation |
| **PDF Processing** | PyPDF | LinkedIn profile parsing |
| **Notifications** | Pushover API | Real-time alerts |
| **Environment** | python-dotenv | Configuration management |

---

## 📁 Project Structure

```
interview_bot_v1.1/
│
├── app_sdk.py              # Main application file
├── requirements.txt        # Python dependencies
├── README_SDK.md          # This file
│
├── me/                     # Profile data directory
│   ├── linkedin.pdf       # LinkedIn profile
│   ├── summary.txt        # Personal summary
│   └── resume.txt         # Resume text
│
└── .env                    # Environment variables (create this)
```

---

## 🔧 Configuration

### Customizing the Bot

Edit the `system_prompt()` method in the `Me` class to customize:
- Bot personality and tone
- Tool usage rules
- Response style

### Adjusting Safety Settings

Modify `safety_check_agent()` to:
- Change safety thresholds
- Customize warning messages
- Adjust strike system behavior

### Tool Customization

Add new tools by:
1. Creating a function decorated with `@function_tool`
2. Adding it to `tools_sdk` list
3. Updating the system prompt to instruct the agent on usage

---

## 🎓 Key Learning Points

This project demonstrates:

1. **Agent Orchestration**: Using OpenAI Agents SDK for complex AI workflows
2. **Automatic Tool Management**: How the SDK handles tool calls automatically
3. **Quality Assurance**: Implementing AI-powered response evaluation
4. **Production Patterns**: Error handling, logging, and graceful degradation
5. **Conversation Management**: Maintaining context across interactions

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'agents'`
- **Solution**: Install `openai-agents` package: `pip install openai-agents`

**Issue**: Tools not being called
- **Solution**: Ensure tools are properly decorated with `@function_tool` and have type annotations

**Issue**: Safety check always returns None
- **Solution**: Check that `OPENAI_API_KEY` is set correctly in `.env`

**Issue**: PDF reading errors
- **Solution**: Ensure `me/linkedin.pdf` exists and is a valid PDF

---

## 📝 Code Highlights

### Agent Initialization
```python
self.response_agent = Agent(
    name="Interview responder Agent (acting as me)",
    instructions=self.system_prompt(),
    tools=tools_sdk,
    model="gpt-4o-mini"
)
```

### Tool Definition
```python
@function_tool
def record_unknown_question(question: str):
    """Always use this tool to record any question that couldn't be answered"""
    return record_unknown_question_func(question)
```

### Runner Execution
```python
runner = Runner()
result = runner.run_sync(
    starting_agent=self.response_agent,
    input=conversation_context
)
reply = result.final_output
```

---

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Share your own implementations

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Joshua Johnston**

- Portfolio: [Your Portfolio URL]
- LinkedIn: [Your LinkedIn URL]
- Email: [Your Email]

---

## 🙏 Acknowledgments

- OpenAI for the Agents SDK
- Gradio team for the excellent UI framework
- The open-source community for inspiration and tools

---

<div align="center">

**Built with ❤️ using OpenAI Agents SDK**

⭐ Star this repo if you find it useful!

</div>

