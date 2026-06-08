from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal


SkillStatus = Literal["installed", "missing", "recommended", "optional"]


@dataclass(frozen=True)
class ProjectAnswers:
    project_name: str
    idea: str
    dimension: str
    target_platforms: list[str]
    core_player_action: str
    first_playable: str
    team_profile: str
    ai_help_expected: list[str]
    art_direction: str = "undecided"
    online_mode: str = "single-player"
    follow_up_answers: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Complexity:
    technical: str
    performance: str
    content: str
    production: str


@dataclass(frozen=True)
class ArchitectureRecommendation:
    recommended: list[str]
    avoid_for_now: list[str]
    revisit_later: list[str]
    confidence: str
    rationale: list[str]


@dataclass(frozen=True)
class Risk:
    category: str
    risk: str
    probability: str
    impact: str
    mitigation: str


@dataclass(frozen=True)
class ProjectDiagnosis:
    project_type: list[str]
    first_playable_scope: list[str]
    explicit_non_goals: list[str]
    complexity: Complexity
    architecture: ArchitectureRecommendation
    risks: list[Risk]
    confidence: str
    evidence: list[str]


@dataclass(frozen=True)
class SkillResolution:
    name: str
    status: SkillStatus
    purpose: str
    trigger_scenarios: list[str]


@dataclass(frozen=True)
class BootstrapperSession:
    session_id: str
    status: str
    answers: ProjectAnswers
    diagnosis: ProjectDiagnosis
    skills: list[SkillResolution]
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    )
