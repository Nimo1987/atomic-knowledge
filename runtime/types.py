"""Minimal runtime data structures for the internal execution layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class RuntimeRequest:
    """Common request envelope for a runtime action."""

    action: str
    kb_path: Path
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeReport:
    """Reusable structured report for check, context, and validate actions."""

    success: bool
    summary: str = ""
    warnings: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeResult:
    """Common result envelope returned by a runtime action."""

    action: str
    success: bool
    message: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    report: Optional[RuntimeReport] = None
