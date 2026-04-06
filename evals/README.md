# Agent Acceptance Scenarios

This directory provides a small acceptance suite for validating that an existing agent has actually integrated the Atomic Knowledge protocol.

The suite assumes the following pieces already exist and are treated as the prerequisite baseline:

- `AGENT.md`
- `BOOTSTRAP_PROMPT.md`
- `docs/AGENT_NATIVE_USAGE.md`
- `docs/KNOWLEDGE_CONSULTATION.md`
- `docs/LINT_WORKFLOW.md`
- `docs/CANDIDATE_LIFECYCLE.md`
- `example-kb/`

## What This Suite Verifies

These scenarios are meant to answer one question:

Can the user's existing agent behave like an Atomic Knowledge agent inside an ordinary conversation, with filesystem-backed work-memory updates, without requiring a separate UI or platform-specific command layer?

The scenarios are intentionally conversation-native.
They are not UI automation tests, button-click scripts, or slash-command demos.

## How To Use This Suite

1. Install or adapt the protocol into the target agent using the normal repository instructions.
2. Point the agent at a real Atomic Knowledge base.
3. Run one scenario at a time by saying the natural-language prompt in chat.
4. Inspect what the agent actually read and what the knowledge base actually changed.
5. Judge the run using the pass and fail checklist in the scenario file.

## Recommended Test Surface

You can run these scenarios against either:

- your own installed knowledge base
- `example-kb/` as a small deterministic fixture

If you use your own knowledge base, substitute equivalent pages for the example paths mentioned below.

## Example KB Mapping

If you rehearse against `example-kb/`, these are the closest built-in anchors:

- active project: `wiki/projects/agent-memory-boundary.md`
- durable insight: `wiki/insights/candidates-should-stay-supplementary.md`
- main concept: `wiki/concepts/work-memory.md`
- comparison entity: `wiki/entities/mem0.md`
- open candidate: `meta/candidates/candidate-promotion-needs-a-second-anchor.md`
- candidate index: `meta/candidates/index.md`
- maintenance baseline: `meta/lint-status.json`, `wiki/log.md`, and `meta/lint-reports/2026-04-06-example-maintenance-pass.md`

The example fixture includes a local `meta/schemas/` mirror, so it behaves like a real installed knowledge base during acceptance rehearsals.

## Evaluation Principles

- The user should speak in ordinary language.
- The agent should map clear intent to the right workflow with low interruption.
- The agent should consult the knowledge base in the documented retrieval order when prior work-memory context matters.
- The agent should write durable knowledge back to files when the user's request clearly implies it.
- Candidate notes should stay supplementary and should not silently outrank formal wiki pages.
- Maintenance should be a real knowledge-base pass, not a vague "looks fine" response.

## Scenario Index

| File | Core Behavior Under Test |
| --- | --- |
| `01-ingest-and-writeback.md` | Ingest new material, route it correctly, and update durable knowledge without a separate workflow UI. |
| `02-research-query.md` | Recover prior context before answering a research question and cite the right files. |
| `03-candidate-resolution.md` | Resolve an existing candidate through a real lifecycle transition and update the right pages. |
| `04-maintenance-pass.md` | Run a practical lint and candidate-review pass, then record the maintenance result. |

## Pass Standard For The Whole Suite

An agent has passed this suite when it can repeatedly do all of the following in normal chat:

- recognize the intended workflow from natural language
- read the right knowledge-base files before acting
- keep stable wiki knowledge distinct from provisional candidate material
- update the expected files with minimal ceremony
- avoid platform-specific slash commands, dashboards, or mode switches

That is the acceptance bar for "the existing agent is integrated with the protocol," not merely "the agent can explain the protocol in words."
