from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path


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
