# Repository Scaffold

## Planned Directories

- `src/orchestrator/` — objective handling, task decomposition, state machine, and policies.
- `src/runtime/` — agent registry, task executor, tool permissions, and retry controls.
- `src/agents/gameplay_intent_guard/` — behavior assumptions, tuning-sensitive systems, and optimization risk flags.
- `src/agents/performance_optimizer/` — Unity analyzer rules, findings, and fix planners.
- `src/context/` — repository indexing, ranking, summarization, and context packs.
- `src/memory/` — local storage adapters and memory record types.
- `src/verification/` — gates, command runners, parsers, and evidence reports.
- `src/self_healing/` — failure diagnosis, retry policy, and repair tasks.
- `src/ui/` — future web UI.
- `tests/` — schema, analyzer, runtime, and integration tests.
- `examples/` — sample Unity projects and seeded benchmark fixtures.

## First Implementation Cut

Start with backend-only local CLI before building a full web UI:

1. `unity-ai new`
2. `scan-project`
3. `performance-review`
4. `verify`
5. `run-demo`

This sequence validates core value before investing in UI complexity.

## `unity-ai new` Responsibilities

`unity-ai new` should not create a Unity project immediately. It should:

- Run the core questionnaire.
- Ask conditional follow-up questions.
- Diagnose project type, scope, risk, and architecture.
- Resolve required AI skills.
- Generate a confirmation preview.
- Write project artifacts and scaffold manifest only after confirmation.

## `scan-project` Responsibilities

`scan-project` should produce the first project cognition artifact, not just a file inventory:

- Engineering scan: Unity version, packages, scenes, scripts, assemblies, render pipeline, tests, and verification capabilities.
- Planning scan: design docs, requirements docs, roadmap docs, README files, balance tables, and exported spreadsheets when available.
- Project inference: project type, target platform hints, gameplay system hints, and likely content scale.
- Architecture prediction: current architecture hints, recommended architecture candidates, options to avoid, and confidence.
- Risk hypotheses: likely performance, production, design, architecture, and verification risks with mitigation notes.
