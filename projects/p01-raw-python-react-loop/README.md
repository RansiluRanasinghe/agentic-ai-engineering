# Raw Python ReAct Loop

A from-scratch ReAct (Reasoning + Acting) agent loop built in pure Python — no agent framework involved.

## Objective

Before adopting high-level frameworks like LangChain or LangGraph, it's critical to understand the underlying mechanics of an AI agent. This project builds a ReAct loop entirely from scratch, enforcing robust software engineering fundamentals and structural code verification.

By manually parsing `Thought:`, `Action:`, and `Observation:` strings using regular expressions, this implementation exposes exactly how an LLM interacts with external tools in a deterministic loop.

## Architecture

The script operates in a continuous asynchronous `while` loop:

1. **System Prompt** — Instructs the LLM to output a strict text format.
2. **Thought** — The model reasons about the current state of the problem.
3. **Action** — The model requests a tool call (e.g., `calculate: 45 * 12`).
4. **Execution & Regex** — The Python backend intercepts the response, uses regex to extract the action, and executes a hardcoded local Python function (the mock tool).
5. **Observation** — The backend injects the function's return value back into the prompt history as an "Observation".
6. **Final Answer** — The loop repeats until the model outputs the final computed string.

## Tech Stack

- **Language:** Python 3.10+ (`asyncio`)
- **LLM Provider:** Groq API (`llama-3-70b-8192` or `llama-3-8b-8192`)
- **Parsing:** Python's native `re` module

## Setup & Execution

1. Ensure your virtual environment is active from the repository root.
2. Export your Groq API key:

   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```

3. Run the agent:

   ```bash
   python main.py
   ```

## Verification & Testing

To confirm the parsing logic handles edge cases correctly, verify the following during execution:

- [ ] The regex parser correctly isolates the exact arithmetic expression without capturing trailing spaces or punctuation.
- [ ] The LLM gracefully handles an `Observation: Error` if it attempts an invalid mathematical operation (e.g., division by zero).
- [ ] The loop terminates successfully once a `Final Answer:` token is generated, preventing infinite API looping.

## Example Execution Trace

```
User: What is 25 multiplied by 4, and then add 15 to the result?

Thought: I need to calculate 25 * 4 first.
Action: calculate[25 * 4]
Observation: 100

Thought: Now I need to add 15 to the previous result (100).
Action: calculate[100 + 15]
Observation: 115

Final Answer: The final result is 115.
```