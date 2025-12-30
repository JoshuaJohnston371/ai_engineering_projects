# Deep Research System v1.5

An advanced, production-ready multi-agent AI system that autonomously conducts comprehensive research, generates high-quality reports, and delivers them via email. Built using the OpenAI Agents SDK, this system demonstrates sophisticated agentic workflows, strategic model selection, and iterative quality improvement patterns.

## 🎯 Overview

The Deep Research System transforms a simple research query into a comprehensive, well-formatted research report through an intelligent multi-stage pipeline. The system employs multiple specialized AI agents that work together autonomously, with built-in quality evaluation and iterative refinement to ensure exceptional output quality.

## 🏗️ Architecture

### Agentic Workflow Pattern

This system implements a sophisticated **agents-as-tools** architecture where specialized agents are converted into tools that can be orchestrated by a manager agent. This pattern enables:

- **Autonomous Decision Making**: The research manager agent decides how to use its tools based on context
- **Modular Design**: Each agent has a specific responsibility and can be developed/tested independently
- **Flexible Orchestration**: Agents can be composed in different ways for different use cases
- **Tool Reusability**: Agents can be used as tools by other agents, creating powerful composition patterns

### Multi-Agent System Components

1. **Query Clarifier Agent** - Generates 3 clarifying questions to refine user queries
2. **Research Manager Agent** - Orchestrates the research process using specialized tool agents
3. **Planner Agent** - Creates strategic search plans based on the research query
4. **Search Agent** - Performs web searches and summarizes results
5. **Draft Report Agent** - Generates comprehensive draft reports from research findings
6. **Evaluator Agent** - Critically evaluates report quality and provides actionable feedback
7. **Final Report Agent** - Formats and polishes reports with summaries and follow-up questions
8. **Email Agent** - Converts markdown to HTML and sends reports via email

### Evaluator-Optimizer Pattern

The system implements a powerful **evaluator-optimizer feedback loop**:

1. **Generation Phase**: Research Manager generates a draft report using tool agents
2. **Evaluation Phase**: Evaluator Agent critically reviews the report against quality standards
3. **Feedback Integration**: If quality thresholds aren't met, feedback is passed back to the Research Manager
4. **Iterative Refinement**: The Research Manager uses feedback to improve subsequent iterations
5. **Acceptance Criteria**: Process continues until quality score ≥ 0.90 or max iterations reached

This pattern ensures continuous quality improvement and addresses gaps or weaknesses in the research output.

## 🧠 Strategic Model Selection

A key architectural decision is the **strategic use of different models** for different tasks:

### Generation Models (GPT-4o-mini / GPT-4.1-mini)
- **Used for**: Research planning, web search summarization, draft report generation, final formatting
- **Rationale**: These tasks require broad knowledge and generation capabilities but don't need the highest reasoning power. Using smaller models:
  - Reduces API costs significantly
  - Maintains high quality for generation tasks
  - Enables faster response times
  - Allows for more iterations within budget constraints

### Evaluation Model (GPT-4.1)
- **Used for**: Critical evaluation of report quality, identifying gaps, providing actionable feedback
- **Rationale**: Evaluation requires sophisticated reasoning, critical thinking, and the ability to identify subtle issues:
  - Needs higher reasoning capabilities to assess quality comprehensively
  - Must be "tough but fair" in evaluation
  - Requires understanding of nuanced requirements
  - Critical for maintaining high output standards

This cost-optimized approach balances quality and efficiency, ensuring critical evaluation uses the most capable model while generation tasks use appropriately-sized models.

## 🔄 Workflow

```
User Query
    ↓
Query Clarifier → 3 Clarifying Questions
    ↓
Refined Query
    ↓
Research Manager Agent
    ├─→ Planner Agent (creates search strategy)
    ├─→ Search Agent (performs web searches)
    └─→ Draft Report Agent (generates initial report)
    ↓
Evaluator Agent (evaluates quality)
    ├─→ Score ≥ 0.90? → Accept
    └─→ Score < 0.90? → Feedback → Research Manager (iterate)
    ↓
Final Report Agent (formatting & polish)
    ↓
Email Agent (HTML conversion & delivery)
    ↓
Gradio UI Display
```

## ✨ Key Features

- **Autonomous Multi-Agent Orchestration**: Agents work together without manual intervention
- **Iterative Quality Improvement**: Up to 10 refinement rounds with quality scoring
- **Feedback-Driven Refinement**: Evaluation feedback automatically improves subsequent iterations
- **Cost-Optimized Architecture**: Strategic model selection balances quality and efficiency
- **Comprehensive Error Handling**: Robust error handling at every stage with graceful degradation
- **Email Integration**: Automatic HTML conversion and email delivery
- **Modern UI**: Clean Gradio interface with progress tracking
- **Full Observability**: OpenAI trace integration for debugging and monitoring

## 🛠️ Technology Stack

- **OpenAI Agents SDK** - Multi-agent orchestration and tool management
- **Gradio** - Modern web UI framework
- **Pydantic** - Type-safe data validation and models
- **Python-dotenv** - Environment variable management
- **SMTP** - Email delivery (configurable for Gmail, Outlook, etc.)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd deep_research_v1.5
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file with:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   
   # Optional: Email configuration
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   FROM_EMAIL=your_email@gmail.com
   TO_EMAIL=recipient@example.com
   ```

4. **Run the application**
   ```bash
   python deep_research.py
   ```

## 🚀 Usage

1. Enter your research query in the Gradio interface
2. Answer the 3 clarifying questions generated by the system
3. The system will autonomously:
   - Plan research strategy
   - Perform web searches
   - Generate and refine reports
   - Format and email the final report
4. View the comprehensive report in the UI

## 🎓 Design Patterns Demonstrated

- **Agents-as-Tools**: Converting agents into reusable tools
- **Evaluator-Optimizer Loop**: Quality assurance through iterative refinement
- **Manager-Worker Pattern**: Central manager orchestrating specialized workers
- **Feedback Propagation**: Passing evaluation feedback through the agent chain
- **Strategic Model Selection**: Using appropriate models for different task types
- **Error Handling & Resilience**: Comprehensive error handling with fallbacks

## 📊 Performance Characteristics

- **Quality Threshold**: Reports must achieve ≥ 0.90 quality score
- **Max Iterations**: Up to 10 refinement rounds
- **Report Length**: 5-10 pages, 1000+ words
- **Search Strategy**: 5 targeted web searches per query
- **Evaluation Criteria**: Completeness, accuracy, relevance, structure

## 🔍 Technical Highlights

- **Type Safety**: Full Pydantic model validation throughout
- **Async/Await**: Non-blocking operations for better performance
- **Streaming Output**: Real-time progress updates via Gradio
- **Trace Integration**: Full observability with OpenAI traces
- **Modular Architecture**: Clean separation of concerns
- **Extensible Design**: Easy to add new agents or modify workflows

## 🎯 Use Cases

- Market research and competitive analysis
- Technical deep-dives and literature reviews
- Business intelligence gathering
- Academic research assistance
- Industry trend analysis
- Product research and evaluation

## 🤝 Contributing

This project demonstrates production-ready patterns for building multi-agent AI systems. Key areas for extension:

- Additional specialized agents (data analysis, visualization)
- Custom evaluation criteria
- Integration with additional data sources
- Enhanced email formatting options
- Multi-language support

## 📝 License

[Specify your license]

## 👤 Author

Built as a demonstration of advanced AI engineering practices, multi-agent system design, and production-ready software architecture.

---

**Note**: This system showcases enterprise-grade patterns for building autonomous AI systems that can operate independently while maintaining high quality standards through built-in evaluation and refinement mechanisms.
