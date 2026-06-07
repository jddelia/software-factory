from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise AssertionError(f"{path} does not start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise AssertionError(f"{path} does not close YAML frontmatter")

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if not sep:
            raise AssertionError(f"invalid frontmatter line: {line}")
        fields[key.strip()] = value.strip().strip('"')
    return fields


class SkillPackageTests(unittest.TestCase):
    def test_skill_frontmatter_is_minimal_and_trigger_focused(self) -> None:
        fields = read_frontmatter(REPO_ROOT / "SKILL.md")

        self.assertEqual(set(fields), {"name", "description"})
        self.assertEqual(fields["name"], "software-factory")
        self.assertIn("Use when Codex should", fields["description"])
        self.assertIn("software factory", fields["description"])

    def test_agent_metadata_has_default_prompt(self) -> None:
        metadata = (REPO_ROOT / "agents" / "openai.yaml").read_text()

        self.assertIn('display_name: "Software Factory"', metadata)
        self.assertIn("$software-factory", metadata)
        self.assertIn("default_prompt:", metadata)

    def test_long_references_have_contents_sections(self) -> None:
        for path in (REPO_ROOT / "references").glob("*.md"):
            lines = path.read_text().splitlines()
            if len(lines) <= 100:
                continue
            opening = "\n".join(lines[:30])
            self.assertIn("## Contents", opening, f"{path} needs quick navigation")

    def test_public_package_metadata_is_present(self) -> None:
        required_paths = [
            "LICENSE",
            "SECURITY.md",
            "CONTRIBUTING.md",
            ".github/pull_request_template.md",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/feature_request.yml",
            "examples/safe-mvp-kickoff.md",
        ]
        for relative_path in required_paths:
            self.assertTrue((REPO_ROOT / relative_path).exists(), relative_path)

        readme = (REPO_ROOT / "README.md").read_text()
        self.assertNotIn("<owner>", readme)
        self.assertIn("https://github.com/jddelia/software-factory.git", readme)


if __name__ == "__main__":
    unittest.main()
