from __future__ import annotations

from .models import (
    ArchitectureRecommendation,
    Complexity,
    ProjectAnswers,
    ProjectDiagnosis,
    Risk,
)


def diagnose_project(answers: ProjectAnswers) -> ProjectDiagnosis:
    text = " ".join(
        [
            answers.idea,
            answers.dimension,
            " ".join(answers.target_platforms),
            answers.core_player_action,
            answers.first_playable,
            answers.art_direction,
            answers.online_mode,
        ]
    ).lower()

    project_type = _infer_project_type(answers, text)
    first_scope = _infer_first_scope(answers, text)
    non_goals = _infer_non_goals(text)
    complexity = _estimate_complexity(project_type, text, answers)
    architecture = _recommend_architecture(project_type, text, answers)
    risks = _infer_risks(project_type, text, answers)
    evidence = _collect_evidence(answers, project_type)

    confidence = "medium" if answers.idea and answers.core_player_action else "low"
    return ProjectDiagnosis(
        project_type=project_type,
        first_playable_scope=first_scope,
        explicit_non_goals=non_goals,
        complexity=complexity,
        architecture=architecture,
        risks=risks,
        confidence=confidence,
        evidence=evidence,
    )


def _infer_project_type(answers: ProjectAnswers, text: str) -> list[str]:
    tags: list[str] = []
    dimension = answers.dimension.upper()
    if dimension in {"2D", "3D"}:
        tags.append(dimension)

    if any(platform.lower() in {"android", "ios", "mobile"} for platform in answers.target_platforms):
        tags.append("mobile")
    if any(platform.lower() in {"pc", "windows", "mac", "linux", "steam"} for platform in answers.target_platforms):
        tags.append("pc")
    if "webgl" in text or "web" in text:
        tags.append("webgl")

    keyword_tags = {
        "action": ["action", "combat", "fight", "battle", "shoot", "射击", "战斗", "动作"],
        "roguelike": ["roguelike", "rogue", "肉鸽", "随机", "run"],
        "rpg": ["rpg", "role", "角色", "装备", "升级"],
        "idle": ["idle", "放置", "挂机"],
        "simulation": ["simulation", "sim", "模拟", "经营"],
        "puzzle": ["puzzle", "解谜"],
        "multiplayer": ["multiplayer", "online", "联网", "多人", "co-op"],
        "ui-heavy": ["ui", "菜单", "列表", "卡牌", "背包"],
    }
    for tag, keywords in keyword_tags.items():
        if any(keyword in text for keyword in keywords):
            tags.append(tag)

    return _dedupe(tags or ["prototype"])


def _infer_first_scope(answers: ProjectAnswers, text: str) -> list[str]:
    scope = [item.strip() for item in answers.first_playable.replace("，", ",").split(",") if item.strip()]
    if scope:
        return scope

    defaults = ["one playable scene", "player control", "one core interaction", "basic win/fail condition"]
    if "combat" in text or "战斗" in text:
        defaults.extend(["basic combat", "one enemy type"])
    if "wave" in text or "波次" in text:
        defaults.append("simple wave spawning")
    return defaults


def _infer_non_goals(text: str) -> list[str]:
    non_goals = ["full content pipeline", "production monetization", "large-scale refactor"]
    if "multiplayer" not in text and "联网" not in text and "多人" not in text:
        non_goals.append("multiplayer")
    if "open world" not in text and "开放世界" not in text:
        non_goals.append("open world")
    if "story" not in text and "剧情" not in text:
        non_goals.append("full story campaign")
    return non_goals


def _estimate_complexity(project_type: list[str], text: str, answers: ProjectAnswers) -> Complexity:
    technical = "medium"
    performance = "medium"
    content = "medium"
    production = "medium"

    if "multiplayer" in project_type:
        technical = "high"
        production = "high"
    if "mobile" in project_type and any(tag in project_type for tag in ["action", "roguelike", "simulation"]):
        performance = "high"
    if any(keyword in text for keyword in ["many enemies", "大量", "弹幕", "hundreds", "open world", "开放世界"]):
        performance = "high"
        technical = "high"
    if "solo" in answers.team_profile.lower():
        production = "medium-high"
    if any(tag in project_type for tag in ["rpg", "simulation"]):
        content = "high"

    return Complexity(
        technical=technical,
        performance=performance,
        content=content,
        production=production,
    )


def _recommend_architecture(
    project_type: list[str], text: str, answers: ProjectAnswers
) -> ArchitectureRecommendation:
    recommended = ["MonoBehaviour feature modules", "ScriptableObject data configs", "basic event channel"]
    avoid = ["full ECS/DOTS rewrite", "custom render pipeline", "premature multiplayer architecture"]
    revisit = ["Addressables after content scale is clearer", "ECS/DOTS after entity count is proven high"]
    rationale = ["Simple Unity architecture keeps the first playable cheap to build and easy for AI agents to modify."]

    if "mobile" in project_type:
        recommended.extend(["URP", "performance budget from day one"])
        rationale.append("Mobile targets require early frame-time, memory, and GC constraints.")
    if any(tag in project_type for tag in ["action", "roguelike"]):
        recommended.extend(["object pooling", "state machines for gameplay actors"])
        rationale.append("Action and roguelike loops commonly create spawn, projectile, animation, and GC pressure.")
    if "ui-heavy" in project_type or "idle" in project_type:
        recommended.extend(["UI screen flow layer", "list virtualization where needed", "save data service"])
        rationale.append("UI-heavy games need explicit UI lifecycle and allocation control.")
    if "multiplayer" in project_type or answers.online_mode.lower() in {"multiplayer", "co-op"}:
        recommended.append("networking spike before implementation")
        avoid = [item for item in avoid if item != "premature multiplayer architecture"]
        rationale.append("Networking decisions affect architecture and must be validated before scaffold expansion.")

    confidence = "medium"
    if answers.target_platforms and answers.core_player_action and answers.first_playable:
        confidence = "high"

    return ArchitectureRecommendation(
        recommended=_dedupe(recommended),
        avoid_for_now=_dedupe(avoid),
        revisit_later=_dedupe(revisit),
        confidence=confidence,
        rationale=rationale,
    )


def _infer_risks(project_type: list[str], text: str, answers: ProjectAnswers) -> list[Risk]:
    risks = [
        Risk(
            category="scope",
            risk="First playable may expand beyond a testable prototype if non-goals are not enforced.",
            probability="medium",
            impact="high",
            mitigation="Freeze project-brief.md and require Scope Guard review for new systems.",
        )
    ]
    if "mobile" in project_type:
        risks.append(
            Risk(
                category="performance",
                risk="Mobile frame time and GC spikes can appear early if gameplay loops allocate per frame.",
                probability="high",
                impact="high",
                mitigation="Enable performance budget, object pooling, and static performance review from the first sprint.",
            )
        )
    if any(tag in project_type for tag in ["action", "roguelike"]) or "wave" in text or "波次" in text:
        risks.append(
            Risk(
                category="architecture",
                risk="Spawning, projectiles, and enemy lifecycle may become tangled without ownership boundaries.",
                probability="medium",
                impact="high",
                mitigation="Create explicit spawner, pool, actor state, and damage interaction modules.",
            )
        )
    if "solo" in answers.team_profile.lower():
        risks.append(
            Risk(
                category="production",
                risk="Solo development can stall if art, content, and systems are all treated as P0.",
                probability="medium",
                impact="medium",
                mitigation="Limit first playable to one scene, placeholder art, and one validated core loop.",
            )
        )
    return risks


def _collect_evidence(answers: ProjectAnswers, project_type: list[str]) -> list[str]:
    evidence = [
        f"Game idea: {answers.idea}",
        f"Target platforms: {', '.join(answers.target_platforms)}",
        f"Core player action: {answers.core_player_action}",
        f"Project type tags: {', '.join(project_type)}",
    ]
    if answers.team_profile:
        evidence.append(f"Team profile: {answers.team_profile}")
    return evidence


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
