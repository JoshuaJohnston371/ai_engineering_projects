from agents import Runner
from clarifier_agent import clarifier_agent, ClarifyingQuestions

##Query Clarifier Agent
async def get_clarifying_questions(query: str) -> ClarifyingQuestions:
    """ Generate clarifying questions for the query """
    print("Clarifying query...")
    result = await Runner.run(
        clarifier_agent,
        f"Query: {query}",
    )
    clarifying_questions = result.final_output_as(ClarifyingQuestions)
    print(f"Generated {len(clarifying_questions.questions)} clarifying questions")
    return clarifying_questions

##Building the refined query
def refine_query_with_answers(original_query: str, questions: list[str], answers: list[str]) -> str:
    """ Refine the query by incorporating the user's answers to the clarifying questions """
    # Create a refined query that includes the original query and the user's answers
    qa_pairs = "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(questions, answers)])
    refined_query = f"""{original_query}\n\n
    Based on the following clarifications:
    {qa_pairs}"""
    return refined_query