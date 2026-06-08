from __future__ import annotations

import argparse
import json
from pathlib import Path
from uuid import uuid4

from agents.performance_optimizer.static_analyzer import write_performance_report
from context.unity_project_scanner import write_project_summary
from verification.runner import run_verification_commands, run_verification_from_config

from .artifacts import build_scaffold_manifest, render_confirmation_preview, write_confirmed_artifacts
from .diagnosis import diagnose_project
from .models import BootstrapperSession
from .questionnaire import answers_from_args, prompt_for_answers
from .scaffold import create_unity_project_files
from .skills import resolve_skills


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "new":
        return run_new(args)
    if args.command == "scan-project":
        return run_scan_project(args)
    if args.command == "performance-review":
        return run_performance_review(args)
    if args.command == "verify":
        return run_verify(args)
    if args.command == "scaffold":
        return run_scaffold(args)
    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="unity-ai")
    subparsers = parser.add_subparsers(dest="command")

    new_parser = subparsers.add_parser("new", help="Start AI Unity project onboarding.")
    new_parser.add_argument("--non-interactive", action="store_true", help="Use CLI args instead of prompts.")
    new_parser.add_argument("--confirm", action="store_true", help="Write artifacts after preview.")
    new_parser.add_argument("--create-unity-project", action="store_true", help="Create minimal Unity project files after confirmation.")
    new_parser.add_argument("--install-packages", action="store_true", help="Write recommended Unity packages into Packages/manifest.json.")
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
    new_parser.add_argument("--followup", action="append", default=[], help="Follow-up answer as key=value. Can be repeated.")

    scaffold_parser = subparsers.add_parser("scaffold", help="Create Unity project files from scaffold-manifest.json.")
    scaffold_parser.add_argument("--project-dir", default=".", help="Project directory.")
    scaffold_parser.add_argument("--manifest", default="scaffold-manifest.json", help="Path to scaffold manifest.")
    scaffold_parser.add_argument("--install-packages", action="store_true", help="Write package dependencies into Packages/manifest.json.")

    scan_parser = subparsers.add_parser("scan-project", help="Scan an existing Unity project.")
    scan_parser.add_argument("--project-dir", default=".", help="Unity project directory.")
    scan_parser.add_argument("--output", default=None, help="Output JSON path.")

    perf_parser = subparsers.add_parser("performance-review", help="Run static Unity performance review.")
    perf_parser.add_argument("--project-dir", default=".", help="Unity project directory.")
    perf_parser.add_argument("--output", default=None, help="Output JSON path.")

    verify_parser = subparsers.add_parser("verify", help="Run verification commands and write a report.")
    verify_parser.add_argument("--project-dir", default=".", help="Project directory.")
    verify_parser.add_argument("--command", action="append", help="Verification command. Can be repeated.")
    verify_parser.add_argument("--config", default=None, help="Verification config path. Defaults to .orchestrator/verification.json.")
    verify_parser.add_argument("--output", default=None, help="Output JSON path.")
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
    if args.create_unity_project:
        create_unity_project_files(
            Path(args.output_dir),
            build_scaffold_manifest(session),
            install_packages=args.install_packages,
        )
    print(f"Artifacts written to {Path(args.output_dir).resolve()}")
    return 0


def run_scaffold(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir)
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = project_dir / manifest_path
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    created = create_unity_project_files(project_dir, manifest, install_packages=args.install_packages)
    print(f"Created {len(created)} scaffold entries in {project_dir.resolve()}")
    return 0


def run_scan_project(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir)
    output = Path(args.output) if args.output else None
    summary = write_project_summary(project_dir, output)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def run_performance_review(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir)
    output = Path(args.output) if args.output else None
    findings = write_performance_report(project_dir, output)
    print(json.dumps({"findings": findings}, indent=2, ensure_ascii=False))
    return 0


def run_verify(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir)
    output = Path(args.output) if args.output else None
    if args.command:
        report = run_verification_commands(args.command, project_dir, output)
    else:
        config = Path(args.config) if args.config else None
        report = run_verification_from_config(project_dir, config, output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] in {"passed", "skipped"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
