"""Service skeleton for the internal Atomic Knowledge runtime."""

from __future__ import annotations

import subprocess
import re
from pathlib import Path
from typing import Iterable, NoReturn, Union

from .errors import RuntimeActionNotImplementedError, RuntimeConfigurationError
from .types import RuntimeReport, RuntimeResult


ENTRY_FILE_PATHS = (
    Path("wiki/active.md"),
    Path("wiki/recent.md"),
    Path("wiki/index.md"),
)

OPTIONAL_AREA_PATHS = (
    Path("wiki/projects"),
    Path("wiki/insights"),
    Path("wiki/concepts"),
    Path("wiki/entities"),
    Path("meta/candidates"),
)

VALIDATE_ENTRY_FILE_PATHS = (
    Path("wiki/active.md"),
    Path("wiki/recent.md"),
    Path("wiki/index.md"),
    Path("wiki/log.md"),
)

VALIDATE_DIRECTORY_PATHS = (
    Path("raw/sources"),
    Path("wiki/concepts"),
    Path("wiki/entities"),
    Path("wiki/projects"),
    Path("wiki/insights"),
    Path("meta/candidates"),
)

VALIDATE_MARKDOWN_ROOT_PATHS = (
    Path("wiki"),
    Path("meta/candidates"),
)

FRONTMATTER_NAME_PATTERN = re.compile(r"^\s*(title|name)\s*:")


class AtomicKnowledgeRuntime:
    """Optional agent-facing runtime for bounded KB execution.

    This service is a mechanical execution layer. It does not interpret user
    intent, decide write authorization, or replace the markdown protocol.
    """

    def __init__(self, kb_path: Union[str, Path]) -> None:
        """Store the base knowledge-base location for later runtime actions."""

        if not kb_path:
            raise RuntimeConfigurationError(
                "kb_path is required for the runtime service"
            )

        self.kb_path = Path(kb_path).expanduser()

    def init_kb(self) -> RuntimeResult:
        """Initialize a KB by delegating to the repository init script."""

        kb_path = self.kb_path.resolve(strict=False)
        if kb_path.exists() and not kb_path.is_dir():
            raise RuntimeConfigurationError(
                f"kb_path must point to a directory path: {kb_path}"
            )

        if kb_path.parent.exists() and not kb_path.parent.is_dir():
            raise RuntimeConfigurationError(
                f"kb_path parent is not a directory: {kb_path.parent}"
            )

        script_path = Path(__file__).resolve().parents[1] / "scripts" / "init-kb.sh"
        if not script_path.is_file():
            raise RuntimeConfigurationError(f"init_kb script is missing: {script_path}")

        completed = subprocess.run(
            ["bash", str(script_path), str(kb_path)],
            capture_output=True,
            text=True,
            check=False,
        )

        data = {
            "kb_path": str(kb_path),
            "script_path": str(script_path),
        }

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        if stdout:
            data["stdout"] = stdout
        if stderr:
            data["stderr"] = stderr

        if completed.returncode != 0:
            data["returncode"] = completed.returncode
            return RuntimeResult(
                action="init_kb",
                success=False,
                message=f"init_kb failed with exit code {completed.returncode}",
                data=data,
            )

        return RuntimeResult(
            action="init_kb",
            success=True,
            message=f"Initialized knowledge base at {kb_path}",
            data=data,
        )

    def check_kb(self) -> RuntimeResult:
        """Run the repository health check script against an existing KB."""

        kb_path = self.kb_path.resolve(strict=False)
        if not kb_path.exists():
            raise RuntimeConfigurationError(f"kb_path does not exist: {kb_path}")

        if not kb_path.is_dir():
            raise RuntimeConfigurationError(
                f"kb_path must point to an existing directory: {kb_path}"
            )

        script_path = Path(__file__).resolve().parents[1] / "scripts" / "check-kb.sh"
        if not script_path.is_file():
            raise RuntimeConfigurationError(
                f"check_kb script is missing: {script_path}"
            )

        completed = subprocess.run(
            ["bash", str(script_path), str(kb_path)],
            capture_output=True,
            text=True,
            check=False,
        )

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        result_line = ""
        if stdout:
            for line in reversed(stdout.splitlines()):
                line = line.strip()
                if line.startswith("Result:"):
                    result_line = line
                    break

        data = {
            "kb_path": str(kb_path),
            "script_path": str(script_path),
            "returncode": completed.returncode,
        }

        if stdout:
            data["stdout"] = stdout
        if stderr:
            data["stderr"] = stderr

        if completed.returncode != 0:
            message = f"check_kb failed with exit code {completed.returncode}"
            if result_line:
                message = f"{message}: {result_line}"

            return RuntimeResult(
                action="check_kb",
                success=False,
                message=message,
                data=data,
            )

        message = f"Completed knowledge base health check for {kb_path}"
        if result_line:
            message = f"{message}: {result_line}"

        return RuntimeResult(
            action="check_kb",
            success=True,
            message=message,
            data=data,
        )

    def get_context(self) -> RuntimeResult:
        """Return a stable, structure-based recommended read set for a KB."""

        kb_path = self.kb_path.resolve(strict=False)
        if not kb_path.exists():
            raise RuntimeConfigurationError(f"kb_path does not exist: {kb_path}")

        if not kb_path.is_dir():
            raise RuntimeConfigurationError(
                f"kb_path must point to an existing directory: {kb_path}"
            )

        recommended_files = []
        missing_expected_files = []
        for relative_path in ENTRY_FILE_PATHS:
            candidate = kb_path / relative_path
            if candidate.is_file():
                recommended_files.append(relative_path.as_posix())
            else:
                missing_expected_files.append(relative_path.as_posix())

        optional_areas = []
        for relative_path in OPTIONAL_AREA_PATHS:
            area_path = kb_path / relative_path
            if not area_path.is_dir():
                continue

            area_files = sorted(
                (
                    child
                    for child in area_path.iterdir()
                    if child.is_file() and not child.name.startswith(".")
                ),
                key=lambda child: (child.name != "index.md", child.name),
            )
            available_files = [
                child.relative_to(kb_path).as_posix() for child in area_files
            ]
            optional_areas.append(
                {
                    "path": relative_path.as_posix(),
                    "available_files": available_files,
                }
            )

        message = f"Prepared context read set for {kb_path}"
        if missing_expected_files:
            message = (
                f"{message} with {len(missing_expected_files)} missing expected entry "
                "file(s)"
            )

        return RuntimeResult(
            action="get_context",
            success=True,
            message=message,
            data={
                "kb_path": str(kb_path),
                "recommended_files": recommended_files,
                "optional_areas": optional_areas,
                "missing_expected_files": missing_expected_files,
            },
        )

    def validate_kb(self) -> RuntimeResult:
        """Run lightweight structural validation against an existing KB."""

        kb_path = self.kb_path.resolve(strict=False)
        if not kb_path.exists():
            raise RuntimeConfigurationError(f"kb_path does not exist: {kb_path}")

        if not kb_path.is_dir():
            raise RuntimeConfigurationError(
                f"kb_path must point to an existing directory: {kb_path}"
            )

        missing_files = [
            relative_path.as_posix()
            for relative_path in VALIDATE_ENTRY_FILE_PATHS
            if not (kb_path / relative_path).is_file()
        ]
        missing_directories = [
            relative_path.as_posix()
            for relative_path in VALIDATE_DIRECTORY_PATHS
            if not (kb_path / relative_path).is_dir()
        ]

        warnings = []
        issues = [
            f"missing required file: {relative_path}" for relative_path in missing_files
        ]
        issues.extend(
            f"missing required directory: {relative_path}"
            for relative_path in missing_directories
        )

        checked_files = []
        for relative_path in self._iter_validate_markdown_files(kb_path):
            checked_files.append(relative_path)
            status = self._frontmatter_status(kb_path / relative_path)
            if status == "missing":
                warnings.append(f"missing frontmatter block: {relative_path}")
            elif status == "unclosed":
                issues.append(f"unclosed frontmatter block: {relative_path}")
            elif status == "missing_name":
                issues.append(
                    f"frontmatter missing required title/name field: {relative_path}"
                )

        success = not issues
        summary = self._build_validation_summary(
            checked_files_count=len(checked_files),
            warning_count=len(warnings),
            issue_count=len(issues),
        )
        message = f"Validated knowledge base at {kb_path}"
        if issues:
            message = f"Validation found {len(issues)} issue(s) in {kb_path}"
        elif warnings:
            message = (
                f"Validation completed with {len(warnings)} warning(s) for {kb_path}"
            )

        return RuntimeResult(
            action="validate_kb",
            success=success,
            message=message,
            data={
                "kb_path": str(kb_path),
                "checked_files_count": len(checked_files),
                "missing_files": missing_files,
                "missing_directories": missing_directories,
            },
            report=RuntimeReport(
                success=success,
                summary=summary,
                warnings=warnings,
                issues=issues,
                details={
                    "kb_path": str(kb_path),
                    "checked_files_count": len(checked_files),
                },
            ),
        )

    def _iter_validate_markdown_files(self, kb_path: Path) -> Iterable[str]:
        relative_paths = []
        for root_path in VALIDATE_MARKDOWN_ROOT_PATHS:
            absolute_root = kb_path / root_path
            if not absolute_root.is_dir():
                continue

            for file_path in absolute_root.rglob("*.md"):
                if not file_path.is_file():
                    continue

                relative_path = file_path.relative_to(kb_path)
                if any(part.startswith(".") for part in relative_path.parts):
                    continue

                relative_paths.append(relative_path.as_posix())

        yield from sorted(set(relative_paths))

    def _frontmatter_status(self, file_path: Path) -> str:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0].strip() != "---":
            return "missing"

        closing_index = None
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                closing_index = index
                break

        if closing_index is None:
            return "unclosed"

        frontmatter_lines = lines[1:closing_index]
        if any(FRONTMATTER_NAME_PATTERN.match(line) for line in frontmatter_lines):
            return "ok"

        return "missing_name"

    def _build_validation_summary(
        self, checked_files_count: int, warning_count: int, issue_count: int
    ) -> str:
        return (
            "Checked "
            f"{checked_files_count} markdown file(s); found {issue_count} issue(s) "
            f"and {warning_count} warning(s)."
        )

    def _not_implemented(self, action: str) -> NoReturn:
        raise RuntimeActionNotImplementedError(
            f"{action} is a runtime placeholder only. "
            "Task 4 adds the module skeleton; a later task will implement the action."
        )
