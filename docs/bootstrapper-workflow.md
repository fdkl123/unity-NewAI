# AI Unity Project Bootstrapper Workflow

## Purpose

The Bootstrapper converts a rough game idea into a confirmed Unity + AI development environment. It is not a plain template generator. It is a diagnosis-first onboarding flow that asks targeted questions, recommends architecture, resolves AI skills, freezes scope, and only then creates project structure.

## Workflow

```text
Game Idea
→ Core Questionnaire
→ Conditional Follow-Up
→ Project Diagnosis
→ Skill Resolution
→ Architecture Recommendation
→ Risk Register
→ Project Brief Preview
→ User Confirmation
→ Scaffold Manifest
→ Unity + AI Project Scaffold
```

## Stage 1: Core Questionnaire

Ask only high-signal questions:

- What is the game idea in one paragraph?
- Is the game 2D, 3D, or undecided?
- What are the target platforms?
- What is the core player action?
- What is the intended first playable scope?
- What is the team size and skill profile?
- What AI help is expected: planning, code, design, performance, assets, tests, or all of these?

## Stage 2: Conditional Follow-Up

Follow-up questions depend on project type:

- Action games: combat loop, enemy count, camera, physics, animation, hit detection.
- Roguelikes: run structure, upgrades, procedural content, enemy waves, save data.
- UI-heavy games: screen count, lists, data tables, localization, save model.
- Simulation games: entity count, tick rate, pathfinding, economy systems.
- Multiplayer games: authority model, sync frequency, matchmaking, server constraints.

## Stage 3: Project Diagnosis

Output:

- Project positioning.
- Project type tags.
- First playable scope.
- Explicit non-goals.
- Technical complexity.
- Performance complexity.
- Content complexity.
- Production risk.

## Stage 4: Skill Resolution

Resolve skills as project dependencies:

- `spec` for feature specifications.
- `unity-developer` for Unity implementation.
- `unity-performance` for performance budgets and review.
- `memory-management` for object pooling, GC, and resource lifecycle.
- `testing-verification` for tests and verification gates.
- `asset-pipeline` for Addressables, import settings, compression, and content loading.
- `superpower` or equivalent advanced agent capability when the project requires broader autonomous workflows.

## Stage 5: Architecture Recommendation

Recommendations must include:

- Recommended architecture.
- Why it fits.
- What to avoid for now.
- What to revisit after the prototype.
- Confidence level.
- Evidence from user answers.

## Stage 6: Confirmation Preview

Before generating files, show:

- Project name.
- Game type.
- Target platforms.
- First playable scope.
- Explicit non-goals.
- Recommended Unity architecture.
- Required AI skills.
- Major risks.
- Files and directories to generate.

## Stage 7: Frozen Artifacts

After confirmation, generate:

- `conductor/project-brief.md`
- `conductor/ai-skills.md`
- `conductor/architecture-decision.md`
- `conductor/risk-register.md`
- `conductor/mvp-plan.md`
- `conductor/performance-budget.md`
- `scaffold-manifest.json`

## Guardrails

- Do not generate Unity files before confirmation.
- Prefer a smaller first playable over a broad MVP.
- Treat advanced architecture as opt-in, not default.
- Require approval before installing missing skills or packages.
- Preserve the frozen project brief as the source of truth.
