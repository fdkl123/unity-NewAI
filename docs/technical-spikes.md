# Technical Spike List

## Spike 1: Unity Repository Scanner

- **Question**: Can the system reliably detect Unity version, packages, render pipeline, scripts, scenes, and test configuration from files alone?
- **Output**: Scanner prototype and project summary schema.
- **Risk Reduced**: Context quality and onboarding reliability.

## Spike 2: Static Performance Analyzer

- **Question**: How accurately can static rules detect common Unity performance problems before profiler data exists?
- **Output**: Analyzer rules for `Update` lookups, allocations, pooling candidates, physics hot paths, and material instancing.
- **Risk Reduced**: MVP value without Unity Editor integration.

## Spike 3: Context Pack Builder

- **Question**: Can task-specific context packs stay compact while preserving enough source evidence?
- **Output**: Ranking and summarization prototype with source attribution.
- **Risk Reduced**: Agent quality and token cost.

## Spike 4: Verification Gate Runner

- **Question**: Can checks be configured across heterogeneous Unity projects without hardcoding one studio workflow?
- **Output**: Gate config schema and command runner.
- **Risk Reduced**: Adoption friction.

## Spike 5: Self-Healing Boundaries

- **Question**: Which failures are safe for autonomous retry and which require approval?
- **Output**: Retry policy, failure taxonomy, and sample repair loop.
- **Risk Reduced**: Trust and safety.

## Spike 6: Demo Fixture

 - **Question**: Can a small Unity sample demonstrate performance detection, gameplay-risk guarding, verification failure, and repair?
- **Output**: Fixture project or mocked repository with seeded issues.
- **Risk Reduced**: Fundraising, sales, and internal validation.
