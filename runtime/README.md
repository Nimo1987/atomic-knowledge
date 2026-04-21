# Runtime

This directory contains the internal Atomic Knowledge runtime.

The runtime is:
- internal
- agent-facing
- optional
- a bounded execution layer for mechanical knowledge-base actions

It is not:
- the main product entry point
- a normal end-user surface
- a replacement for the markdown filesystem protocol
- a CLI-first workflow

Atomic Knowledge remains chat-native. Ordinary users should continue to work through natural-language chat with an agent; they do not need to learn runtime calls, CLI commands, or MCP details for normal use.

The markdown knowledge base remains the source of truth. The runtime only helps an agent execute small, repeatable operations after the relevant intent and authorization judgment has already been made.

Current implemented actions:
- `init_kb` initializes a knowledge base by delegating to `scripts/init-kb.sh`
- `check_kb` runs the existing health check through `scripts/check-kb.sh`
- `get_context` returns a stable recommended read set from entry pages and known optional areas, including page-level `search_anchors` and `key_entities` hints when present
- `validate_kb` performs lightweight structural validation for required files, directories, and markdown frontmatter

There is no CLI-first surface here. Agent hosts may call the runtime directly in code or through the optional MCP adapter in [`../adapters/mcp/`](../adapters/mcp/).

For the product direction and runtime boundary, see [`../docs/AGENT_RUNTIME_DIRECTION.md`](../docs/AGENT_RUNTIME_DIRECTION.md) and [`../docs/RUNTIME_BOUNDARY.md`](../docs/RUNTIME_BOUNDARY.md).
