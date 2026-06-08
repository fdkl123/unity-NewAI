# Bootstrapper Spec: AI Unity Project Bootstrapper

## Objective

Build an interactive project onboarding system that turns a user's rough game idea into a confirmed Unity + AI development project brief, recommended architecture, required AI skills, risk register, MVP plan, and scaffold manifest.

The system must ask questions before generating files. It should prevent premature scaffolding, over-scoping, and unnecessary technical complexity.

## User Stories

- As a solo creator, I can describe a game idea and be guided through only the questions needed to clarify the first playable version.
- As a Unity engineer, I can receive architecture recommendations tied to project type, target platform, performance risks, and team constraints.
- As a technical designer, I can confirm MVP scope and non-goals before the engineering structure is generated.
- As an AI-assisted team, we can record required skills, installed/missing capabilities, and AI boundaries before implementation starts.

## Functional Requirements

- Run an interactive `unity-ai new` flow.
- Ask a small first-round questionnaire for project type, platform, gameplay, art direction, team size, and AI assistance expectations.
- Dynamically ask second-round questions based on inferred project type.
- Diagnose project positioning, MVP scope, likely architecture, technical complexity, and risks.
- Resolve required AI skills and mark each as `installed`, `missing`, or `optional`.
- Generate a confirmation preview before writing scaffold files.
- Generate frozen context artifacts after user confirmation.
- Generate a scaffold manifest describing planned directories, Unity packages, templates, and verification commands.

## Non-Functional Requirements

- The questionnaire must be resumable.
- Every recommendation must include evidence, confidence, and rationale.
- The system must explicitly identify non-goals for the first phase.
- The system must prefer simple Unity architecture unless project constraints justify advanced systems.
- Skill installation must require user confirmation.
- Scaffold generation must be deterministic from the confirmed project brief.

## Acceptance Criteria

- A user can run `unity-ai new` and complete a guided onboarding session.
- The system produces `conductor/project-brief.md`, `conductor/ai-skills.md`, `conductor/architecture-decision.md`, `conductor/risk-register.md`, `conductor/mvp-plan.md`, and `scaffold-manifest.json`.
- The generated MVP plan includes explicit non-goals and first playable scope.
- The architecture recommendation includes options to use, avoid, and revisit later.
- Missing AI skills are listed with purpose and installation recommendation.
- No Unity project files are generated before user confirmation.
