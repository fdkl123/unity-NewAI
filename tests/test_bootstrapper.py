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
from bootstrapper.skills import resolve_skills


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


if __name__ == "__main__":
    unittest.main()
