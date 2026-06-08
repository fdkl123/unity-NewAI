from __future__ import annotations

from pathlib import Path

from .models import ProjectAnswers, SkillResolution


KNOWN_SKILL_PATHS = {
    "unity-developer": [".agents/skills/unity-developer", ".codex/skills/unity-developer"],
    "unity-performance": [".agents/skills/unity-performance", ".codex/skills/unity-performance"],
    "memory-management": [".agents/skills/memory-management", ".codex/skills/memory-management"],
    "testing-verification": [".agents/skills/testing-verification", ".codex/skills/testing-verification"],
    "asset-pipeline": [".agents/skills/asset-pipeline", ".codex/skills/asset-pipeline"],
    "spec": [".agents/skills/spec", ".codex/skills/spec"],
}


def resolve_skills(answers: ProjectAnswers, root: Path | None = None) -> list[SkillResolution]:
    requested = {item.lower() for item in answers.ai_help_expected}
    text = " ".join(
        [
            answers.idea,
            answers.dimension,
            " ".join(answers.target_platforms),
            answers.core_player_action,
            answers.first_playable,
        ]
    ).lower()

    required: list[tuple[str, str, list[str]]] = [
        (
            "spec",
            "Turn user intent into feature specifications before implementation.",
            ["feature planning", "scope changes", "acceptance criteria"],
        ),
        (
            "unity-developer",
            "Implement Unity gameplay systems using maintainable project structure.",
            ["Unity code generation", "gameplay systems", "scene structure"],
        ),
    ]

    if "performance" in requested or any(platform.lower() in {"android", "ios", "mobile"} for platform in answers.target_platforms):
        required.append(
            (
                "unity-performance",
                "Define budgets and review Unity CPU, memory, rendering, physics, and GC risks.",
                ["performance review", "frame budget", "GC allocation", "rendering cost"],
            )
        )
        required.append(
            (
                "memory-management",
                "Guide object pooling, allocation control, and resource lifecycle decisions.",
                ["object pooling", "spawn systems", "GC control", "asset lifetime"],
            )
        )

    if "tests" in requested or "verification" in requested:
        required.append(
            (
                "testing-verification",
                "Define verification gates for generated gameplay and optimization changes.",
                ["Unity tests", "verification gates", "regression checks"],
            )
        )

    if any(keyword in text for keyword in ["addressables", "content", "大量资源", "关卡", "角色", "装备"]):
        required.append(
            (
                "asset-pipeline",
                "Plan content loading, import settings, Addressables, compression, and asset lifecycle.",
                ["Addressables", "asset import", "content loading", "compression"],
            )
        )

    root = root or Path.cwd()
    return [
        SkillResolution(
            name=name,
            status=_skill_status(name, root),
            purpose=purpose,
            trigger_scenarios=triggers,
        )
        for name, purpose, triggers in _dedupe_by_name(required)
    ]


def _skill_status(name: str, root: Path) -> str:
    for relative_path in KNOWN_SKILL_PATHS.get(name, []):
        if (root / relative_path).exists():
            return "installed"
    return "missing"


def _dedupe_by_name(items: list[tuple[str, str, list[str]]]) -> list[tuple[str, str, list[str]]]:
    seen: set[str] = set()
    result: list[tuple[str, str, list[str]]] = []
    for item in items:
        if item[0] not in seen:
            seen.add(item[0])
            result.append(item)
    return result
