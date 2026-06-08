from __future__ import annotations

import json
from pathlib import Path


DEFAULT_UNITY_VERSION = "6000.0.0f1"


def create_unity_project_files(output_dir: Path, manifest: dict, install_packages: bool = False) -> list[Path]:
    created: list[Path] = []
    for directory in manifest.get("directories", []):
        path = output_dir / directory
        path.mkdir(parents=True, exist_ok=True)
        created.append(path)

    project_version = output_dir / "ProjectSettings" / "ProjectVersion.txt"
    _write(project_version, f"m_EditorVersion: {DEFAULT_UNITY_VERSION}\nm_EditorVersionWithRevision: {DEFAULT_UNITY_VERSION}\n")
    created.append(project_version)

    project_settings = output_dir / "ProjectSettings" / "ProjectSettings.asset"
    _write(
        project_settings,
        "%YAML 1.1\n--- !u!129 &1\nPlayerSettings:\n  productGUID: 00000000000000000000000000000000\n",
    )
    created.append(project_settings)

    readme = output_dir / "Assets" / "_Project" / "README.md"
    _write(
        readme,
        "# Unity Project Structure\n\nThis scaffold was generated from `conductor/project-brief.md`.\n",
    )
    created.append(readme)

    package_manifest = output_dir / "Packages" / "manifest.json"
    dependencies = {}
    if install_packages:
        dependencies.update(_unity_package_versions(manifest.get("unity_packages", [])))
    _write(
        package_manifest,
        json.dumps({"dependencies": dependencies}, indent=2, ensure_ascii=False) + "\n",
    )
    created.append(package_manifest)

    packages_lock = output_dir / "Packages" / "packages-lock.json"
    _write(packages_lock, json.dumps({"dependencies": {}}, indent=2) + "\n")
    created.append(packages_lock)

    verification_config = output_dir / ".orchestrator" / "verification.json"
    _write(
        verification_config,
        json.dumps(
            {
                "commands": [],
                "notes": [
                    "Add project-specific commands here, for example Unity batchmode tests or Python tooling checks.",
                    "The `unity-ai verify` command reads this file when no --command is provided.",
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    )
    created.append(verification_config)

    return created


def _unity_package_versions(packages: list[str]) -> dict[str, str]:
    versions = {
        "com.unity.inputsystem": "1.7.0",
        "com.unity.render-pipelines.universal": "17.0.3",
        "com.unity.addressables": "2.2.2",
    }
    return {package: versions.get(package, "latest") for package in packages}


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
