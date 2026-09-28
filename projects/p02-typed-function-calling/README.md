\# Typed Function-Calling Agent



A tool-using agent that replaces brittle, regex-based text parsing with native API function calling, using Pydantic v2 as a strict validation gatekeeper for every tool call.



\## Overview



Instead of relying on the LLM to produce correctly formatted conversational text, this project forces the model to emit structured JSON arguments. Pydantic models validate that output before anything runs. If the LLM hallucinates an argument or uses the wrong data type, Pydantic raises a `ValidationError`, and the FSM loop feeds that exact error back to the model so it can correct itself autonomously.



\## Core Architecture



1\. \*\*Pydantic v2 Schemas:\*\* Tool arguments are defined as Python classes (`BaseModel`), which automatically generate the JSON schema required by the Groq API.

2\. \*\*Native Tool Calling:\*\* The `tools` and `tool\_choice` parameters of the Groq SDK offload parsing complexity to the API layer.

3\. \*\*Gatekeeper Pattern:\*\* No tool executes unless its inputs pass `Model.model\_validate\_json()`.

4\. \*\*Autonomous Self-Healing:\*\* Validation errors are caught and injected into the model's context, allowing it to recognize its mistake and retry without crashing the Python runtime.



\## Tool: System Metric Checker



The agent is equipped with a custom infrastructure tool that safely mocks system metrics.



\- \*\*Input Schema:\*\* Expects a specific `module` (e.g., `cpu`, `memory`, `disk`) and a `detailed` boolean flag.

\- \*\*Failure Scenarios:\*\* If the user asks for `network` metrics, or the LLM passes `"detailed": "yes"` (a string instead of a boolean), Pydantic blocks execution and forces the agent to correct the call.



\## Directory Structure



```text

projects/p02-typed-function-calling/

├── README.md

└── app/

&#x20;   ├── \_\_init\_\_.py

&#x20;   ├── main.py      # FSM loop handling Groq's tool\_call payloads

&#x20;   ├── schema.py    # Pydantic v2 BaseModels for strict type definitions

&#x20;   └── tool.py      # System metric checker execution logic

```



\## Running the Agent



From the monorepo root, with your virtual environment active:



```bash

python -m projects.p02-typed-function-calling.app.main

```



\## Key Learning Outcomes



\- Mapping Python classes to JSON Schemas dynamically

\- Processing `tool\_calls` and `tool\_call\_id` in API responses

\- Handling Pydantic `ValidationError` traces as conversational feedback

