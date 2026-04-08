"""Minimal error hierarchy for the internal runtime surface."""


class RuntimeErrorBase(Exception):
    """Base class for runtime-specific errors."""


class RuntimeConfigurationError(RuntimeErrorBase):
    """Raised when runtime configuration is missing or invalid."""


class RuntimeActionNotImplementedError(RuntimeErrorBase, NotImplementedError):
    """Raised when a declared runtime action is still a placeholder."""
