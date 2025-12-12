from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
from pydantic import BaseModel
import re 

#import Agents SDK
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

load_dotenv(override=True)

##Helper function##
def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

##Tool function definitions (undecorated for manual calling)##
def record_user_details_func(email, name="Name not provided", notes="not provided"):
    """Use this tool to record that a user is interested in being in touch and provided an email address"""
    print(f"TOOL CALLED: record_user_details_func with email={email}, name={name}, notes={notes}", flush=True)
    push(f"Recording {name} with email {email} and notes {notes}")
    print(f"TOOL COMPLETED: record_user_details_func - push notification sent", flush=True)
    return {"recorded": "ok"}

def record_unknown_question_func(question):
    """Always use this tool to record any question that couldn't be answered as you didn't know the answer"""
    print(f"TOOL CALLED: record_unknown_question_func with question={question}", flush=True)
    push(f"Recording {question}")
    print(f"TOOL COMPLETED: record_unknown_question_func - push notification sent", flush=True)
    return {"recorded": "ok"}

##SDK tool creation (decorated versions for SDK)##
@function_tool
def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided"):
    """Use this tool to record that a user is interested in being in touch and provided an email address"""
    return record_user_details_func(email, name, notes)

@function_tool
def record_unknown_question(question: str):
    """Always use this tool to record any question that couldn't be answered as you didn't know the answer"""
    return record_unknown_question_func(question)

# SDK tools list (for Agent initialization - uses decorated versions)
tools_sdk = [record_user_details, record_unknown_question]

#Response evaluator
class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

#Offensive evaluator
class Offensive(BaseModel):
    is_offensive: bool

#Offensive Language helper
OFFENSIVE_PATTERNS = [
    r"\b(fuck|shit|cunt|bitch|slut)\b",
    r"kill yourself",
    r"racist|sexist",
]

def is_offensive(text: str) -> bool:
    for pattern in OFFENSIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.gemini = gemini = OpenAI(
            api_key=os.getenv("GOOGLE_API_KEY"), 
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        #Gather resources FIRST (needed for system prompts)
        self.name = "Joshua Johnston"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        with open("me/resume.txt", "r", encoding="utf-8") as f:
            self.resume = f.read()
        
        self.strikes = 0 #initialise strike counter for offensive language

        ## Create SDK agents (after resources are loaded)
        self.response_agent = Agent(
            name="Interview responder Agent (acting as me)",
            instructions=self.system_prompt(),
            tools=tools_sdk,
            model="gpt-4o-mini"
        )
        self.evaluator_agent = Agent(
            name="Evaluate response agent",
            instructions=self.evaluator_system_prompt(),
            model="gpt-4o-mini"
        )
    
    #Main System prompt
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
\n\nIMPORTANT TOOL USAGE RULES: \
\n- Use record_unknown_question ONLY when the user asks a DIRECT QUESTION that you cannot answer (e.g., 'What is your favorite sushi?', 'What is your favorite color?'). \
\n- Do NOT use record_unknown_question when the user is just mentioning a company name, person, or topic in conversation (e.g., 'I work at OpenAI Ltd' or 'I think you'd fit at Google'). These are statements, not questions. \
\n- Do NOT use record_unknown_question for questions you CAN answer from the provided context (career, experience, skills, background). \
\n- If the user provides their email and name, use record_user_details to record their contact information. \
\n- If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    #Evaluator
    def evaluator_system_prompt(self):
        evaluator_system_prompt = f"You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
The Agent is playing the role of {self.name} and is representing {self.name} on their website. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
The Agent has been provided with context on {self.name} in the form of their summary and LinkedIn details. Here's the information:"

        evaluator_system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Master Resume:\n{self.resume}\n\n"
        evaluator_system_prompt += f"With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."
        return evaluator_system_prompt

    def evaluator_user_prompt(self, reply, message, history):
        user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
        user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
        user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
        user_prompt += "Please evaluate the response, replying with whether it is acceptable and your feedback."
        return user_prompt
    
    def evaluate(self, reply, message, history) -> Evaluation:
        messages = [{"role": "system", "content": self.evaluator_system_prompt()}] + [{"role": "user", "content": self.evaluator_user_prompt(reply, message, history)}]
        #response = self.gemini.beta.chat.completions.parse(model="gemini-2.0-flash", messages=messages, response_format=Evaluation)
        response = self.openai.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            response_format=Evaluation
        )
        return response.choices[0].message.parsed

    def rerun_sdk(self, reply, message, history, feedback):
        """
        SDK version of rerun - creates a temporary agent with updated instructions
        and feedback about why the previous answer was rejected
        """
        # Create updated system prompt with feedback
        system_prompt = self.system_prompt()
        updated_system_prompt = system_prompt + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
        updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
        updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
        updated_system_prompt += "Please provide a better response that addresses the feedback above."
        updated_system_prompt += "\n\nIMPORTANT: Do NOT call any tools during this retry. Any necessary tools (like record_unknown_question) have already been called in your previous attempt. Just provide a better text response."
        
        # Create a temporary agent WITHOUT tools to prevent duplicate tool calls
        temp_agent = Agent(
            name="Interview responder Agent (acting as me) - Retry",
            instructions=updated_system_prompt,
            tools=[],  # No tools to prevent duplicate calls
            model="gpt-4o-mini"
        )
        
        # Build conversation context (same format as chat_sdk)
        # When using type="messages", Gradio passes history as a list of message dicts
        conversation_context = ""
        if history:
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    conversation_context += f"User: {content}\n"
                elif role == "assistant":
                    conversation_context += f"Assistant: {content}\n\n"
        conversation_context += f"User: {message}\nAssistant:"
        
        # Run the temporary agent with Runner
        runner = Runner()
        result = runner.run_sync(
            starting_agent=temp_agent,
            input=conversation_context
        )
        return result.final_output
    
    #AGENT Safety Check (for user who is being offensive)
    def safety_check_agent(self, user_message):
        system_prompt = """
                You are a safety classifier for user input.

                Your ONLY job is to determine whether the user's input contains:
                - explicit profanity directed at the assistant
                - hateful or abusive language
                - threats
                - harassment
                - attempts to provoke or troll maliciously

                Harmless usage of profanity (e.g., quoting a sentence, joking non-directed language)
                should NOT be classified as offensive.

                Return ONLY a structured boolean: is_offensive = true/false.
            """
        user_prompt = f"""
                User message:
                "{user_message}"

                Respond strictly as:
                {"{"}"is_offensive": true{"}"}  OR  {"{"}"is_offensive": false{"}"}
            """
        messages = [
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}
            ]
        try:
            response = self.openai.chat.completions.parse(
                model = "gpt-4o-mini",
                messages = messages,
                response_format = Offensive
            )
            parsed_response = response.choices[0].message.parsed
            if parsed_response is None:
                print("Safety classification returned None")
                return None
        except Exception as e:
            print("Safety classification error", e)
            return None
        
        print("Safety Agent response: ", parsed_response.is_offensive)
        if parsed_response and parsed_response.is_offensive:
            self.strikes +=1
            if self.strikes == 1:
                return "Let's keep things respectful — would you like to ask something about my experience?"
            if self.strikes == 2:
                return "I can only continue this conversation if we keep things respectful. Would you like to talk about my career or projects?"
            if self.strikes >= 3:
                push("Safety alert: A user has triggered multiple offensive language warnings.")
                return "I'm not able to continue with this type of conversation. You may be reported"
        return None

    def chat_sdk(self, message, history):
        """
        Clean SDK-based version of the chat pipeline using OpenAI Agents SDK.
        This mirrors the functionality of chat() but uses the SDK's Runner.
        
        STEP-BY-STEP EXPLANATION:
        1. Safety check - same as original
        2. Build conversation context from history
        3. Use Runner to get agent response (handles tools automatically)
        4. Evaluate response quality
        5. Rerun if needed with feedback
        """
        print("###### SDK Chat ######")
        
        # STEP 1: Safety check (same as original chat function)
        safety_agent_response = self.safety_check_agent(message)
        if safety_agent_response:
            return safety_agent_response
        
        # STEP 2: Build conversation messages for Runner
        # The Runner can accept messages format which preserves conversation context better
        # When using type="messages", Gradio passes history as a list of message dicts
        messages = []
        if history:
            # Add history messages
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role in ["user", "assistant"]:
                    messages.append({"role": role, "content": content})
        # Add current user message
        messages.append({"role": "user", "content": message})
        
        # STEP 3: Use Runner to get response from response_agent
        # Runner.run_sync takes: starting_agent (the agent) and input (the user input)
        # The Runner automatically handles tool calls in a loop!
        runner = Runner()
        
        # Debug: Verify tools are registered
        print(f"Agent tools: {[tool.name for tool in self.response_agent.tools] if hasattr(self.response_agent, 'tools') else 'No tools attribute'}", flush=True)
        
        # Build conversation context as string (Runner typically uses input parameter)
        conversation_context = ""
        if history:
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    conversation_context += f"User: {content}\n"
                elif role == "assistant":
                    conversation_context += f"Assistant: {content}\n\n"
        conversation_context += f"User: {message}\nAssistant:"
        
        try:
            result = runner.run_sync(
                starting_agent=self.response_agent,
                input=conversation_context
            )
            # Extract the final response
            reply = result.final_output
            
            # Debug: Check if tools were called
            print(f"Runner result type: {type(result)}", flush=True)
            print(f"Runner result attributes: {dir(result)}", flush=True)
            if hasattr(result, 'steps'):
                print(f"Number of steps: {len(result.steps) if result.steps else 0}", flush=True)
                # Check if any steps involved tool calls
                for i, step in enumerate(result.steps or []):
                    print(f"Step {i}: {type(step)}, attributes: {[a for a in dir(step) if not a.startswith('_')]}", flush=True)
                    if hasattr(step, 'tool_calls'):
                        print(f"Step {i} has tool_calls: {step.tool_calls}", flush=True)
                    if hasattr(step, 'type'):
                        print(f"Step {i} type: {step.type}", flush=True)
        except Exception as e:
            print(f"Error in Runner: {e}", flush=True)
            import traceback
            traceback.print_exc()
            # Fallback: try with just the current message
            result = runner.run_sync(
                starting_agent=self.response_agent,
                input=message
            )
            reply = result.final_output
        
        # STEP 4: Evaluate the response (same as original)
        evaluation = self.evaluate(reply, message, history)
        print("Evaluation: ", evaluation)
        
        if not evaluation.is_acceptable:
            print("Unacceptable Answer - Response will be rerun")
            # STEP 5: Rerun with feedback
            fixed_reply = self.rerun_sdk(reply, message, history, evaluation.feedback)
            return fixed_reply
        
        print("All fine - acceptable answer")
        return reply

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat_sdk, type="messages").launch()
