from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = """You are a helpful assistant that clarifies the user's query.
You will be provided with a query and you should return exactly 3 clarifying questions.
The clarifying questions should be specific to the query and should help understand what aspects 
of the topic the user wants to research. Focus on:
- Specific time periods or dates
- Geographic regions or locations
- Particular aspects or angles
- Target audience or use case
- Depth of detail needed
"""


class ClarifyingQuestions(BaseModel):
    questions: list[str] = Field(
        description="A list of exactly 3 clarifying questions to help refine the research query."
    )


clarifier_agent = Agent(
    name="Query Clarifier Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ClarifyingQuestions,
)

