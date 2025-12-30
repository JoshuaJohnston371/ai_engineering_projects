from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field
from agents import Agent

class Evaluation(BaseModel):
    accepted: bool = Field(description="Meets requirements (true) or not (false)")
    score: float = Field(ge=0.0, le=1.0, description="Overall quality score in [0,1]")
    feedback: str = Field(description="Actionable feedback to improve the draft")
    reasons: List[str] = Field(default_factory=list, description="Short bullet reasons")

evaluator_agent = Agent(
    name="LLM Evaluator",
    model="gpt-4.1",
    output_type=Evaluation,
    instructions=(
        "You are a strict evaluator.\n"
        "Given USER_QUERY, and a DRAFT REPORT SOLUTION:\n"
        "- If ANY requirement is unmet: accepted=false.\n"
        "- Provide a score in [0,1].\n"
        "- Provide specific, actionable feedback.\n"
        "- List concise reasons as bullets.\n"
        "Be tough but fair."
    ),
)