# Self-Healing Design

## Goal

Self-healing exists to recover from failed verification without unbounded autonomous changes.

## Policy

- Default maximum attempts: 3.
- Each attempt must target a specific failure.
- The system must stop on destructive, ambiguous, or broad architectural changes.
- The final report must include every attempt and reason for success or stop.

## Diagnosis Inputs

- Failed gate type.
- Command and raw output.
- Parsed error.
- Last changed files or proposed changes.
- Relevant source context.
- Similar historical failures from memory.

## Retry Decision

Retry is allowed when:

- Failure has a clear local cause.
- Patch scope is narrow.
- Verification command is repeatable.
- The risk policy permits mutation.

Retry is blocked when:

- Failure requires product judgment.
- Failure implies broad refactor.
- Required dependency or environment is missing.
- Retry budget is exhausted.
