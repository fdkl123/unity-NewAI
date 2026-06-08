# MVP Backlog

## P0: Project Ingestion

- Detect Unity project structure from repository root.
- Read `ProjectSettings/ProjectVersion.txt`, `Packages/manifest.json`, `Assets/**/*.cs`, and test folders.
- Discover and summarize planning/design documents such as `README`, `Docs`, `Design`, `策划`, `需求`, markdown, text, and spreadsheet exports when present.
- Infer project type such as 2D, 3D, mobile, PC, action, RPG, simulation, idle, roguelike, multiplayer, or tool project from engineering and planning evidence.
- Predict suitable technical architecture candidates such as MonoBehaviour service architecture, ScriptableObject data-driven design, Addressables, object pooling, event bus, ECS/DOTS, or hybrid architecture.
- Generate early risk hypotheses and likely mitigation paths before deeper analysis.
- Infer render pipeline, target platforms, packages, and available verification commands.
- Produce a project summary artifact.

## P0: Run Orchestration

- Create run IDs and persist run state.
- Support first-stage run modes: `review_only` and `propose_patch`.
- Decompose a performance objective into typed tasks.
- Track task status, agent status, retries, and evidence paths.

## P0: Gameplay-Intent Guard

- Extract expected behavior from scripts, scene naming, comments, and user notes.
- Identify tuning-sensitive systems such as spawning, physics, animation, camera, and UI feedback.
- Flag optimization proposals that may alter gameplay timing, collision behavior, visual feedback, or difficulty.
- Require manual approval for behavior-changing optimizations.

## P0: Performance Optimizer Agent

- Detect `GetComponent`, `Find`, and `transform` hot-path patterns.
- Detect per-frame allocations from strings, collections, LINQ, closures, and yield instructions.
- Detect `Instantiate` and `Destroy` in gameplay loops.
- Detect physics hot paths such as uncached layer masks and excessive raycasts.
- Prioritize findings by likely runtime impact and fix confidence.

## P0: Verification Pipeline

- Define verification gate config schema.
- Run shell commands with captured stdout, stderr, exit code, duration, and artifact path.
- Parse known result types into structured gate outcomes.
- Block acceptance on required gate failures.

## P0: Self-Healing

- Diagnose failed gates from parsed output.
- Decide retry eligibility using risk policy.
- Generate one narrow repair task per attempt.
- Stop after 3 attempts or unsafe diagnosis.

## P1: Memory System

- Store project facts, decisions, findings, and failures.
- Retrieve similar prior findings during new runs.
- Record successful optimization patterns.
- Expose memory records through CLI or API.

## P1: CLI Demo Flow

- `scan-project`
- `performance-review`
- `verify`
- `run-demo`

## P2: UI/UX Baseline

- Show run timeline.
- Show current agent and task status.
- Show findings with severity and evidence.
- Show verification gates and retry attempts.
- Show approval prompts for high-risk actions.

## P2: Game Design Expansion

- Convert design prompt into mechanic spec.
- Identify affected systems and required assets.
- Generate implementation tasks and acceptance criteria.
- Flag design risks such as scope creep, unclear tuning variables, or missing feedback loops.

## P2: Unity Editor Plugin

- Capture profiler exports.
- Trigger Orchestrator runs from Unity.
- Display findings in an editor window.
- Link findings back to source files and scenes.

## MVP Definition of Done

- Demo scenario runs end-to-end on a seeded Unity fixture.
- P0 backlog is implemented or explicitly deferred with rationale.
- At least four static performance anti-pattern categories are detected.
- `apply_patch` is not required for first-stage MVP; patch proposals are enough.
- Every run emits an auditable final artifact.
- Verification and self-healing behavior is visible in run history.
