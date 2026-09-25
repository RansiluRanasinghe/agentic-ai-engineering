import asyncio
import sys

from shared.config import Config
from shared.groq_client import get_async_client
from .parser import parse_llm_output
from .tool import safe_calculate

SYSTEM_PROMPT = """You are a deterministic, logical AI agent capable of executing mathematical calculations.

AVAILABLE TOOLS:
- calculate[<expression>]: Safely evaluates a mathematical expression (e.g., calculate[15 * 4]).

STRICT GRAMMAR CONTRACT:
You must process tasks through an iterative loop of Thought, Action, and Observation.
Your response MUST contain exactly ONE step at a time and strictly match one of the two formats below.
Do not add markdown code fences, conversational filler, or extra formatting.

CRITICAL EXECUTION RULES:
1. NEVER generate the "Observation:" line yourself under any circumstances. Observations are provided exclusively by the system runtime.
2. When you output an "Action:", you must STOP generating immediately. Do not anticipate, predict, or simulate what the tool will return.
3. If no further calculations are required, proceed directly to FORMAT 2.

FORMAT 1 - WHEN YOU NEED TO USE A TOOL:
Thought: <reasoning about what single mathematical step to take next>
Action: calculate[<valid math expression>]

FORMAT 2 - WHEN YOU HAVE THE FINAL ANSWER:
Thought: <reasoning that the problem is fully solved>
Final Answer: <the computed final result>

MULTI-TURN EXECUTION TRACE:
User: What is 15 * 4, and then add 20?
Assistant:
Thought: I need to multiply 15 by 4 first.
Action: calculate[15 * 4]
[System provides Observation: 60]
Assistant:
Thought: Now I need to add 20 to the previous result of 60.
Action: calculate[60 + 20]
[System provides Observation: 80]
Assistant:
Thought: The math is complete.
Final Answer: 80
"""

async def run_agent(user_query: str, max_steps: int = 5) -> str:
    """
    Executes the ReAct Finite State Machine.
    Controls the state transitions between the LLM inference, parsing, and tool execution.
    """

    client = get_async_client()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    print(f"\n[SYSTEM] Starting Agent Loop for Query: '{user_query}'\n" + "-"*50)

    for step in range(1, max_steps + 1):
        print(f"\n--- Step {step}/{max_steps} ---")

        try:
            response = await client.chat.completions.create(
                model=Config.DEFAULT_MODEL,
                messages=messages,
                temperature=Config.TEMPERATURE,
                stop = ["Observation:", "\nObservation:"]
            )

            llm_text = response.choices[0].message.content
            print(f"\n[MODEL OUTPUT]\n{llm_text}\n")

            messages.append({
                "role": "assistant",
                "content": f"[System provides Observation: {observation}]"
                })

        except Exception as e:
            return f"CRITICAL: Inference failure: {str(e)}"

        parsed_state = parse_llm_output(llm_text)

        if parsed_state["type"] == "final":
            print("="*50)
            return parsed_state["content"]

        elif parsed_state["type"] == "action":
            tool_name = parsed_state["tool"]
            tool_arg = parsed_state["arg"]

            if tool_name == "calculate":
                result = safe_calculate(tool_arg)
                observation = f"{result}"
            else:
                observation = f"Error: Unknown tool '{tool_name}'."

            print(f"[TOOL EXECUTION] {tool_name}[{tool_arg}] -> {observation}")

            messages.append({"role": "user", "content": f"Observation: {observation}"})

        elif parsed_state["type"] == "error":
           print("[SYNTAX ERROR] Model hallucinated formatting. Triggering self-correction.")
           error_msg = "[System provides Observation: Error: Invalid format. You must use 'Action: calculate[arg]' or 'Final Answer: <text>'.]"
           messages.append({"role": "user", "content": error_msg})

    raise TimeoutError(f"Agent failed to reach a Final Answer within {max_steps} steps.")

async def main():
       print("Raw Python ReAct Agent Initialized. Type 'exit' to quit.")

       while True:
           try:
               user_input = input("\nUser Query: ")
               if user_input.lower() in ['exit', 'quit']:
                   print("Exiting the agent. Goodbye!")
                   break
               if not user_input.strip():
                   print("Please enter a valid query.")
                   continue

               final_answer = await run_agent(user_input)
               print(f"\nFINAL ANSWER: {final_answer}\n")

           except TimeoutError as e:
               print(f"\nTIMEOUT ERROR: {e}\n")
           except KeyboardInterrupt:
               print("\nShutting down gracefully...")
               break
           except Exception as e:
               print(f"\n UNEXPECTED ERROR: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())                                     