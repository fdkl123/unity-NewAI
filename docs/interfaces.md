# System Module Interfaces

## Core Data Types

### Bootstrapper Session

```json
{
  "session_id": "bootstrap_20260607_001",
  "status": "questionnaire | diagnosis | confirmation | confirmed | scaffolded | cancelled",
  "raw_answers": [],
  "project_signals": {
    "project_name": "ArenaPrototype",
    "dimension": "3D",
    "target_platforms": ["Android", "iOS"],
    "core_player_action": "Move, dodge, and fight enemy waves",
    "ai_help_expected": ["planning", "code", "performance", "tests"]
  },
  "created_at": "2026-06-07T00:00:00Z"
}
```

### Project Diagnosis

```json
{
  "project_type": ["3D", "mobile", "action", "roguelike"],
  "first_playable_scope": ["movement", "basic combat", "enemy spawning", "one arena", "object pooling"],
  "explicit_non_goals": ["multiplayer", "full equipment system", "story campaign"],
  "complexity": {
    "technical": "medium",
    "performance": "high",
    "content": "medium",
    "production": "medium"
  },
  "confidence": "medium",
  "evidence": ["target platform is mobile", "core loop includes enemy waves"]
}
```

### Skill Resolution

```json
{
  "skills": [
    {
      "name": "unity-performance",
      "status": "installed | missing | recommended | optional",
      "purpose": "Define budgets and review Unity performance risks",
      "trigger_scenarios": ["performance review", "object pooling", "GC allocation"]
    }
  ],
  "requires_install_confirmation": ["asset-pipeline"]
}
```

### Scaffold Manifest

```json
{
  "project_name": "ArenaPrototype",
  "template_profile": "3d_mobile_action_roguelike",
  "directories": ["Assets/_Project/Runtime", "Assets/_Project/Scenes"],
  "files": ["conductor/project-brief.md", "conductor/performance-budget.md"],
  "unity_packages": ["com.unity.inputsystem"],
  "ai_skills": ["unity-developer", "unity-performance", "memory-management"],
  "verification_commands": [],
  "requires_confirmation": ["install Unity packages"]
}
```

### Project Summary

```json
{
  "project_id": "unity_project_001",
  "root_path": "E:/Games/MyUnityProject",
  "unity": {
    "is_unity_project": true,
    "unity_version": "6000.0.0f1",
    "render_pipeline": "URP | HDRP | Built-in | unknown",
    "packages": ["com.unity.inputsystem", "com.unity.addressables"],
    "script_count": 128,
    "scene_count": 6,
    "asmdef_count": 4
  },
  "planning": {
    "documents": [
      {
        "path": "Docs/策划案.md",
        "kind": "design_doc | requirements | roadmap | balance_table | readme | unknown",
        "summary": "Wave-based mobile action roguelike with arena encounters."
      }
    ],
    "project_intent": "Mobile arena action game focused on repeatable combat runs.",
    "project_type": ["3D", "mobile", "action", "roguelike"],
    "target_platform_hints": ["Android", "iOS"],
    "gameplay_system_hints": ["spawning", "combat", "projectiles", "inventory", "upgrade choices"]
  },
  "architecture_prediction": {
    "current_hints": ["MonoBehaviour-heavy", "ScriptableObject configs"],
    "recommended_candidates": ["object pooling", "event-driven gameplay flow", "Addressables for content loading"],
    "avoid_for_now": ["full ECS rewrite"],
    "confidence": "medium"
  },
  "risk_hypotheses": [
    {
      "category": "performance",
      "risk": "Wave spawning may create frame spikes if enemies are instantiated during combat.",
      "mitigation": "Use prewarmed object pools sized by wave budget."
    }
  ],
  "verification_capabilities": {
    "has_editmode_tests": true,
    "has_playmode_tests": false,
    "has_build_config": false
  },
  "warnings": []
}
```

### Run

```json
{
  "run_id": "run_20260605_001",
  "project_id": "unity_project_001",
  "objective": "Optimize gameplay scene CPU and GC cost",
  "mode": "review_only | propose_patch",
  "status": "queued | running | verifying | healing | succeeded | failed | cancelled",
  "created_at": "2026-06-05T00:00:00Z"
}
```

### Task

```json
{
  "task_id": "task_perf_001",
  "run_id": "run_20260605_001",
  "type": "performance_review | gameplay_intent_guard | verification | self_healing",
  "agent": "performance_optimizer",
  "context_pack_id": "ctx_001",
  "permissions": ["read_repo", "write_patch", "run_tests"],
  "status": "queued | running | completed | failed"
}
```

### Context Pack

```json
{
  "context_pack_id": "ctx_001",
  "task_id": "task_perf_001",
  "token_budget": 24000,
  "sources": [
    {
      "path": "Assets/Scripts/EnemySpawner.cs",
      "reason": "Contains repeated Instantiate in gameplay loop"
    }
  ],
  "summary": "Unity URP mobile project with wave spawning and pooled projectile candidates."
}
```

### Finding

```json
{
  "finding_id": "finding_001",
  "category": "cpu | gc | rendering | physics | memory | asset_pipeline | design_risk",
  "severity": "critical | high | medium | low",
  "location": "Assets/Scripts/EnemySpawner.cs:42",
  "evidence": "Instantiate called during repeated spawn loop without pooling.",
  "recommendation": "Introduce object pool and prewarm based on wave size.",
  "expected_metric": "Reduce frame spikes and GC churn during enemy waves."
}
```

### Verification Gate

```json
{
  "gate_id": "gate_editmode_tests",
  "name": "Unity Edit Mode Tests",
  "command": "Unity -batchmode -runTests -testPlatform EditMode",
  "required": true,
  "status": "passed | failed | skipped | unsupported",
  "evidence_path": ".orchestrator/runs/run_001/gates/editmode.json"
}
```

## Agent Contracts

### Gameplay-Intent Guard

Input:

- Project context pack.
- Known architecture and constraints.
- Target platform and performance budget.
- Optional user notes about expected behavior.

Output:

- Behavior assumptions.
- Tuning-sensitive systems.
- Optimization risk flags.
- Manual approval requirements.
- Suggested behavior-preserving tests.

### Performance Optimizer Agent

Input:

- Unity project context pack.
- Static analyzer results.
- Optional profiler exports.
- Performance budgets.

Output:

- Prioritized findings.
- Root-cause explanations.
- Proposed fixes.
- Expected metric impact.
- Verification gates.
- Patch proposal when mode permits.

### Verification Agent

Input:

- Proposed changes or review target.
- Gate configuration.
- Project command environment.

Output:

- Gate statuses.
- Parsed failures.
- Evidence paths.
- Acceptance decision.

### Self-Healing Agent

Input:

- Failed gate result.
- Last patch or proposal.
- Relevant context pack.
- Retry count and policy.

Output:

- Failure diagnosis.
- Safe retry decision.
- Repair plan or patch proposal.
- Stop reason when unsafe or exhausted.

## API Sketch

- `POST /runs` — create scan, performance-review, verification, or demo run.
- `GET /runs/{run_id}` — get run state and timeline.
- `GET /runs/{run_id}/artifact` — get final artifact.
- `POST /runs/{run_id}/approve` — approve proposed patch or high-risk action.
- `POST /projects/{project_id}/scan` — scan Unity project.
- `GET /projects/{project_id}/memory` — list project memory.
- `POST /verification/gates` — register or update gate config.
