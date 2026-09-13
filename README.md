# agentic-ai-engineering

**Status:** 🚧 In progress — daily build log lives in `/notes`

A 14-day, progressively harder deep-dive into Agentic AI systems engineering — from raw ReAct loops built without any framework, to production-grade, multi-agent orchestration behind a real API. Every project prioritizes strict software engineering fundamentals — typed state, validated I/O, and verified execution — over rapid, unvalidated AI generation.

## Core Tech Stack

| Layer | Tools |
|---|---|
| Orchestration | LangChain, LangGraph |
| Inference | Groq API (Llama 3) |
| Backend & State | Python, Pydantic v2, FastAPI, SQLite, PostgreSQL |
| Vector Search | ChromaDB, SentenceTransformers |
| Observability | LangSmith |

## Repository Architecture

```
.
├── notes/      # Architectural diagrams, theory, and daily study takeaways
├── shared/     # Reusable backend utilities, API clients, and base Pydantic schemas
└── projects/   # Isolated daily 2-hour mini-projects
```

## Roadmap

| Day | Project | Tech Stack | Deliverable |
|---|---|---|---|
| 1 | Raw Python ReAct Loop | Python asyncio, Groq API, Regex | Build an autonomous loop from scratch without frameworks. Parse `Thought:`, `Action:`, and `Observation:` strings with regex, invoking a hardcoded mock calculator tool before returning a final answer. |
| 2 | Typed Function-Calling Agent | Groq API, Pydantic v2, Python | Implement structured outputs using Pydantic schemas. Define strict input/output models for custom tools (e.g., a system metric checker) and handle validation errors when the model outputs malformed arguments. |
| 3 | LangChain Dynamic Tool Runner | LangChain Core, Groq API, DuckDuckGo Search | Construct a LangChain agent using the `@tool` decorator. Implement a multi-tool agent that queries real-time web data and local file structures, returning validated Pydantic models. |
| 4 | Hybrid Local RAG CLI | ChromaDB, all-MiniLM-L6-v2, LangChain | Load local Markdown or text documents, chunk them via `RecursiveCharacterTextSplitter`, store embeddings locally in ChromaDB, and execute similarity search with metadata filtering via CLI. |
| 5 | Self-Correcting Retrieval Pipeline | LangChain, ChromaDB, LangSmith | Build a retrieval chain that grades retrieved document relevance using an LLM. If the score falls below a threshold, automatically rewrite the query and retry. Trace every step in LangSmith. |
| 6 | LangGraph State Machine | LangGraph, Pydantic, Groq API | Build a basic cyclic graph using `TypedDict` and Pydantic state schemas. Define nodes that intake a user request, classify its intent (Support vs. Sales), and route it down deterministic graph edges. |
| 7 | Human-in-the-Loop Approval Gate | LangGraph, Python `input()` | Implement graph interrupts (`interrupt_before`). Build a code-generation node that drafts a shell command, pauses the graph state, prompts the user in the terminal to [A]pprove or [E]dit, and executes only on confirmation. |
| 8 | Self-Reflective Code Improver | LangGraph, Python subprocess | Design a two-node cyclical sub-graph: Node A writes a Python function; Node B attempts to execute it in an isolated subprocess. If a `CalledProcessError` occurs, the traceback is passed back to Node A to self-repair (max 3 loops). |
| 9 | Persistent Chat Session with SQLite | LangGraph, SqliteSaver | Wire LangGraph's checkpointer to a local `sqlite3` database file. Assign distinct `thread_id` keys to simulate multiple users; verify that terminating and restarting the Python process preserves state history. |
| 10 | Cross-Session Memory Profile Store | LangGraph Store, Groq API | Implement semantic memory across multiple threads. Create a background node that extracts persistent user facts (e.g., technical preferences, constraints) from dialogue and writes them to LangGraph's long-term memory store. |
| 11 | Supervisor-Worker Orchestrator | LangGraph, Groq API | Create a central supervisor node that decomposes a user prompt and delegates tasks to two worker nodes: a Technical Researcher and a Technical Writer. Workers return findings to the supervisor for final aggregation. |
| 12 | Multi-Agent Debate & Consensus | LangGraph, Groq API | Construct a collaborative multi-agent debate between an "Optimistic Architect" node and a "Security Hardener" node. They pass state back and forth for exactly two rounds before a "Tech Lead" node outputs a balanced final design. |
| 13 | Capstone: FastAPI Multi-Agent Engine | FastAPI, LangGraph, SQLite, LangSmith | Wrap the Day 11 supervisor architecture in an async FastAPI service. Expose `/chat` and `/feedback` endpoints supporting background thread execution, persistent checkpoints, and full LangSmith distributed tracing. |
| 14 | Capstone: Containerization & CI Verification | Docker, GitHub Actions, Pytest | Write unit tests verifying graph routing states and Pydantic outputs. Package the FastAPI agent into a multi-stage Dockerfile and configure a local GitHub Actions workflow that lints and runs tests on push. |

## Development Workflow

This project strictly follows feature-branch isolation:

- Every daily project is developed on a `feat/day-XX` branch
- Work is committed atomically, per feature addition
- Branches are merged into `main` via pull request, only after passing local validation

## Getting Started

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
