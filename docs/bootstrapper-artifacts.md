# Bootstrapper Artifacts

## `conductor/project-brief.md`

Frozen summary of the confirmed project.

Required sections:

- Project name.
- One-line positioning.
- Target platforms.
- Project type tags.
- Core player experience.
- First playable scope.
- Explicit non-goals.
- Team and production constraints.
- Confirmation record.

## `conductor/ai-skills.md`

Project-level AI capability dependencies.

Required sections:

- Required skills.
- Optional skills.
- Missing skills.
- Installation recommendations.
- Skill trigger scenarios.
- Skill boundaries.

## `conductor/architecture-decision.md`

Architecture recommendation and rationale.

Required sections:

- Recommended architecture.
- Rationale and evidence.
- Alternatives considered.
- Options to avoid for now.
- Revisit triggers.
- Confidence level.

## `conductor/risk-register.md`

Risk register for technical and production planning.

Required sections:

- Risk.
- Category.
- Probability.
- Impact.
- Mitigation.
- Owner.
- Review trigger.

## `conductor/mvp-plan.md`

First playable plan.

Required sections:

- First playable objective.
- In-scope features.
- Out-of-scope features.
- Milestones.
- Acceptance criteria.
- Verification gates.

## `conductor/performance-budget.md`

Initial performance budget.

Required sections:

- Target FPS.
- Target platforms.
- Frame-time budget.
- GC allocation policy.
- Draw call target.
- Memory target.
- Loading target.
- Profiling plan.

## `scaffold-manifest.json`

Deterministic scaffold plan generated from the confirmed brief.

Required fields:

```json
{
  "project_name": "ArenaPrototype",
  "template_profile": "3d_mobile_action_roguelike",
  "directories": [],
  "files": [],
  "unity_packages": [],
  "ai_skills": [],
  "verification_commands": [],
  "requires_confirmation": []
}
```
