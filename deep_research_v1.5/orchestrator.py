from __future__ import annotations

from typing import Any, Dict, List
from agents import Runner, trace, gen_trace_id
from evaluator_optimizer_agent import evaluator_agent, Evaluation
from research_manager_agent import manager_agent
from final_report_agent import writer_agent, ReportData
from email_agent import email_agent

async def run_evaluator_optimizer(
    query: str,
    *,
    max_rounds: int = 4,
    min_score: float = 0.85
    ) -> Dict[str, Any]:
    """
    Manager-owned loop:
      Generator -> Evaluator -> accept/reject -> feedback -> Generator -> ...
    """

    history: List[Dict[str, Any]] = []
    draft: str = ""

    manager_prompt = f"""
    USER_QUERY: 
    {query}

    Please conduct the research and produce a high quality draft report
    """

    for round_idx in range(1, max_rounds + 1):
        print(f"## Starting Iteration {round_idx} ##")
        # 1) Generate Draft
        response = await Runner.run(manager_agent, manager_prompt)
        draft = response.final_output

        # 2) Evaluate
        eval_prompt = f"""
        USER_QUERY: 
        {query}

        DRAFT REPORT SOLUTION:
        {draft}
        """

        eval_response = await Runner.run(evaluator_agent, eval_prompt)
        evaluation = eval_response.final_output_as(Evaluation)

        history.append(
            {
                "round" : round_idx,
                "draft" : draft,
                "evaluation" : evaluation.model_dump()
            }
        )

        # 3) Accept / Reject
        print(f"Iteration decision: {evaluation.accepted}")
        print(f"Score: {evaluation.score}\n")
        print(f"Score: {evaluation.feedback}")
        if (evaluation.accepted) and (evaluation.score >= min_score):
            return {"final" : draft, "history" : history, "accepted" : True}

        # 4) Rejected, feedback into next manager_prompt
        manager_prompt = f"""
        USER_QUERY: 
        {query}

        PREVIOUS REPORT SOLUTION:
        {draft}

        EVALUATON_FEEDBACK
        {evaluation.feedback}

        Revise the solution to address the feedback explicitly.
        Please conduct the research again and produce a high quality draft report 
        which includes what is expressed in the evaluation feedback
        """

    # Max rounds exhausted
    return {"final": draft, "history": history, "accepted": False}

async def run_advanced_research(query):
    try:
        trace_id = gen_trace_id()
        with trace("Advanced Research Manager Trace", trace_id=trace_id):
            trace_url = f"https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print(f"**View trace:** {trace_url}")
            yield f"**View trace:** {trace_url}"
            print(f"**Starting research**")
            yield f"**Starting research**"
            print(f"**Research In Progress... This may take a while**")
            yield f"**Research In Progress... This may take a while**"

            try:
                result = await run_evaluator_optimizer(query=query, max_rounds=10, min_score=0.90)
            except Exception as e:
                error_msg = f"Error during research evaluation: {str(e)}"
                print(error_msg)
                yield f"**Error:** {error_msg}"
                return

            if not result or "final" not in result:
                error_msg = "Research completed but no final report was generated"
                print(error_msg)
                yield f"**Error:** {error_msg}"
                return

            print("Research Completed!")
            yield "Research Completed!"
            print("Formatting final report and sending email")
            yield "Formatting final report and sending email...\n\n"
            
            try:
                final_output_prompt = f"""
                DRAFT RESEARCH REPORT:
                {result["final"]}
                
                Please format this report, add a summary and follow-up questions.
                """
                
                final_response = await Runner.run(writer_agent, final_output_prompt)
                final_report_data = final_response.final_output_as(ReportData)
            except Exception as e:
                error_msg = f"Error formatting final report: {str(e)}"
                print(error_msg)
                yield f"**Error:** {error_msg}"
                yield f"\n\n# Research Report\n\n{result['final']}"
                return

            try:
                email_prompt = f"RESEARCH REPORT:{final_report_data.markdown_report}.\
                    Please convert to html and send email"
                
                email_response = await Runner.run(email_agent, email_prompt)
                response_contents = email_response.final_output
                
                if isinstance(response_contents, dict):
                    email_status = response_contents.get("status", "unknown")
                    email_message = response_contents.get("message", "No message")
                else:
                    email_status = "completed"
                    email_message = str(response_contents)
                
                print(f"Email Status: {email_status}")
                print(f"Message: {email_message}")
                yield f"Email Status: {email_status}"
                yield f"Message: {email_message}"
            except Exception as e:
                error_msg = f"Error sending email: {str(e)}"
                print(error_msg)
                yield f"**Warning:** {error_msg}"
            
            try:
                markdown_content = final_report_data.markdown_report
                
                follow_up_text = ""
                if final_report_data.follow_up_questions:
                    follow_up_section = "## Follow-up Questions"
                    if follow_up_section.lower() not in markdown_content.lower():
                        follow_up_text = f"\n\n## Follow-up Questions\n{chr(10).join([f'{i+1}. {q}' for i, q in enumerate(final_report_data.follow_up_questions)])}"
                
                formatted_output = f"""# Research Report

## Summary
{final_report_data.short_summary}

---

{markdown_content}

---{follow_up_text}
"""
                yield formatted_output
            except Exception as e:
                error_msg = f"Error formatting output: {str(e)}"
                print(error_msg)
                yield f"**Error:** {error_msg}"
                yield f"\n\n# Research Report\n\n{final_report_data.markdown_report}"
                
    except Exception as e:
        error_msg = f"Unexpected error in research process: {str(e)}"
        print(error_msg)
        yield f"**Fatal Error:** {error_msg}"
