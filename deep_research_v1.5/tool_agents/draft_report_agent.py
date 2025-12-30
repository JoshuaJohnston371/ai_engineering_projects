from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You are to gather the reasearch from the research assistant and produce a high quality draft report\n"
    "Requiremnents:\n"
    "- Return as much detail as possible"
    "- Return quality and quantity"
    "- Dont worry about formatting, communtary or metadata"
    "- (IMPORTANT) This draft will be passed on to a Final Report Writer agent so focus on getting as much detail down as possible \
        Aim for 5-10 pages of content, at least 1000 words.\n\n"
    "CRITICAL: If EVALUATION_FEEDBACK is provided about a previous report, you MUST:\n"
    "- Read and understand each point in the feedback\n"
    "- Explicitly address every issue, gap, or concern mentioned\n"
    "- Revise your approach to incorporate the feedback\n"
    "- Ensure the new draft resolves all problems identified in the evaluation" 
)


class ReportData(BaseModel):
    draft_report: str = Field(description="A draft report with high detail and minimal formatting")


draft_report_agent = Agent(  # type: ignore[call-arg]
    name="DraftWriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)