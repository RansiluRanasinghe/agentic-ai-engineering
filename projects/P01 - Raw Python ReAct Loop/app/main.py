import asyncio
import sys

from shared.config import Config
from shared.groq_client import get_async_client
from parser import parse_llm_output
from tool import safe_calculate

SYSTEM_PROMPT = """You are a deterministic, logical AI agent capable of executing mathematical calculations.

AVAILABLE TOOLS:
- calculate[<expression>]: Safely evaluates a mathematical expression. (e.g., calculate[15 * 4])

STRICT GRAMMAR CONTRACT:
You must process tasks in a loop of Thought, Action, and Observation.
Your output MUST perfectly match one of the two following formats. Do not add markdown blocks or conversational filler.

FORMAT 1 - WHEN YOU NEED TO USE A TOOL:
Thought: <reasoning about what mathematical step to take next>
Action: calculate[<valid math expression>]

FORMAT 2 - WHEN YOU HAVE THE FINAL ANSWER:
Thought: <reasoning that the problem is fully solved>
Final Answer: <the computed final result>

EXAMPLE EXECUTION:
User: What is 15 * 4, and then add 20?
Thought: I need to multiply 15 by 4 first.
Action: calculate[15 * 4]
Observation: 60
Thought: Now I need to add 20 to the previous result of 60.
Action: calculate[60 + 20]
Observation: 80
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
                temperature=Config.DEFAULT_TEMPERATURE,
            )

            llm_text = response.choices[0].message.content
            print(f"\n[MODEL OUTPUT]\n{llm_text}\n")

            messages.append({"role": "assistant", "content": llm_text})

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
           error_msg = "Observation: Error: Invalid format. You must use 'Action: tool[arg]' or 'Final Answer: <text>'."
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