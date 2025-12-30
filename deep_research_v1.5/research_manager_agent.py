from agents import Agent
from tool_agents import planner_agent, search_agent, draft_report_agent

INSTRUCTIONS="""
You are an Advanced Research Manager. You are tasked with recieving a USER_QUERY in which you are 
to perform some deep research to generate a solution.
You are not going to perform the research yourself, you will use your tools you have available to carry out the research
and produce a final draft.

**Your core workflow is as follows**:
1) call your plan_research_searches tool to create a list of searches based on the USER_QUERY
2) call your perform_web_search tool to perform searches for each search term that is returned by the planner
3) call your generate_draft_report tool to generate an initial draft report

IMPORTANT CONSIDERATIONS:
- follow your workflow exactly in the order outlined above
- You may be given previous reports you have writen with some EVALUATON_FEEDBACK written by an evaluator agent. 
  If this is given then make sure to add/append this feedback into your core workflow considerations

**CRITICAL: When EVALUATION_FEEDBACK is provided, you MUST pass it to ALL your tools:**
- When calling plan_research_searches: Include the EVALUATION_FEEDBACK so the planner can adjust search strategy
- When calling perform_web_search: Include the EVALUATION_FEEDBACK so searches focus on addressing gaps
- When calling generate_draft_report: Include the EVALUATION_FEEDBACK so the draft addresses all feedback points

The feedback should be included in the input/arguments you pass to each tool call.

Output:
The generate_draft_report tool will return ReportData object which contains a draft_report string field
"""

##convert agents to tools

planner_tool = planner_agent.as_tool(
    tool_name="plan_research_searches",
    tool_description="Create a research plan with search queries based on the USER_QUERY. If EVALUATION_FEEDBACK is provided, use it to adjust the search strategy to address gaps or issues. Returns a list of search terms to investigate."
)

search_tool = search_agent.as_tool(
    tool_name="perform_web_search",
    tool_description="Perform a web search for a given search term and return a concise summary (2-3 paragraphs, <300 words). If EVALUATION_FEEDBACK is provided, focus the search on addressing specific gaps or issues mentioned in the feedback. Use this for each search query from the planner."
)

draft_report_tool = draft_report_agent.as_tool(
    tool_name="generate_draft_report",
    tool_description="Generate a comprehensive draft research report (5-10 pages, 1000+ words) based on the original query and collected search summaries. If EVALUATION_FEEDBACK is provided, you MUST explicitly address each point in the feedback. Returns a ReportData object with the draft report."
)

tools = [planner_tool, search_tool, draft_report_tool]

manager_agent = Agent(
    name="ResearchManager",
    instructions=INSTRUCTIONS,
    model="gpt-4.1-mini",
    tools=tools,
)
