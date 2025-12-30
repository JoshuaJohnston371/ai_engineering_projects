import gradio as gr
from dotenv import load_dotenv
from helper_functions import get_clarifying_questions, refine_query_with_answers
# from advanced_research_manager import run_advanced_research
# from adv_research_manager_2 import run_advanced_research_alt
#from research_manager import run_advanced_research
from orchestrator import run_advanced_research

load_dotenv(override=True)

async def handle_follow_up(query: str, state: gr.State, progress=gr.Progress()):
    """Handle follow-up clarification by checking clarity again"""
    if not query or not query.strip():
        yield (
            "Please enter a research query first.",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            state
        )
        return

    # Make sections visible immediately with loading message
    loading_message = "**Generating clarifying questions...**\n\nPlease wait..."
    
    progress(0, desc="Generating clarifying questions...")
    
    # Show loading state immediately
    yield (
        loading_message,
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
        state
    )

    clarifying_questions = await get_clarifying_questions(query)
    
    progress(1, desc="Done")
    questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(clarifying_questions.questions)])
    
    state["query"] = query  # type: ignore[index]
    state["questions"] = clarifying_questions.questions  # type: ignore[index]
    
    final_message = f"**Thanks for the query. To help me with my research please answer these questions:**\n\n{questions_text}\n\n*Please provide answers below, then click 'Start Research'*"
    
    yield (
        final_message,
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
        state
    )

async def run_research(answer1: str, answer2: str, answer3: str, state: gr.State):
    questions = []
    answers = []
    if "questions" not in state:  # type: ignore[operator]
        yield "Please generate clarifying questions first."
        return
    
    questions = state["questions"]  # type: ignore[index]
    original_query = state["query"]  # type: ignore[index]
    
    answers = [a.strip() for a in [answer1, answer2, answer3] if a.strip()]
    
    if len(answers) < 3:
        yield "Please answer all 3 clarifying questions before starting research."
        return

    final_query = refine_query_with_answers(original_query, questions, answers)
    
    yield f"**Refined Query:**\n{final_query}\n\n"
    yield "Starting advanced research with autonomous agent manager...\n\n"
    
    async for chunk in run_advanced_research(final_query):
        yield chunk

    # async for chunk in run_advanced_research_alt(final_query):
    #     yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")  # Markdown component for formatted text
    
    with gr.Row():
        query_textbox = gr.Textbox(
            label="What topic would you like to research?", 
            placeholder="e.g., What are the latest developments in quantum computing?",
            lines=2
        )
    
    start_research_btn = gr.Button("Start Research", variant="primary")
    
    with gr.Row(visible=False) as followup_display:
        questions_display = gr.Markdown(label="Follow up questions", value="")
    
    with gr.Column(visible=False) as answer_section:
        gr.Markdown("### Answer the Questions")
        with gr.Row():
            answer1 = gr.Textbox(label="Answer to Question 1", lines=2)
            answer2 = gr.Textbox(label="Answer to Question 2", lines=2)
            answer3 = gr.Textbox(label="Answer to Question 3", lines=2)
    
    final_research_btn = gr.Button("Start Research with Clarifications", variant="primary", visible=False)
    report = gr.Markdown(label="Research Report")
    
    state = gr.State(value={"questions": [], "query": ""})
    

    start_research_btn.click(
        fn=handle_follow_up,
        inputs=[query_textbox, state],
        outputs=[questions_display, followup_display, answer_section, final_research_btn, state]
    )
    
    final_research_btn.click(
        fn=run_research,  # Async generator function that yields output chunks
        inputs=[answer1, answer2, answer3, state],  # Get values from answer textboxes
        outputs=report  # Stream output to report markdown component
    )
    

ui.launch(inbrowser=True)


###My tasks###
# 1) Copy over code into my environment and run it
# 2) Start by coming up with 3 clarifying questions based on the query
# 3) Tune the searches taking into account the clarifications
# 4) Make the Manager an Agent with agents-as-tools and handoffs
    #4.a
    # The hardest part of this is transforming the manager from a simple Python script — essentially
    # a sequence of function calls — into something that is genuinely agentic.

    # We should take inspiration from what we worked on earlier this week, particularly the patterns
    # where agents are treated as tools and where we have explicit handoffs between agents. 
    # Those ideas should be incorporated into the deep research flow so the system has more autonomy.

    # Specifically, the deep research agent should be able to decide for itself whether it needs to
    # perform additional searches. 
    # You may want to impose a cap or add controls, but the goal is to give it the freedom to explore, 
    # refine its queries based on what it has learned so far, and iterate.

    # One possible direction is to introduce evaluator–optimizer design patterns, where a separate agent
    # is responsible for reviewing or critiquing the work of the deep research agent.

    # All of these patterns are worth exploring, but the most important piece is the autonomous manager. 
    # We want it to drive more work, more analysis, and deeper reasoning, so that the system can spend 
    # several minutes operating and then return with something substantially more comprehensive and 
    # compelling — something that clearly adds significant value.

    # That’s the challenge. I’m very interested to see what you come back with.
    
