from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import BootstrapperSession, ProjectAnswers, ProjectDiagnosis, SkillResolution


def build_scaffold_manifest(session: BootstrapperSession) -> dict:
    answers = session.answers
    diagnosis = session.diagnosis
    profile = "_".join(tag.lower().replace("-", "_") for tag in diagnosis.project_type[:4])
    directories = [
        "Assets/_Project/Runtime",
        "Assets/_Project/Editor",
        "Assets/_Project/Tests",
        "Assets/_Project/Scenes",
        "Assets/_Project/Prefabs",
        "Assets/_Project/ScriptableObjects",
        "Assets/_Project/Settings",
        "conductor",
        ".orchestrator/rules",
        ".orchestrator/reports",
    ]
    files = [
        "conductor/project-brief.md",
        "conductor/ai-skills.md",
        "conductor/architecture-decision.md",
        "conductor/risk-register.md",
        "conductor/mvp-plan.md",
        "conductor/performance-budget.md",
        ".orchestrator/verification.json",
        "scaffold-manifest.json",
    ]
    packages = []
    if "3D" in diagnosis.project_type or "2D" in diagnosis.project_type:
        packages.append("com.unity.inputsystem")
    if "mobile" in diagnosis.project_type:
        packages.append("com.unity.render-pipelines.universal")

    return {
        "project_name": answers.project_name,
        "template_profile": profile or "unity_prototype",
        "directories": directories,
        "files": files,
        "unity_packages": packages,
        "ai_skills": [skill.name for skill in session.skills],
        "verification_commands": [],
        "requires_confirmation": ["install Unity packages", "create or modify Unity ProjectSettings"],
    }


def write_confirmed_artifacts(session: BootstrapperSession, output_dir: Path) -> None:
    conductor = output_dir / "conductor"
    conductor.mkdir(parents=True, exist_ok=True)
    (output_dir / ".orchestrator" / "rules").mkdir(parents=True, exist_ok=True)
    (output_dir / ".orchestrator" / "reports").mkdir(parents=True, exist_ok=True)

    _write(conductor / "project-brief.md", render_project_brief(session))
    _write(conductor / "ai-skills.md", render_ai_skills(session.skills))
    _write(conductor / "architecture-decision.md", render_architecture_decision(session))
    _write(conductor / "risk-register.md", render_risk_register(session.diagnosis))
    _write(conductor / "mvp-plan.md", render_mvp_plan(session))
    _write(conductor / "performance-budget.md", render_performance_budget(session))

    manifest = build_scaffold_manifest(session)
    _write(output_dir / "scaffold-manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    _write(
        output_dir / ".orchestrator" / "bootstrapper-session.json",
        json.dumps(asdict(session), indent=2, ensure_ascii=False) + "\n",
    )


def render_confirmation_preview(session: BootstrapperSession) -> str:
    answers = session.answers
    diagnosis = session.diagnosis
    skills = ", ".join(f"{skill.name}({skill.status})" for skill in session.skills)
    risks = "\n".join(f"- {risk.category}: {risk.risk}" for risk in diagnosis.risks)
    return f"""Project Confirmation Preview

Project: {answers.project_name}
Positioning: {answers.idea}
Type: {", ".join(diagnosis.project_type)}
Platforms: {", ".join(answers.target_platforms)}
First playable: {", ".join(diagnosis.first_playable_scope)}
Non-goals: {", ".join(diagnosis.explicit_non_goals)}
Architecture: {", ".join(diagnosis.architecture.recommended)}
Avoid now: {", ".join(diagnosis.architecture.avoid_for_now)}
AI skills: {skills}
Confidence: {diagnosis.confidence}

Major risks:
{risks}
"""


def render_project_brief(session: BootstrapperSession) -> str:
    answers = session.answers
    diagnosis = session.diagnosis
    return f"""# Project Brief

## Project Name

{answers.project_name}

## One-Line Positioning

{answers.idea}

## Target Platforms

{_bullets(answers.target_platforms)}

## Project Type Tags

{_bullets(diagnosis.project_type)}

## Core Player Experience

{answers.core_player_action}

## First Playable Scope

{_bullets(diagnosis.first_playable_scope)}

## Explicit Non-Goals

{_bullets(diagnosis.explicit_non_goals)}

## Team and Production Constraints

{answers.team_profile}

## Confirmation Record

- Session: `{session.session_id}`
- Created: `{session.created_at}`
- Confidence: `{diagnosis.confidence}`
"""


def render_ai_skills(skills: list[SkillResolution]) -> str:
    sections = []
    for skill in skills:
        sections.append(
            f"""## {skill.name}

- Status: `{skill.status}`
- Purpose: {skill.purpose}
- Trigger scenarios: {", ".join(skill.trigger_scenarios)}
"""
        )
    return "# AI Skills\n\n" + "\n".join(sections)


def render_architecture_decision(session: BootstrapperSession) -> str:
    architecture = session.diagnosis.architecture
    return f"""# Architecture Decision

## Recommended Architecture

{_bullets(architecture.recommended)}

## Rationale and Evidence

{_bullets(architecture.rationale + session.diagnosis.evidence)}

## Options to Avoid for Now

{_bullets(architecture.avoid_for_now)}

## Revisit Triggers

{_bullets(architecture.revisit_later)}

## Confidence

{architecture.confidence}
"""


def render_risk_register(diagnosis: ProjectDiagnosis) -> str:
    lines = [
        "# Risk Register",
        "",
        "| Category | Risk | Probability | Impact | Mitigation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for risk in diagnosis.risks:
        lines.append(
            f"| {risk.category} | {risk.risk} | {risk.probability} | {risk.impact} | {risk.mitigation} |"
        )
    return "\n".join(lines) + "\n"


def render_mvp_plan(session: BootstrapperSession) -> str:
    diagnosis = session.diagnosis
    return f"""# MVP Plan

## First Playable Objective

Build a small, testable version of the core player experience before expanding systems or content.

## In-Scope Features

{_bullets(diagnosis.first_playable_scope)}

## Out-of-Scope Features

{_bullets(diagnosis.explicit_non_goals)}

## Milestones

- M1: Create project skeleton and one playable scene.
- M2: Implement core interaction with placeholder assets.
- M3: Add minimum feedback, failure/win condition, and tuning data.
- M4: Run performance review and verification gates.

## Acceptance Criteria

- The core loop can be played end to end.
- The project uses the confirmed architecture boundaries.
- Performance budget exists before optimization work starts.
- Non-goals are not added without Scope Guard review.
"""


def render_performance_budget(session: BootstrapperSession) -> str:
    platforms = [platform.lower() for platform in session.answers.target_platforms]
    mobile = any(platform in {"android", "ios", "mobile"} for platform in platforms)
    fps = "60 FPS" if mobile else "60 FPS minimum"
    draw_calls = "Under 100 for simple mobile scenes" if mobile else "Project-specific after first benchmark"
    memory = "Keep runtime memory conservative for target mobile devices" if mobile else "Measure after first content benchmark"
    return f"""# Performance Budget

## Target FPS

{fps}

## Frame-Time Budget

- 60 FPS target: 16.67 ms per frame.
- Scripts: target under 4 ms for gameplay scenes.
- Physics: target under 2 ms unless gameplay requires otherwise.

## GC Allocation Policy

- Gameplay hot paths should target 0 B/frame managed allocations.
- Avoid per-frame string concatenation, LINQ allocations, collection creation, and uncached yield instructions.

## Draw Call Target

{draw_calls}

## Memory Target

{memory}

## Loading Target

- First playable should use simple scene loading.
- Revisit Addressables after content scale is proven.

## Profiling Plan

- Run static performance review after first playable.
- Add Unity Profiler captures once gameplay scene exists.
"""


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None"
