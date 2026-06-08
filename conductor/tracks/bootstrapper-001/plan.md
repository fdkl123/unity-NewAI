# Bootstrapper Implementation Plan

## Phase 1: Questionnaire Engine

- Define first-round core questions.
- Define conditional follow-up question sets by project type.
- Persist onboarding session state for resume.
- Normalize answers into structured project signals.

## Phase 2: Diagnosis Engine

- Infer project type, target platform, gameplay system hints, and content scale.
- Estimate technical, performance, content, and production complexity.
- Recommend MVP scope and explicit non-goals.
- Generate architecture candidates with confidence and rationale.

## Phase 3: Skill Resolver

- Map project signals to required AI skills.
- Check installed skill availability when possible.
- Mark missing, optional, and recommended skills.
- Generate `ai-skills.md` and installation prompts.

## Phase 4: Confirmation and Frozen Brief

- Generate project confirmation preview.
- Require user confirmation before scaffold generation.
- Write frozen `project-brief.md`.
- Write architecture, risk, MVP, and scaffold manifest artifacts.

## Phase 5: Scaffold Generation

- Generate Unity-friendly directory structure.
- Generate conductor context files.
- Generate default verification and performance-budget files.
- Leave Unity package installation and editor operations behind explicit approval gates.
