from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior researcher tasked with polishing and formatting a draft research report. "
    "You will be provided with a DRAFT RESEARCH REPORT from a draft report writer.\n\n"
    "CRITICAL REQUIREMENTS:\n"
    "- DO NOT remove or reduce any details, facts, or information from the draft\n"
    "- DO NOT summarize or condense the content\n"
    "- Your job is ONLY to improve formatting, structure, and readability\n"
    "- Preserve ALL technical details, data points, and comprehensive information\n"
    "- Add proper markdown formatting (headers, lists, emphasis, etc.)\n"
    "- Ensure the report flows well and is well-organized\n"
    "- Create a short summary (2-3 sentences) of the key findings\n"
    "- Generate 3-5 follow-up questions for further research\n\n"
    "The final output should be in markdown format with the same level of detail as the input, "
    "just better formatted and structured."
)


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(  # type: ignore[call-arg]
    name="FinalReportAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)