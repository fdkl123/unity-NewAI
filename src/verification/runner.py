from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path


DEFAULT_CONFIG_PATH = ".orchestrator/verification.json"


def load_verification_commands(root: Path, config_path: Path | None = None) -> list[str]:
    config_path = config_path or root / DEFAULT_CONFIG_PATH
    if not config_path.exists():
        return []
    data = json.loads(config_path.read_text(encoding="utf-8"))
    commands = data.get("commands", [])
    if not isinstance(commands, list):
        raise ValueError("verification config `commands` must be a list")
    return [str(command) for command in commands]


def run_verification_commands(commands: list[str], root: Path, output_path: Path | None = None) -> dict:
    results = []
    for command in commands:
        started = time.perf_counter()
        completed = subprocess.run(command, cwd=root, shell=True, capture_output=True, text=True)
        results.append(
            {
                "command": command,
                "exit_code": completed.returncode,
                "duration_seconds": round(time.perf_counter() - started, 3),
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "status": "passed" if completed.returncode == 0 else "failed",
            }
        )
    report = {
        "status": "passed" if all(result["exit_code"] == 0 for result in results) else "failed",
        "results": results,
    }
    output_path = output_path or root / ".orchestrator" / "reports" / "verification-report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def run_verification_from_config(root: Path, config_path: Path | None = None, output_path: Path | None = None) -> dict:
    commands = load_verification_commands(root, config_path)
    if not commands:
        report = {
            "status": "skipped",
            "reason": "No verification commands configured.",
            "results": [],
        }
        output_path = output_path or root / ".orchestrator" / "reports" / "verification-report.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return report
    return run_verification_commands(commands, root, output_path)
