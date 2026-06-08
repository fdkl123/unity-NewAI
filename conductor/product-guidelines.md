# Product Guidelines

## Communication Principles

- Be concrete: every recommendation must name the affected Unity system, file, scene, metric, or risk.
- Be measurable: optimization advice should reference a target such as frame time, GC allocation, draw calls, memory, or build size.
- Be bounded: agent autonomy must include retry limits, confidence, and escalation points.
- Be implementation-oriented: design outputs should become specs, tasks, acceptance criteria, or patches.

## Preferred Terminology

- Use `Orchestrator` for the central planner and gatekeeper.
- Use `Agent Runtime` for task execution, agent scheduling, retries, and tool permissions.
- Use `Context Pack` for the task-specific compressed context passed to an agent.
- Use `Project Memory` for durable facts about one game project.
- Use `Optimization Memory` for reusable Unity performance patterns and prior fixes.
- Use `Verification Gate` for a required check before accepting output.
- Use `Self-Healing Attempt` for a bounded diagnosis-and-retry cycle.

## Agent Output Standard

Agent responses should include:

- Objective.
- Inputs used.
- Assumptions.
- Proposed changes or findings.
- Risks.
- Verification evidence.
- Next action.

## UX Principles

- Show the plan before mutation.
- Display current agent, task status, verification gate, and retry count.
- Make performance budgets visible.
- Separate design suggestions from code changes.
- Require explicit approval before high-risk changes such as deleting assets, changing project settings globally, or mass refactoring.
