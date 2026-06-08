# Development Workflow

## Operating Model

Use Context → Spec → Plan → Implement → Verify → Record Memory.

## Standard Track Flow

1. Read `conductor/index.md` and active track files.
2. Confirm scope and non-goals.
3. Update or create a spec with acceptance criteria.
4. Create an implementation plan with verification gates.
5. Implement minimal focused changes.
6. Run the narrowest relevant checks first.
7. Record decisions, failures, and reusable project facts in memory artifacts.

## Quality Gates

Every implemented feature should define:

- Static validation gate.
- Unit or integration test gate when applicable.
- Unity-specific gate such as edit mode tests, play mode tests, build validation, profiler budget, or analyzer report.
- Manual review gate when automation cannot safely verify behavior.

## Agent Autonomy Policy

- Agents may read repository files and generate reports without approval.
- Agents may propose patches after showing scope.
- Agents must not delete assets, rewrite broad architecture, or alter global project settings without explicit approval.
- Self-healing is limited to 3 attempts by default.
- Failed verification must include the failing command, parsed error, likely cause, and proposed next step.

## Performance Review Policy

Optimization work must:

- Start with a baseline or explain why no baseline exists.
- Tie each fix to a measurable budget.
- Avoid speculative micro-optimizations unless they address known Unity hot paths.
- Prefer root-cause fixes such as pooling, caching, batching, culling, or event-driven flow.
- Preserve gameplay behavior unless a design change explicitly requires otherwise.
