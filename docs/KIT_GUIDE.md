# Kit Guide

This repository is the platform-neutral starter kit for Atomic Knowledge.

It is the portable protocol layer: a rendered `AGENT.md`, a markdown knowledge-base template, canonical schemas, and setup scripts that can work across agent systems.
It is meant to plug into an existing agent workflow, not to introduce a separate UI, dashboard, or command layer.

## What Atomic Knowledge Is For

Atomic Knowledge is a `work memory` system for long-term research collaboration.

It is built to preserve what the user and agent have already figured out together, connect it to source material, and reuse it across sessions and future projects.

It is not a persona-memory layer, a save-everything chat archive, or a place to store routine task state.

## What Gets Captured

Atomic Knowledge keeps value in three layers:

- `raw/sources/` captures external material in an immutable form
- `wiki/` captures compiled knowledge such as concepts, entities, projects, and insights
- `meta/candidates/` captures provisional but valuable work memory that is not stable enough for the formal wiki yet

Not every durable result starts as a document. Some of the most reusable material appears during comparison, synthesis, and discussion with the agent. That material should not disappear into chat history. Stable outcomes can be written into the wiki when the user asks to record them. Promising but unresolved outcomes should land in the candidate buffer until they can be promoted, merged, or dropped.

## Core Workflows

The public kit is built around three recurring workflows:

- `ingest`: capture a source in `raw/sources/` and update the formal wiki
- `query`: recover context through `active -> recent -> index -> relevant formal pages`
- `maintenance`: run lint, review candidate notes, and resolve them through `open -> promoted | merged | dropped`

See [LINT_WORKFLOW.md](LINT_WORKFLOW.md) for the maintenance loop and [CANDIDATE_LIFECYCLE.md](CANDIDATE_LIFECYCLE.md) for candidate review and resolution.

## Autonomy Boundary

The protocol is meant to feel low-interruption in normal chat, but the write boundary stays conservative:

- read proactively for continuation, context recovery, retrieval, and lint freshness checks
- suggest ingest, candidate capture, promote or merge, stale-candidate cleanup, or lint without writing by default
- treat clear natural-language record intent as write authorization, for example `ingest this link`, `save this as a candidate`, `merge this into the project`, or `run maintenance`
- ask explicitly before high-impact actions such as deletes, archiving, bulk cleanup, large restructures, or directory changes

Summarizing a link, paper, or note is not the same as ingesting it.

## Why The Entry Pages Matter

The protocol uses a small set of entry pages so new sessions can recover context without rereading the whole knowledge base:

- `wiki/active.md`: current projects, live comparisons, and open questions
- `wiki/recent.md`: recent additions, corrections, supersessions, and meaningful updates
- `wiki/index.md`: the broader catalog once the current thread is clearer

These are the primary retrieval entry pages, which is why the lookup model starts with `active -> recent -> index -> detailed pages`, instead of jumping straight into broad folder search.

`meta/candidates/index.md` is not part of that primary entry path. It is a supplementary review queue for provisional notes that may later be promoted, merged, or dropped, and it should be consulted only after the formal wiki is still insufficient.

## Design Position

This kit is intentionally markdown-first.

Markdown pages are the primary knowledge layer because they are portable, inspectable, editable by both users and agents, and easy to keep under version control. Small global metadata files such as `meta/lint-status.json` are fine, but the source of truth stays in the markdown knowledge base.

For the current stage, the protocol does not make a database the primary storage layer, and it does not require a sidecar JSON file for every page. That keeps the system simpler, more portable, and less fragile when the user edits knowledge directly. See `DESIGN_PRINCIPLES.md` for the rationale.

## What This Repository Contains

- `AGENT.md`: a platform-neutral protocol file for persistent agent instructions
- `docs/AGENT_NATIVE_USAGE.md`: how the protocol should behave inside an existing agent conversation
- `knowledge-base-template/`: a generic markdown knowledge-base skeleton
- `schemas/`: canonical page schemas for concepts, entities, projects, insights, and candidates
- `scripts/init-kb.sh`: initializes a knowledge base and renders a concrete `AGENT.md`
- `scripts/check-kb.sh`: an optional read-only local health check helper
- `example-kb/`: a small readable knowledge base that shows the model after ingest, query, and maintenance work
- `example-kb/WALKTHROUGH.md`: a guided tour of the example KB and how it maps to the eval scenarios
- `evals/`: acceptance scenarios for validating that an existing agent has really integrated the protocol
- `BOOTSTRAP_PROMPT.md`: a single prompt that users can paste into an agent with local file access and shell command support

## Install

Run:

```bash
bash scripts/init-kb.sh "$HOME/Desktop/My-Knowledge"
```

This creates a knowledge base at the target path and generates a concrete `AGENT.md` inside it.

This install path assumes the target agent or platform can read repository files, run local shell commands, and read or write the target knowledge-base directory.

It also copies the canonical page schemas into:

```text
<your-kb>/meta/schemas/
```

After that:

1. Open `<your-kb>/AGENT.md`.
2. Put its contents into the persistent instruction surface your agent platform supports.
3. If your platform does not support persistent instructions, tell the agent to read that file at the start of each new session.

This kit extends the agent you already use. See [AGENT_NATIVE_USAGE.md](AGENT_NATIVE_USAGE.md) for the expected low-interruption behavior in normal chat.

Optional read-only health check:

```bash
bash scripts/check-kb.sh "$HOME/Desktop/My-Knowledge"
```

The helper accepts `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SSZ`, and ISO 8601 timestamps with explicit UTC offsets in `meta/lint-status.json`.

Optional:

```bash
git init "$HOME/Desktop/My-Knowledge"
```

## Further Reading

- [AGENT_NATIVE_USAGE.md](AGENT_NATIVE_USAGE.md) for the agent-native, no-new-UI usage model
- [PLATFORM_INTEGRATION.md](PLATFORM_INTEGRATION.md) for the cross-agent integration model
- [GOLDEN_PATH.md](GOLDEN_PATH.md) for the end-to-end example flow
- [KNOWLEDGE_CONSULTATION.md](KNOWLEDGE_CONSULTATION.md) for retrieval triggers and lookup order
- [LINT_WORKFLOW.md](LINT_WORKFLOW.md) for maintenance and lint behavior
- [CANDIDATE_LIFECYCLE.md](CANDIDATE_LIFECYCLE.md) for candidate intake, review, and resolution
- [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) for the main design tradeoffs
- [../example-kb/](../example-kb/) for a directly readable example knowledge base
- [../example-kb/WALKTHROUGH.md](../example-kb/WALKTHROUGH.md) for the fastest guided tour through the example KB
- [../evals/README.md](../evals/README.md) for the acceptance scenarios that validate a real agent integration
- [../BOOTSTRAP_PROMPT.md](../BOOTSTRAP_PROMPT.md) for a one-shot setup prompt

## Recommended Mental Model

- raw sources are immutable inputs
- wiki pages are compiled knowledge
- candidate notes are a buffer, not a final truth layer
- the agent maintains the wiki with the user
- durable answers should be written back when the user asks to keep them instead of letting them disappear into chat history
