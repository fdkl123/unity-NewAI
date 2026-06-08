# Bootstrapper Backlog

## P0: `unity-ai new`

- Start an interactive new-project onboarding session.
- Support resume from saved session state.
- Refuse scaffold generation until confirmation.
- Emit a confirmation preview before writing files.

## P0: Questionnaire Engine

- Ask first-round core questions.
- Select conditional follow-up set by inferred project type.
- Normalize answers into project signals.
- Preserve raw answers for traceability.

## P0: Diagnosis Engine

- Infer project type tags.
- Infer target platform implications.
- Estimate technical, performance, content, and production complexity.
- Recommend first playable scope and explicit non-goals.
- Generate risk hypotheses and mitigation paths.

## P0: Skill Resolver

- Map project signals to required AI skills.
- Mark skills as `installed`, `missing`, `recommended`, or `optional`.
- Explain why each skill is needed.
- Ask for confirmation before installing missing skills.

## P0: Project Brief Generator

- Generate `conductor/project-brief.md`.
- Generate `conductor/ai-skills.md`.
- Generate `conductor/architecture-decision.md`.
- Generate `conductor/risk-register.md`.
- Generate `conductor/mvp-plan.md`.
- Generate `conductor/performance-budget.md`.

## P0: Scaffold Manifest

- Generate deterministic `scaffold-manifest.json`.
- List directories, files, Unity packages, AI skills, verification commands, and approval-required operations.
- Use the confirmed project brief as the only source of scaffold truth.

## P1: Scaffold Writer

- Create Unity-friendly directory structure.
- Create initial conductor files.
- Create default `.orchestrator` config.
- Leave Unity package installation behind explicit approval.

## P1: Template Profiles

- `2d_mobile_casual`
- `3d_mobile_action`
- `pc_prototype`
- `roguelike_arena`
- `ui_heavy_idle`

## Definition of Done

- A user can complete `unity-ai new` without writing Unity files before confirmation.
- Generated artifacts include rationale, evidence, confidence, and non-goals.
- Missing skills are clearly identified before scaffold generation.
- The scaffold manifest can be re-run deterministically from the frozen brief.
