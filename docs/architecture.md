# System Architecture

## Overview

The Orchestrator coordinates specialized agents around a Unity repository. In the first stage, it converts performance objectives into typed review, gameplay-risk, verification, and self-healing tasks. It builds compact context packs, executes agents with scoped permissions, verifies outputs, records memory, and optionally retries through a bounded self-healing loop.

## Major Components

### Orchestrator

Responsibilities:

- Accept user objective and project target.
- Decompose objective into typed tasks.
- Select agents and assign context packs.
- Enforce permissions, verification gates, and retry budgets.
- Merge results into a final artifact.

### Multi-Agent Runtime

Responsibilities:

- Register agents and capabilities.
- Execute agent tasks with status tracking.
- Isolate tool permissions per task.
- Persist intermediate outputs.
- Support cancellation and bounded retries.

### Context Engineering

Responsibilities:

- Index project files, Unity settings, package manifests, scripts, scenes, and documentation.
- Summarize planning and design documents into project intent, type, target platform hints, and gameplay system hints.
- Predict likely technical architecture candidates from project intent and existing engineering evidence.
- Generate early risk hypotheses and mitigation notes for downstream agents.
- Rank relevant context per task.
- Compress context into source-linked packs.
- Track what context each agent used.

### Memory System

Responsibilities:

- Store project facts such as platform targets, render pipeline, Unity version, coding conventions, and performance budgets.
- Store decisions and rejected approaches.
- Store optimization patterns and prior fixes.
- Store failure records and self-healing outcomes.

### Verification Pipeline

Responsibilities:

- Run configured gates such as tests, build checks, analyzers, profiler-budget checks, and custom scripts.
- Parse outputs into structured results.
- Block acceptance when required gates fail.
- Generate verification evidence for final reports.

### Self-Healing

Responsibilities:

- Diagnose failed gates.
- Decide whether retry is safe.
- Generate a bounded repair task.
- Stop when retry budget is exhausted or risk exceeds policy.

## Runtime Flow

1. User submits scan or performance optimization objective.
2. Orchestrator creates run ID and objective record.
3. Context layer builds project summary and task context packs.
4. Agent runtime executes selected agents.
5. Orchestrator merges findings and proposed changes.
6. Verification pipeline runs configured gates.
7. Self-healing retries failed gates when safe.
8. Memory system records facts, decisions, failures, and reusable patterns.
9. Final artifact is returned with status, evidence, and next steps.

## MVP Deployment Shape

- One local backend process.
- One local CLI; web UI remains optional after core value is validated.
- SQLite metadata database.
- File-based run artifact directory.
- Repository scanner operating on a checked-out Unity project.

## Upgrade Paths

- Replace in-process queue with durable workflow engine.
- Add Unity Editor plugin for direct profiler capture.
- Add remote workers for heavy analysis.
- Add organization memory and team policy enforcement.
- Add benchmark service for performance regression tracking.
