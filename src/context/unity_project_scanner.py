from __future__ import annotations

import json
from pathlib import Path


PLANNING_NAMES = ("readme", "docs", "design", "策划", "需求", "企画", "기획")


def scan_unity_project(root: Path) -> dict:
    assets = root / "Assets"
    packages = root / "Packages"
    project_settings = root / "ProjectSettings"
    scripts = sorted(str(path.relative_to(root)) for path in assets.rglob("*.cs")) if assets.exists() else []
    scenes = sorted(str(path.relative_to(root)) for path in assets.rglob("*.unity")) if assets.exists() else []
    asmdefs = sorted(str(path.relative_to(root)) for path in assets.rglob("*.asmdef")) if assets.exists() else []
    planning_docs = _find_planning_docs(root)
    package_dependencies = _read_manifest(packages / "manifest.json")

    return {
        "root_path": str(root.resolve()),
        "unity": {
            "is_unity_project": assets.exists() and packages.exists() and project_settings.exists(),
            "unity_version": _read_unity_version(project_settings / "ProjectVersion.txt"),
            "render_pipeline": _detect_render_pipeline(package_dependencies),
            "packages": sorted(package_dependencies.keys()),
            "script_count": len(scripts),
            "scene_count": len(scenes),
            "asmdef_count": len(asmdefs),
        },
        "files": {
            "scripts": scripts,
            "scenes": scenes,
            "asmdefs": asmdefs,
            "planning_documents": planning_docs,
        },
        "verification_capabilities": {
            "has_editmode_tests": any("editor" in path.lower() or "editmode" in path.lower() for path in scripts),
            "has_playmode_tests": any("playmode" in path.lower() for path in scripts),
            "has_build_config": (root / ".orchestrator" / "verification.json").exists(),
        },
        "warnings": _warnings(assets, packages, project_settings),
    }


def write_project_summary(root: Path, output_path: Path | None = None) -> dict:
    summary = scan_unity_project(root)
    output_path = output_path or root / ".orchestrator" / "project-summary.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def _read_unity_version(path: Path) -> str:
    if not path.exists():
        return "unknown"
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("m_EditorVersion:"):
            return line.split(":", 1)[1].strip()
    return "unknown"


def _read_manifest(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data.get("dependencies", {})


def _detect_render_pipeline(packages: dict) -> str:
    if "com.unity.render-pipelines.universal" in packages:
        return "URP"
    if "com.unity.render-pipelines.high-definition" in packages:
        return "HDRP"
    return "Built-in or unknown"


def _find_planning_docs(root: Path) -> list[str]:
    matches: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".csv", ".tsv", ".json"}:
            continue
        relative = str(path.relative_to(root))
        lowered = relative.lower()
        if any(name in lowered for name in PLANNING_NAMES):
            matches.append(relative)
    return sorted(matches)


def _warnings(assets: Path, packages: Path, project_settings: Path) -> list[str]:
    warnings: list[str] = []
    if not assets.exists():
        warnings.append("Missing Assets directory.")
    if not packages.exists():
        warnings.append("Missing Packages directory.")
    if not project_settings.exists():
        warnings.append("Missing ProjectSettings directory.")
    return warnings
