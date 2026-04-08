# MCP Tool Contracts

This note defines the minimal tool contract, permission boundary, and write safety boundary for the Atomic Knowledge MCP adapter.

The MCP adapter is an optional execution surface over bounded runtime actions. It is not the main user surface, not the policy layer, and not an authorization layer.

## Scope

- This contract covers the four V1 MCP tools exposed by the adapter.
- Each tool requires a `kb_path` string that points to the target knowledge-base root.
- MCP `tools/call` returns a tool response with `content` and `isError`.
- The `content` payload is a JSON-serialized runtime result with this minimal shape:

```json
{
  "action": "init_kb | check_kb | get_context | validate_kb",
  "success": true,
  "message": "human-readable summary",
  "data": {},
  "report": null
}
```

- `report` is optional and is mainly relevant for validation-style results.
- A successful tool call means the bounded runtime action executed successfully. It does not by itself authorize any follow-up write.

## Tool Classes

### Write-Capable

| Tool | Class | Direct-Call Rule |
|------|-------|------------------|
| `atomic_knowledge_init_kb` | Write-Capable | Call only when setup intent is clear and the target location is understood. |

### Read-Only

| Tool | Class | Direct-Call Rule |
|------|-------|------------------|
| `atomic_knowledge_check_kb` | Read-Only | Safe for bounded inspection once the KB path is known. |
| `atomic_knowledge_get_context` | Read-Only | Safe for read-side context recovery once the KB path is known. |
| `atomic_knowledge_validate_kb` | Read-Only | Safe for bounded structural inspection once the KB path is known. |

## Tool Contracts

### `atomic_knowledge_init_kb`

- Purpose: initialize a knowledge base directory with the standard Atomic Knowledge starter structure.
- Required Input: `kb_path` as the chosen knowledge-base directory.
- Side Effects: creates directories and files, copies the starter structure, mirrors local schemas, and writes a generated `AGENT.md` into the target knowledge base.
- Expected Output Shape: `action="init_kb"`, `success`, `message`, and `data` containing `kb_path`, `script_path`, and optional execution details such as `stdout`, `stderr`, and `returncode` on failure.
- Safe Default Usage: use only when the user has clearly asked to set up or initialize a knowledge base. If the directory choice is ambiguous, sensitive, already exists, or may affect the broader workspace layout, confirm first.

### `atomic_knowledge_check_kb`

- Purpose: run a bounded health check against an existing knowledge base.
- Required Input: `kb_path` as an existing knowledge-base directory.
- Side Effects: no intended knowledge-base writes; this is a read-side inspection action.
- Expected Output Shape: `action="check_kb"`, `success`, `message`, and `data` containing `kb_path`, `script_path`, `returncode`, and optional `stdout` or `stderr` from the health check.
- Safe Default Usage: safe for read-side inspection, maintenance diagnosis, or confirming that a known knowledge base is usable. Its result does not authorize any later writeback step.

### `atomic_knowledge_get_context`

- Purpose: return a stable recommended read set from entry pages and known optional areas.
- Required Input: `kb_path` as an existing knowledge-base directory.
- Side Effects: none; this is a read-only context assembly action.
- Expected Output Shape: `action="get_context"`, `success`, `message`, and `data` containing `kb_path`, `recommended_files`, `optional_areas`, and `missing_expected_files`.
- Safe Default Usage: safe for continuation, proactive read-side lookup, or context recovery once the relevant knowledge base is already determined. If more than one KB location is plausible, confirm which one to use.

### `atomic_knowledge_validate_kb`

- Purpose: run bounded structural validation over an existing knowledge base.
- Required Input: `kb_path` as an existing knowledge-base directory.
- Side Effects: no intended knowledge-base writes; this is a read-side validation action.
- Expected Output Shape: `action="validate_kb"`, `success`, `message`, `data` containing `kb_path`, `checked_files_count`, `missing_files`, and `missing_directories`, plus an optional `report` with `summary`, `warnings`, `issues`, and lightweight `details`.
- Safe Default Usage: safe for bounded inspection before or after an already authorized workflow, or when the user explicitly asks for health checking or maintenance review. A validation result does not by itself authorize the agent to repair, reorganize, or write back anything.

## Confirmation Boundary

- `atomic_knowledge_init_kb` is a write-capable tool.
- Even though `atomic_knowledge_init_kb` is a bounded setup action, it should not be called silently when user intent is unclear.
- Confirm first when the target directory already exists, when the directory choice is ambiguous, when the setup location may be outside the expected workspace, or when the action implies a broader directory or workspace decision.
- `atomic_knowledge_check_kb`, `atomic_knowledge_get_context`, and `atomic_knowledge_validate_kb` may be used as read-side or bounded inspection tools once the KB path is known.
- Read-side use of `check_kb`, `get_context`, or `validate_kb` should not be interpreted as automatic authorization for later writeback.

## Adapter Does Not Decide

The MCP adapter does not own semantic or authorization judgment. In particular, it does not decide:

- semantic interpretation of user intent
- durability judgment
- whether material belongs in `candidate`, `insight`, `project`, or another destination
- writeback authorization
- whether explicit confirmation is required for a high-impact follow-up action
- final synthesis or explanation to the user

Those remain the responsibility of `Protocol / Agent Judgment`.

## Safety Boundary

- The runtime and MCP tool call path are execution layers, not strategy layers.
- A successful tool result does not mean the agent should automatically continue to the next write step.
- A read-only tool result does not mean the user has agreed to writeback, promotion, merge, cleanup, or repair.
- The adapter should stay narrow and should not be expanded into a silent bulk maintenance surface.
- The adapter should not become an auto-promotion or implicit writeback surface.

## Usage Rule

- Prefer ordinary natural-language user intent over command-shaped user workflows.
- The agent should call MCP tools only when the protocol allows the underlying action.
- MCP tools improve execution stability for bounded steps, but they do not replace conservative autonomy, confirmation boundaries, or protocol judgment.
