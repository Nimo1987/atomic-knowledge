"""Minimal MCP adapter exports for Atomic Knowledge."""

from .server import handle_request, main, serve_stdio

__all__ = ["handle_request", "main", "serve_stdio"]
