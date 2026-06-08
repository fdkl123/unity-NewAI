# Verification Pipeline

## Purpose

The verification pipeline prevents agents from treating generated code or recommendations as complete without evidence. It converts checks into structured gates that the Orchestrator can enforce.

## Gate Types

- **Static Analysis**: Unity C# anti-pattern scan, style checks, dependency checks.
- **Unit Tests**: Edit mode tests, pure C# tests, analyzer tests.
- **Play Mode Tests**: Gameplay validation for Unity scenes and mechanics.
- **Build Validation**: Batchmode build or compile-only checks.
- **Profiler Budget**: CPU, GC, memory, draw call, and physics budgets from profiler exports.
- **Manual Review**: Required when automation cannot verify design feel or visual quality.

## MVP Required Gates

- Project scan completes.
- Static performance analyzer completes.
- Configured test command passes or is explicitly marked unsupported.
- Final artifact includes findings and verification evidence.

## Performance Budgets

Default budgets should be project-configurable:

- Target frame time: 16.67 ms for 60 FPS or 33.33 ms for 30 FPS.
- Scripts CPU budget: 4 ms for 60 FPS targets.
- Physics budget: 2 ms for 60 FPS targets.
- Runtime GC allocation: ideally 0 B per frame in gameplay hot paths.
- Mobile draw calls: project-specific target, commonly below 100 for simple scenes.

## Failure Handling

When a gate fails:

1. Store raw output.
2. Parse failure into structured error.
3. Determine whether self-healing is safe.
4. Retry only within policy.
5. Escalate with evidence when unsafe or exhausted.
