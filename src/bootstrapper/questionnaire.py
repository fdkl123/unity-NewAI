from __future__ import annotations

from .models import ProjectAnswers


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def prompt_for_answers() -> ProjectAnswers:
    print("AI Unity Project Bootstrapper")
    print("先问清楚项目，再生成工程。")
    project_name = input("项目名称: ").strip() or "UnityAIProject"
    idea = input("一句话或一段话描述游戏想法: ").strip()
    dimension = input("2D / 3D / undecided: ").strip() or "undecided"
    platforms = split_csv(input("目标平台，用逗号分隔，例如 Android,iOS,PC: ").strip())
    core_action = input("玩家最核心的动作是什么: ").strip()
    first_playable = input("第一版可玩原型必须包含什么: ").strip()
    team_profile = input("团队情况，例如 solo / 2 programmers / designer+programmer: ").strip()
    ai_help = split_csv(input("希望 AI 帮什么，用逗号分隔，例如 planning,code,performance,tests: ").strip())
    art_direction = input("美术风格，例如 pixel, low-poly, stylized, realistic, undecided: ").strip()
    online_mode = input("联网需求，例如 single-player, co-op, multiplayer, undecided: ").strip()

    base_answers = ProjectAnswers(
        project_name=project_name,
        idea=idea,
        dimension=dimension or "undecided",
        target_platforms=platforms or ["undecided"],
        core_player_action=core_action or "undecided",
        first_playable=first_playable or "undecided",
        team_profile=team_profile or "undecided",
        ai_help_expected=ai_help or ["planning"],
        art_direction=art_direction or "undecided",
        online_mode=online_mode or "single-player",
    )
    return ProjectAnswers(
        **{
            **base_answers.__dict__,
            "follow_up_answers": prompt_for_followups(base_answers),
        }
    )


def prompt_for_followups(answers: ProjectAnswers) -> dict[str, str]:
    questions = conditional_followup_questions(answers)
    if not questions:
        return {}
    print("\nSecond-round questions / 第二轮针对性问题")
    followups: dict[str, str] = {}
    for key, question in questions.items():
        followups[key] = input(f"{question}: ").strip()
    return followups


def conditional_followup_questions(answers: ProjectAnswers) -> dict[str, str]:
    text = " ".join(
        [
            answers.idea,
            answers.dimension,
            " ".join(answers.target_platforms),
            answers.core_player_action,
            answers.first_playable,
            answers.online_mode,
        ]
    ).lower()
    questions: dict[str, str] = {}
    if any(keyword in text for keyword in ["action", "combat", "fight", "战斗", "动作", "shoot", "射击"]):
        questions.update(
            {
                "combat_scale": "Expected concurrent enemies/projectiles in the first playable",
                "hit_detection": "Preferred hit detection: physics trigger, raycast, animation event, or undecided",
                "camera_style": "Camera style: top-down, third-person, side view, fixed, or undecided",
            }
        )
    if any(keyword in text for keyword in ["roguelike", "rogue", "肉鸽", "随机", "wave", "波次"]):
        questions.update(
            {
                "run_structure": "Run structure: waves, rooms, timed survival, stages, or undecided",
                "upgrade_model": "Upgrade model for first playable: none, random choices, shop, drops, or undecided",
            }
        )
    if any(keyword in text for keyword in ["ui", "idle", "放置", "卡牌", "菜单", "背包"]):
        questions.update(
            {
                "screen_count": "Approximate number of screens in first playable",
                "data_tables": "Will the project use data tables/config files: yes, no, or undecided",
            }
        )
    if any(keyword in text for keyword in ["multiplayer", "online", "联网", "多人", "co-op"]):
        questions.update(
            {
                "network_authority": "Networking authority: client-host, dedicated server, peer-to-peer, or undecided",
                "sync_frequency": "Expected sync frequency or latency sensitivity",
            }
        )
    return questions


def answers_from_args(args: object) -> ProjectAnswers:
    return ProjectAnswers(
        project_name=args.project_name,
        idea=args.idea,
        dimension=args.dimension,
        target_platforms=split_csv(args.platforms),
        core_player_action=args.core_action,
        first_playable=args.first_playable,
        team_profile=args.team,
        ai_help_expected=split_csv(args.ai_help),
        art_direction=args.art_direction,
        online_mode=args.online_mode,
        follow_up_answers=_parse_followups(args.followup),
    )


def _parse_followups(values: list[str] | None) -> dict[str, str]:
    followups: dict[str, str] = {}
    for value in values or []:
        if "=" in value:
            key, answer = value.split("=", 1)
            followups[key.strip()] = answer.strip()
    return followups
