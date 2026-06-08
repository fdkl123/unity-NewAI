from __future__ import annotations

import argparse
from pathlib import Path
from uuid import uuid4

from .artifacts import render_confirmation_preview, write_confirmed_artifacts
from .diagnosis import diagnose_project
from .models import BootstrapperSession
from .questionnaire import answers_from_args, prompt_for_answers
from .skills import resolve_skills


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "new":
        return run_new(args)
    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="unity-ai")
    subparsers = parser.add_subparsers(dest="command")

    new_parser = subparsers.add_parser("new", help="Start AI Unity project onboarding.")
    new_parser.add_argument("--non-interactive", action="store_true", help="Use CLI args instead of prompts.")
    new_parser.add_argument("--confirm", action="store_true", help="Write artifacts after preview.")
    new_parser.add_argument("--output-dir", default=".", help="Directory where artifacts should be written.")
    new_parser.add_argument("--project-name", default="UnityAIProject")
    new_parser.add_argument("--idea", default="")
    new_parser.add_argument("--dimension", default="undecided")
    new_parser.add_argument("--platforms", default="undecided")
    new_parser.add_argument("--core-action", default="undecided")
    new_parser.add_argument("--first-playable", default="undecided")
    new_parser.add_argument("--team", default="undecided")
    new_parser.add_argument("--ai-help", default="planning")
    new_parser.add_argument("--art-direction", default="undecided")
    new_parser.add_argument("--online-mode", default="single-player")
    return parser


def run_new(args: argparse.Namespace) -> int:
    answers = answers_from_args(args) if args.non_interactive else prompt_for_answers()
    diagnosis = diagnose_project(answers)
    skills = resolve_skills(answers, Path(args.output_dir))
    session = BootstrapperSession(
        session_id=f"bootstrap_{uuid4().hex[:12]}",
        status="confirmed" if args.confirm else "confirmation",
        answers=answers,
        diagnosis=diagnosis,
        skills=skills,
    )

    print(render_confirmation_preview(session))
    if not args.confirm:
        if args.non_interactive:
            print("Dry run only. Re-run with --confirm to write artifacts.")
            return 0
        confirmed = input("确认生成项目上下文和 scaffold manifest? [y/N]: ").strip().lower()
        if confirmed not in {"y", "yes"}:
            print("Cancelled. No files written.")
            return 0

    write_confirmed_artifacts(session, Path(args.output_dir))
    print(f"Artifacts written to {Path(args.output_dir).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
