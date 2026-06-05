from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "seed_factory_docs.py"


class SeedFactoryDocsTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_dry_run_does_not_write_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_script(
                tmp,
                "--project-name",
                "Demo Project",
                "--work-mode",
                "safe_mvp",
                "--dry-run",
                "--print-kickoff",
            )

            self.assertIn("DRY-RUN CREATE", result.stdout)
            self.assertIn("tool_call_budget_policy: bounded_reads", result.stdout)
            self.assertIn("default_resume_mode: continue_same_baton", result.stdout)
            self.assertFalse((Path(tmp) / "docs").exists())

    def test_seeded_docs_include_control_plane_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.run_script(
                tmp,
                "--project-name",
                "Recovery Demo",
                "--work-mode",
                "recovery",
            )

            root = Path(tmp)
            factory_config = (root / "docs" / "factory_config.md").read_text()
            ledger = (root / "docs" / "build_ledger.md").read_text()
            protocol = (root / "docs" / "codex_factory_protocol.md").read_text()

            self.assertTrue((root / "AGENTS.md").exists())
            self.assertIn("default_resume_mode: recovery_first", factory_config)
            self.assertIn("tool_call_budget_policy: bounded_reads", factory_config)
            self.assertIn("thread_read_policy: latest_only", ledger)
            self.assertIn("thread tool schema", ledger)
            self.assertIn("Active actor polling: `adaptive_backoff`", protocol)
            self.assertIn("active_actor_polling_policy: adaptive_backoff", ledger)

    def test_no_agents_flag_skips_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.run_script(tmp, "--project-name", "No Agents Demo", "--no-agents")

            self.assertFalse((Path(tmp) / "AGENTS.md").exists())
            self.assertTrue((Path(tmp) / "docs" / "factory_config.md").exists())


if __name__ == "__main__":
    unittest.main()
