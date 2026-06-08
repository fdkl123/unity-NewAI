# Technical Architecture and Stack

## Architecture Style

Use a modular service architecture with a local-first MVP. The Orchestrator should run as a backend service that coordinates agents, tools, memory, verification, and a web UI.

## Initial Technology Choices

- **Backend**: Python 3.12 with FastAPI for orchestration APIs.
- **Agent Runtime**: Python workers with typed task contracts and per-agent tool permissions.
- **Frontend**: TypeScript with React for plan, run, memory, and verification views.
- **CLI**: Python Typer or Node-based wrapper for local repository operations.
- **Persistence**: SQLite for MVP metadata; vector store can start as local file-backed embeddings.
- **Queue**: In-process queue for MVP; upgrade path to Redis or durable workflow engine.
- **Unity Integration**: Repository scanner first; Unity Editor plugin later.
- **Verification**: Configurable commands for tests, builds, linters, static analyzers, profiler export checks, and custom scripts.
- **Observability**: Structured JSON logs, run traces, agent step timelines, and verification artifacts.

## Core Modules

- `src/bootstrapper/` — questionnaire engine, diagnosis engine, skill resolver, project brief generator, and scaffold manifest generator.
- `src/orchestrator/` — planning, decomposition, state machine, and gate policy.
- `src/runtime/` — agent execution, tool registry, permission model, retry controls.
- `src/agents/gameplay_intent_guard/` — behavior assumptions, tuning-sensitive systems, and optimization risk flags.
- `src/agents/performance_optimizer/` — Unity performance analysis and optimization planning.
- `src/context/` — context pack construction, ranking, summarization, and budget controls.
- `src/memory/` — project facts, decisions, performance patterns, and failure records.
- `src/verification/` — verification gate definitions, runners, parsers, and reports.
- `src/self_healing/` — failure diagnosis, patch strategy, and bounded retry loop.
- `src/ui/` — future web app and API client after CLI validation.

## Key Design Decisions

- Project creation starts with a confirmed brief, not direct file generation.
- Scaffold generation must be deterministic from `project-brief.md` and `scaffold-manifest.json`.
- Prefer explicit task contracts over free-form agent handoffs.
- Store run artifacts so results are auditable and reproducible.
- Keep verification independent from agent generation logic.
- Treat performance budgets as project configuration, not agent preference.
- Support dry-run and review-only modes before automated mutation.

## Unity Performance Model

The MVP should reason about:

- CPU scripting cost, especially `Update`, `FixedUpdate`, coroutines, and expensive lookups.
- GC allocation from strings, LINQ, collection creation, boxing, closures, and repeated yield instructions.
- Object lifecycle cost from `Instantiate`, `Destroy`, material instancing, and asset loading.
- Rendering cost from draw calls, SetPass calls, shader complexity, overdraw, shadows, particles, and UI Canvas rebuilds.
- Physics cost from collision matrix, raycast frequency, rigidbody counts, and trigger callbacks.
- Asset cost from texture compression, audio compression, Addressables, mesh complexity, and scene loading.
