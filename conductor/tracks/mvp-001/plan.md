# MVP Implementation Plan

## Phase 1: Foundation

- Define run state machine, task contracts, and artifact schema.
- Implement project scanner for Unity repositories.
- Implement design-document scanner for project intent, type, architecture hints, and risk hypotheses.
- Create context pack builder for scripts, settings, scenes, and docs.
- Add persisted run history and project memory records.
- Lock first-stage modes to `review_only` and `propose_patch`.

## Phase 2: Performance Core

- Implement Unity performance optimizer agent contract and static finding schema.
- Add initial analyzers for update-loop lookups, GC allocations, object lifecycle churn, and physics hot paths.
- Add gameplay-intent capture to flag behavior-changing optimizations.
- Add agent result merger and conflict handling.

## Phase 3: Verification and Self-Healing

- Implement verification gate registry and command runner.
- Add parser model for test, build, analyzer, and profiler-budget outputs.
- Implement bounded self-healing diagnosis flow.
- Store failure records and successful repair patterns.

## Phase 4: Product Surface

- Add CLI for starting scan, performance review, verification, and demo runs.
- Display run timeline, agent outputs, verification gates, and findings.
- Add review-only and patch-proposal modes.
- Prepare a demo Unity fixture and end-to-end script.

## Phase 5: Hardening

- Add benchmark fixtures with seeded performance issues.
- Add regression tests for analyzers, task contracts, and gate parsing.
- Validate error handling, retry limits, and artifact persistence.
- Document installation, usage, and demo flow.
