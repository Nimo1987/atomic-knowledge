# MCP Adapter

This directory contains the minimal MCP adapter for the Atomic Knowledge runtime.

The adapter is intentionally narrow:
- optional
- minimal
- aimed at agent integration and tool-calling environments
- not the primary user entry point

Atomic Knowledge remains chat-native. Ordinary users should not need to learn MCP in order to use the project.

Current scope:
- stdio JSON-RPC / MCP handling for `initialize`, `notifications/initialized`, `tools/list`, and `tools/call`
- four runtime-backed tools: `atomic_knowledge_init_kb`, `atomic_knowledge_check_kb`, `atomic_knowledge_get_context`, and `atomic_knowledge_validate_kb`
- input validation, runtime dispatch, and JSON serialization of `RuntimeResult`

Contracts, permission boundaries, and write-safety notes live in [`../../docs/MCP_TOOL_CONTRACTS.md`](../../docs/MCP_TOOL_CONTRACTS.md).

Implementation notes:
- `handle_request()` is the main adapter entry for direct calls and smoke tests.
- `serve_stdio()` provides minimal `Content-Length` framed stdio transport for MCP hosts.
- Runtime logic stays in `runtime/`; the adapter does not replace the markdown protocol or introduce a broader CLI surface.
