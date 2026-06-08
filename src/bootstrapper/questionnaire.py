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

    return ProjectAnswers(
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
    )
