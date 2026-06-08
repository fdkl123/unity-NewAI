# End-to-End Demo Scenario

## Demo Goal

Show the Orchestrator reviewing a Unity wave-based arena encounter, identifying performance risks, and proposing safe optimizations without changing gameplay intent.

## Setup

- Sample Unity project with player controller, enemy prefab, projectile prefab, and one gameplay scene.
- Seeded performance issues:
  - `GetComponent` called in `Update`.
  - `Instantiate` used during wave spawning.
  - Per-frame string concatenation in HUD.
  - Physics raycast without cached layer mask.

## User Prompt

Review this wave-based arena encounter for mobile 60 FPS. Identify CPU, GC, physics, rendering, and UI risks, then propose safe fixes without changing encounter pacing or difficulty.

## Expected Flow

1. Orchestrator creates scan, performance review, gameplay-intent guard, and verification tasks.
2. Context builder selects gameplay scripts, prefabs metadata, project settings, and performance budgets.
3. Gameplay-intent guard records encounter pacing, difficulty, and tuning-sensitive systems.
4. Performance optimizer detects seeded issues and prioritizes fixes.
5. Verification pipeline runs static analyzer and tests.
6. Self-healing diagnoses a seeded failed check and proposes a narrow repair.
7. Final artifact summarizes findings, gameplay risks, verification evidence, and next steps.

## Demo Success Criteria

- Performance findings cite concrete files and root causes.
- Proposed fixes state whether gameplay behavior could change.
- Verification status is visible and auditable.
- Self-healing stops or succeeds within the retry limit.
