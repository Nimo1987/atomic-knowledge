import tempfile
import unittest
from pathlib import Path

from runtime import AtomicKnowledgeRuntime, RuntimeResult


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_KB_PATH = REPO_ROOT / "example-kb"
ENTRY_FILES = [
    "wiki/active.md",
    "wiki/recent.md",
    "wiki/index.md",
]
OPTIONAL_AREA_PATHS = {
    "wiki/projects",
    "wiki/procedures",
    "wiki/insights",
    "wiki/concepts",
    "wiki/entities",
    "meta/candidates",
}


class RuntimeActionTests(unittest.TestCase):
    def test_init_kb_creates_minimal_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_path = Path(temp_dir) / "kb"

            result = AtomicKnowledgeRuntime(kb_path).init_kb()

            self.assertIsInstance(result, RuntimeResult)
            self.assertTrue(result.success)
            self.assertEqual(result.action, "init_kb")
            self.assertIn("kb_path", result.data)
            self.assertTrue((kb_path / "AGENT.md").is_file())
            self.assertTrue((kb_path / "wiki/active.md").is_file())
            self.assertTrue((kb_path / "wiki/procedures").is_dir())
            self.assertTrue((kb_path / "meta/lint-status.json").is_file())

    def test_check_kb_succeeds_for_initialized_kb(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_path = Path(temp_dir) / "kb"
            AtomicKnowledgeRuntime(kb_path).init_kb()

            result = AtomicKnowledgeRuntime(kb_path).check_kb()

            self.assertIsInstance(result, RuntimeResult)
            self.assertEqual(result.action, "check_kb")
            self.assertEqual(result.data["returncode"], 0)
            self.assertTrue(result.success)

    def test_check_kb_fails_for_empty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_path = Path(temp_dir) / "empty-kb"
            kb_path.mkdir()

            result = AtomicKnowledgeRuntime(kb_path).check_kb()

            self.assertIsInstance(result, RuntimeResult)
            self.assertFalse(result.success)
            self.assertNotEqual(result.data["returncode"], 0)

    def test_get_context_returns_entry_files_for_example_kb(self) -> None:
        result = AtomicKnowledgeRuntime(EXAMPLE_KB_PATH).get_context()

        self.assertTrue(result.success)
        self.assertEqual(result.action, "get_context")
        for relative_path in ENTRY_FILES:
            self.assertIn(relative_path, result.data["recommended_files"])

        optional_paths = {item["path"] for item in result.data["optional_areas"]}
        self.assertTrue(OPTIONAL_AREA_PATHS.issubset(optional_paths))

        procedure_area = next(
            item
            for item in result.data["optional_areas"]
            if item["path"] == "wiki/procedures"
        )
        procedure_hint = next(
            item
            for item in procedure_area["file_hints"]
            if item["path"] == "wiki/procedures/filesystem-first-query-flow.md"
        )
        self.assertIn("retrieval order", procedure_hint["search_anchors"])
        self.assertIn("Atomic Knowledge", procedure_hint["key_entities"])

    def test_get_context_reports_missing_entry_files_for_empty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_path = Path(temp_dir) / "empty-kb"
            kb_path.mkdir()

            result = AtomicKnowledgeRuntime(kb_path).get_context()

            self.assertTrue(result.success)
            self.assertEqual(result.data["recommended_files"], [])
            for relative_path in ENTRY_FILES:
                self.assertIn(relative_path, result.data["missing_expected_files"])

    def test_validate_kb_reports_expected_shape_for_example_kb(self) -> None:
        result = AtomicKnowledgeRuntime(EXAMPLE_KB_PATH).validate_kb()

        self.assertIsInstance(result, RuntimeResult)
        self.assertEqual(result.action, "validate_kb")
        self.assertIsNotNone(result.report)
        self.assertIsInstance(result.data["checked_files_count"], int)
        self.assertIsInstance(result.report.warnings, list)
        self.assertIsInstance(result.report.issues, list)

    def test_validate_kb_fails_for_empty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_path = Path(temp_dir) / "empty-kb"
            kb_path.mkdir()

            result = AtomicKnowledgeRuntime(kb_path).validate_kb()

            self.assertFalse(result.success)
            self.assertTrue(result.data["missing_files"])
            self.assertTrue(result.data["missing_directories"])

    def test_validate_kb_reports_frontmatter_issue_for_bad_kb(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_path = Path(temp_dir) / "kb"
            AtomicKnowledgeRuntime(kb_path).init_kb()
            (kb_path / "meta/candidates/bad-frontmatter.md").write_text(
                "---\nstatus: open\n",
                encoding="utf-8",
            )

            result = AtomicKnowledgeRuntime(kb_path).validate_kb()

            self.assertFalse(result.success)
            self.assertTrue(
                any("frontmatter" in issue for issue in result.report.issues)
            )


if __name__ == "__main__":
    unittest.main()
