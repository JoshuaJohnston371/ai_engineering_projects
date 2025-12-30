from pydantic import BaseModel, Field
from agents import Agent

HOW_MANY_SEARCHES = 5

#Original
INSTRUCTIONS = f"""You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for.

If EVALUATION_FEEDBACK is provided about a previous report, use it to inform your search strategy:
- Identify gaps or issues mentioned in the feedback
- Create searches that will help address those specific concerns
- Adjust your search terms to target areas that were insufficiently covered
- Consider searches that will provide more depth or different perspectives on weak areas"""

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")

#Original
planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)