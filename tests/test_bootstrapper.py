from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bootstrapper.artifacts import build_scaffold_manifest, write_confirmed_artifacts
from bootstrapper.cli import main
from bootstrapper.diagnosis import diagnose_project
from bootstrapper.models import BootstrapperSession, ProjectAnswers
from bootstrapper.questionnaire import conditional_followup_questions
from bootstrapper.scaffold import create_unity_project_files
from bootstrapper.skills import resolve_skills
from context.unity_project_scanner import scan_unity_project
from agents.performance_optimizer.static_analyzer import analyze_project
from verification.runner import load_verification_commands, run_verification_commands, run_verification_from_config


class BootstrapperTests(unittest.TestCase):
    def make_answers(self) -> ProjectAnswers:
        return ProjectAnswers(
            project_name="ArenaPrototype",
            idea="Mobile 3D roguelike action arena with enemy waves.",
            dimension="3D",
            target_platforms=["Android", "iOS"],
            core_player_action="Move, dodge, and fight waves of enemies.",
            first_playable="movement,basic combat,enemy spawning,one arena",
            team_profile="solo",
            ai_help_expected=["planning", "code", "performance", "tests"],
            art_direction="low-poly",
            online_mode="single-player",
        )

    def test_diagnosis_detects_mobile_action_risk(self) -> None:
        diagnosis = diagnose_project(self.make_answers())

        self.assertIn("3D", diagnosis.project_type)
        self.assertIn("mobile", diagnosis.project_type)
        self.assertIn("roguelike", diagnosis.project_type)
        self.assertIn("object pooling", diagnosis.architecture.recommended)
        self.assertTrue(any(risk.category == "performance" for risk in diagnosis.risks))

    def test_skill_resolution_adds_performance_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skills = resolve_skills(self.make_answers(), Path(temp_dir))

        skill_names = {skill.name for skill in skills}
        self.assertIn("spec", skill_names)
        self.assertIn("unity-developer", skill_names)
        self.assertIn("unity-performance", skill_names)
        self.assertIn("memory-management", skill_names)
        self.assertIn("testing-verification", skill_names)

    def test_conditional_followups_for_action_roguelike(self) -> None:
        questions = conditional_followup_questions(self.make_answers())

        self.assertIn("combat_scale", questions)
        self.assertIn("run_structure", questions)

    def test_artifact_writer_creates_confirmed_files(self) -> None:
        answers = self.make_answers()
        diagnosis = diagnose_project(answers)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            session = BootstrapperSession(
                session_id="bootstrap_test",
                status="confirmed",
                answers=answers,
                diagnosis=diagnosis,
                skills=resolve_skills(answers, output_dir),
            )

            write_confirmed_artifacts(session, output_dir)

            self.assertTrue((output_dir / "conductor" / "project-brief.md").exists())
            self.assertTrue((output_dir / "conductor" / "ai-skills.md").exists())
            self.assertTrue((output_dir / "scaffold-manifest.json").exists())
            manifest = json.loads((output_dir / "scaffold-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["project_name"], "ArenaPrototype")
            self.assertIn("com.unity.inputsystem", manifest["unity_packages"])

    def test_cli_non_interactive_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = main(
                [
                    "new",
                    "--non-interactive",
                    "--output-dir",
                    temp_dir,
                    "--project-name",
                    "DryRun",
                    "--idea",
                    "A small PC puzzle prototype.",
                    "--dimension",
                    "2D",
                    "--platforms",
                    "PC",
                    "--core-action",
                    "Solve tile puzzles.",
                    "--first-playable",
                    "one puzzle,reset,retry",
                    "--team",
                    "solo",
                    "--ai-help",
                    "planning,code",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertFalse((Path(temp_dir) / "scaffold-manifest.json").exists())

    def test_manifest_is_deterministic_for_session(self) -> None:
        answers = self.make_answers()
        diagnosis = diagnose_project(answers)
        session = BootstrapperSession(
            session_id="bootstrap_test",
            status="confirmed",
            answers=answers,
            diagnosis=diagnosis,
            skills=[],
        )

        self.assertEqual(build_scaffold_manifest(session), build_scaffold_manifest(session))

    def test_scaffold_creates_unity_project_files_and_packages(self) -> None:
        answers = self.make_answers()
        diagnosis = diagnose_project(answers)
        session = BootstrapperSession(
            session_id="bootstrap_test",
            status="confirmed",
            answers=answers,
            diagnosis=diagnosis,
            skills=[],
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            manifest = build_scaffold_manifest(session)
            create_unity_project_files(output_dir, manifest, install_packages=True)

            self.assertTrue((output_dir / "Assets" / "_Project" / "README.md").exists())
            self.assertTrue((output_dir / "Packages" / "manifest.json").exists())
            self.assertTrue((output_dir / "ProjectSettings" / "ProjectVersion.txt").exists())
            self.assertTrue((output_dir / ".orchestrator" / "verification.json").exists())
            package_manifest = json.loads((output_dir / "Packages" / "manifest.json").read_text(encoding="utf-8"))
            self.assertIn("com.unity.inputsystem", package_manifest["dependencies"])

    def test_unity_project_scanner_detects_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "Assets" / "_Project" / "Runtime").mkdir(parents=True)
            (root / "Packages").mkdir()
            (root / "ProjectSettings").mkdir()
            (root / "ProjectSettings" / "ProjectVersion.txt").write_text("m_EditorVersion: 6000.0.0f1\n", encoding="utf-8")
            (root / "Packages" / "manifest.json").write_text(
                json.dumps({"dependencies": {"com.unity.render-pipelines.universal": "17.0.3"}}),
                encoding="utf-8",
            )
            (root / "Assets" / "_Project" / "Runtime" / "Player.cs").write_text("public class Player {}", encoding="utf-8")

            summary = scan_unity_project(root)

            self.assertTrue(summary["unity"]["is_unity_project"])
            self.assertEqual(summary["unity"]["render_pipeline"], "URP")
            self.assertEqual(summary["unity"]["script_count"], 1)

    def test_static_analyzer_finds_hot_path_issues(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            script = root / "Assets" / "_Project" / "Runtime" / "EnemySpawner.cs"
            script.parent.mkdir(parents=True)
            script.write_text(
                """
using UnityEngine;
public class EnemySpawner : MonoBehaviour {
  void Update() {
    var rb = GetComponent<Rigidbody>();
    Instantiate(gameObject);
    Physics.Raycast(transform.position, transform.forward);
  }
}
""",
                encoding="utf-8",
            )

            findings = analyze_project(root)

            categories = {finding["category"] for finding in findings}
            self.assertIn("cpu", categories)
            self.assertIn("object_lifecycle", categories)
            self.assertIn("physics", categories)

    def test_verification_runner_records_command_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            report = run_verification_commands(["python --version"], root)

            self.assertEqual(report["status"], "passed")
            self.assertTrue((root / ".orchestrator" / "reports" / "verification-report.json").exists())

    def test_verification_runner_reads_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config = root / ".orchestrator" / "verification.json"
            config.parent.mkdir(parents=True)
            config.write_text(json.dumps({"commands": ["python --version"]}), encoding="utf-8")

            self.assertEqual(load_verification_commands(root), ["python --version"])
            report = run_verification_from_config(root)
            self.assertEqual(report["status"], "passed")

    def test_verification_runner_skips_without_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = run_verification_from_config(Path(temp_dir))

            self.assertEqual(report["status"], "skipped")

    def test_cli_confirm_can_create_unity_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = main(
                [
                    "new",
                    "--non-interactive",
                    "--confirm",
                    "--create-unity-project",
                    "--install-packages",
                    "--output-dir",
                    temp_dir,
                    "--project-name",
                    "GeneratedGame",
                    "--idea",
                    "Mobile 3D action prototype.",
                    "--dimension",
                    "3D",
                    "--platforms",
                    "Android",
                    "--core-action",
                    "Fight enemies.",
                    "--first-playable",
                    "movement,combat",
                    "--team",
                    "solo",
                    "--ai-help",
                    "planning,performance",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(temp_dir) / "ProjectSettings" / "ProjectVersion.txt").exists())
            self.assertTrue((Path(temp_dir) / "conductor" / "project-brief.md").exists())


if __name__ == "__main__":
    unittest.main()
