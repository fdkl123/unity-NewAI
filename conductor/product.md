# Product Context

## Product Name

AI Engineering Orchestrator for Unity Games

## One-Line Description

An agentic engineering system that helps users start Unity projects correctly, then continuously detects, explains, verifies, and safely fixes Unity performance problems while preserving gameplay intent.

## Product Positioning

The product sits between Unity creators, Unity engineers, technical designers, and automated coding agents. It does not replace the Unity Editor or source control. The first-stage product behaves like an AI technical lead during project creation: it asks the right questions, diagnoses scope and risk, resolves required AI skills, recommends architecture, freezes a project brief, and prepares an AI-readable Unity scaffold.

## Core Problem

Game teams lose time because project intent, scope, architecture, AI skills, performance budgets, and verification practices are decided informally or too late. AI coding tools can write code, but they often start without a frozen brief, Unity-specific architecture judgment, persistent project context, reproducible verification, or bounded recovery when changes fail.

## Target Users

- Solo creators who need help turning a rough idea into a scoped Unity project.
- Unity gameplay engineers who want performance-aware code review and patch proposals.
- Indie game teams that need senior-engineering leverage without a dedicated optimization team.
- Studio engineering leads who need consistent optimization standards across projects.
- Technical designers who need optimization work to preserve gameplay intent and tuning constraints.

## MVP Scope

### First-Stage MVP In Scope

- Interactive project questionnaire for new Unity projects.
- Project diagnosis for type, target platform, first playable scope, risks, and architecture candidates.
- AI skill resolution with installed, missing, optional, and recommended skill states.
- Frozen project brief generation before scaffold generation.
- Scaffold manifest generation for deterministic project initialization.
- Unity project ingestion from repository files, settings, scripts, planning documents, and optional profiler exports.
- Performance optimizer agent that flags Unity-specific CPU, memory, rendering, physics, and GC risks.
- Narrow gameplay-intent capture so optimization proposals do not break behavior.
- Context engineering layer that builds compact, task-specific context packs.
- Memory system for decisions, project facts, optimization patterns, and prior failures.
- Verification pipeline for static checks, tests, build commands, profiler-budget checks, and report generation.

### Out of Scope for MVP

- Fully autonomous production deployment.
- Replacing Unity Editor workflows.
- Real-time in-editor co-editing.
- General-purpose game design generation.
- Automatic creation of complete game mechanics from scratch.
- Multiplayer infrastructure generation beyond review and planning.
- Marketplace, billing, and organization admin features.

## Core Capabilities

- **Project Bootstrapper**: Turns rough game ideas into confirmed project briefs, architecture decisions, skill dependencies, risks, and scaffold manifests.
- **Project Cognition Scan**: Reads engineering files and planning documents to form project intent, type, architecture, and risk hypotheses.
- **Performance Review**: Detects common Unity anti-patterns such as repeated `GetComponent`, allocations in `Update`, unbounded `Instantiate/Destroy`, expensive physics queries, and UI batching problems.
- **Optimization Plan**: Proposes measurable fixes tied to frame-time, GC, memory, rendering, or physics budgets.
- **Gameplay-Safe Review**: Captures expected behavior and tuning constraints before recommending changes.
- **Verified Change Loop**: Runs defined checks before accepting a patch or final report.
- **Project Memory**: Remembers project-specific architecture, platform targets, performance budgets, and rejected approaches.

## Success Metrics

- A user can complete guided new-project onboarding before files are generated.
- Every generated scaffold is traceable to a confirmed `project-brief.md`.
- Detect at least 80% of seeded Unity performance anti-patterns in benchmark fixtures.
- Reduce manual review time for common optimization tasks by at least 50%.
- Produce an evidence-backed optimization report for a medium Unity repository in under 5 minutes.
- Every accepted change must include verification evidence or an explicit unsupported-gate note.

## Long-Term Direction

- Unity Editor plugin integration.
- Profiler capture ingestion and regression budgets.
- Full game design agent for mechanics, content iteration, and playtest feedback loops.
- Benchmark scene generation.
- Organization-wide optimization memory.
- Multi-engine support after Unity MVP validation.
