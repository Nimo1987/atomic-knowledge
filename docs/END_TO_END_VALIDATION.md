# End-to-End Validation

This validation pass checks the current runtime, MCP adapter, tests, CI workflow, and `example-kb/` fixture against the acceptance bar implied by `evals/`.

## 1. Scope

This pass covers:

- chat-native bootstrap support
- runtime core actions: `init_kb`, `check_kb`, `get_context`, `validate_kb`
- MCP adapter surface for those runtime actions
- automated tests in `tests/`
- CI coverage in `.github/workflows/ci.yml`
- `example-kb/` as a real validation target
- mapping from current automation to the existing eval scenarios in `evals/`

Status legend:

- `Pass`: current runtime / MCP / tests / CI cover the capability directly
- `Partial`: some bounded automation exists, but the eval outcome still depends on agent judgment or extra manual behavior
- `Manual`: mainly documented or protocol-level behavior; not automatically guaranteed by the current runtime / MCP / tests

## 2. Validation Matrix

| Capability | Evidence | Status | Notes |
| --- | --- | --- | --- |
| bootstrap a KB | `scripts/init-kb.sh`; `runtime/service.py` `init_kb()`; `tests/test_runtime.py`; `tests/test_mcp_adapter.py`; `.github/workflows/ci.yml` init smoke step | Pass | Mechanical KB bootstrap is implemented and tested. This supports the preconditions for all eval scenarios, but bootstrap itself is not one of the eval scenarios. |
| health check a KB | `scripts/check-kb.sh`; `runtime/service.py` `check_kb()`; `tests/test_runtime.py`; `tests/test_mcp_adapter.py`; local run of `bash scripts/check-kb.sh example-kb` | Pass | Read-only structural and freshness-oriented health check exists and is exercised. This supports maintenance-oriented review in `evals/04-maintenance-pass.md`, but it is not a full semantic maintenance pass. |
| recover context from a KB | `runtime/service.py` `get_context()`; `tests/test_runtime.py`; `tests/test_mcp_adapter.py`; `docs/CHAT_NATIVE_JOURNEYS.md`; `evals/02-research-query.md` | Partial | The runtime can assemble a stable entry read set and list optional areas. It does not choose the topic-specific pages, cite them, or decide when candidate notes should be consulted, so the full eval behavior still depends on agent judgment. |
| structurally validate a KB | `runtime/service.py` `validate_kb()`; `tests/test_runtime.py` validate cases; `tests/test_mcp_adapter.py` validate tool call | Pass | Required files, required directories, and markdown frontmatter shape are checked automatically. This is bounded structural validation, not a contradiction, routing, or semantic-quality validator. |
| expose runtime actions through MCP | `adapters/mcp/server.py`; `adapters/mcp/README.md`; `docs/MCP_TOOL_CONTRACTS.md`; `tests/test_mcp_adapter.py` | Pass | The adapter exposes all four runtime actions through minimal JSON-RPC / MCP `tools/list` and `tools/call` handling. |
| run automated runtime tests | `tests/test_runtime.py`; local run of `python3 -m unittest discover -s tests -p 'test_*.py' -v` | Pass | Runtime tests cover success and failure paths for `init_kb`, `check_kb`, `get_context`, and `validate_kb`. |
| run automated MCP adapter tests | `tests/test_mcp_adapter.py`; local run of `python3 -m unittest discover -s tests -p 'test_*.py' -v` | Pass | MCP tests cover initialization, tool listing, tool dispatch, payload shape, and invalid request handling. |
| run CI checks | `.github/workflows/ci.yml`; local rerun of shell syntax checks, `compileall`, unit tests, `example-kb` check, and the init smoke path | Pass | CI coverage exists for the current runtime path. This pass reran the same command set locally; it did not execute a hosted GitHub Actions run. |
| preserve chat-native user entry | `README.md`; `docs/CHAT_NATIVE_JOURNEYS.md`; `evals/README.md` | Manual | This is clearly documented as a product boundary, and the eval suite expects it, but the runtime and MCP adapter do not automatically enforce host-level chat behavior. |
| enforce write-authorization boundaries | `README.md` autonomy boundary; `docs/MCP_TOOL_CONTRACTS.md`; `runtime/service.py`; `adapters/mcp/server.py` | Partial | The tool surface is narrow: `init_kb` is the only write-capable runtime action, while `check_kb`, `get_context`, and `validate_kb` are read-only. However, user-intent interpretation, confirmation for ambiguous setup, and high-impact follow-up approval are not enforced by code; they remain agent responsibilities. |
| eval 01: ingest and durable writeback | `evals/01-ingest-and-writeback.md`; current runtime only provides `check_kb`, `get_context`, and `validate_kb` support around the workflow | Manual | There is no runtime or MCP action that performs ingest, durable routing, raw source capture, or wiki writeback. The current stack can help before or after the write, but not replace the core agent behavior. |
| eval 02: research query from existing record | `evals/02-research-query.md`; `runtime/service.py` `get_context()`; `docs/CHAT_NATIVE_JOURNEYS.md` | Partial | The runtime helps with entry-page recovery, but the actual eval still requires agent-side relevance judgment, file reading order, citation, and synthesis. |
| eval 03: candidate resolution lifecycle | `evals/03-candidate-resolution.md`; current runtime / MCP action set | Manual | No runtime or MCP action currently resolves candidates through `promoted`, `merged`, or `dropped`, and no automated test covers that lifecycle. |
| eval 04: maintenance pass | `evals/04-maintenance-pass.md`; `scripts/check-kb.sh`; `runtime/service.py` `check_kb()` and `validate_kb()`; local `example-kb` check | Partial | Structural and freshness checks are automated, including candidate freshness signals. Actual maintenance decisions, writeback to bookkeeping files, and candidate resolution outcomes still depend on the agent. |
| example-kb validation path | `README.md`; `.github/workflows/ci.yml`; local run of `bash scripts/check-kb.sh example-kb` | Pass | The fixture now passes the shipped health check without warnings and remains usable as a deterministic validation target. |

## 3. What Is Actually Verified

This pass actually reran these checks:

- `bash -n scripts/init-kb.sh && bash -n scripts/check-kb.sh`
  - Result: passed
- `python3 -m compileall runtime adapters tests`
  - Result: passed
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
  - Result: passed, 18 tests
- `bash scripts/check-kb.sh example-kb`
  - Result: `PASS`
- CI-equivalent init smoke path
  - Result: passed

What this means in practice:

- the shell helpers are syntactically valid
- the Python runtime and MCP adapter import and compile cleanly
- runtime and MCP test coverage currently passes end-to-end
- the shipped `example-kb/` fixture is structurally and freshness-valid for the current health check baseline

## 4. Remaining Manual / Agent-Behavior Risks

The current runtime + MCP baseline does not fully automate these areas:

- semantic judgment
  - The system cannot automatically decide whether new material changes a thesis, duplicates an existing page, or should be ignored.
- durability judgment
  - The runtime does not decide what is durable enough for the formal wiki versus still provisional.
- candidate vs insight vs project routing
  - The current action set does not route or resolve material across `meta/candidates/`, `wiki/insights/`, and `wiki/projects/`.
- user intent interpretation
  - Natural-language mapping such as `please ingest this`, `continue our earlier thread`, or `run maintenance` is still agent behavior, not runtime policy.
- high-impact confirmation boundaries
  - Confirmation rules are documented, but code does not enforce when the agent must pause before a broader write, restructure, archive, or cleanup step.
- chat-native behavior consistency across different agent hosts
  - The repository documents the expected behavior, but there is no cross-host automated acceptance harness in CI proving the same conversation-native behavior across different MCP or instruction hosts.
- citation and synthesis quality
  - `get_context()` can suggest a read set, but the answer quality, citation discipline, and distinction between formal and provisional material remain agent responsibilities.
- maintenance outcome recording
  - `check_kb` and `validate_kb` can surface issues, but they do not update `wiki/log.md`, `meta/lint-status.json`, or candidate states by themselves.

## 5. Final Verdict

The current repository does provide a usable agent-facing runtime + MCP baseline for bounded mechanical actions: bootstrap, health check, context bootstrap, and lightweight structural validation.

It does not yet fully automate the conversation-native eval behaviors around ingest, semantic retrieval, candidate lifecycle resolution, maintenance judgment, or write authorization. Those boundaries remain explicitly dependent on agent behavior and user-confirmed protocol judgment.
