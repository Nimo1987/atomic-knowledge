# Atomic Knowledge

[中文说明](README.zh-CN.md)

Atomic Knowledge is a platform-neutral protocol for building agent-maintained work memory in markdown.

It is inspired by Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): instead of rediscovering knowledge from raw documents on every question, an agent incrementally maintains a persistent, interlinked markdown wiki.

Use your existing agent, but give it a maintained markdown work-memory layer that survives session resets and can be reused across future research threads.

## Why It Exists

- session resets make it hard for agents to reuse earlier research context reliably
- valuable judgments and synthesis often appear inside discussion, then disappear into chat history
- users end up re-sending old links, notes, and conclusions instead of continuing from prior work

## What It Is

Atomic Knowledge is for people who already use agents every day to:

- drop in links, notes, and source material
- ask questions and continue discussions across multiple sessions
- compare tools, ideas, and projects
- build up a long-running research context

What matters is not just the source itself, but the insight formed when sources and discussion are combined.

The goal is not to remember every chat message or capture a user persona.

The goal is to preserve durable work memory: reusable conclusions, comparisons, project context, and decision rationale that future sessions can build on.

## What It Is Not

Atomic Knowledge is not primarily:

- a persona-memory layer like mem0
- a chat-memory system or transcript archive
- a vector database
- a generic RAG stack
- a single-platform prompt pack

It is a source-grounded workflow and file protocol for maintaining shared work memory between a user and an agent.

Compared with mem0-style systems, it focuses on work memory rather than preferences, tone, or other persona memory.

Compared with ordinary RAG, it maintains a curated knowledge layer instead of only retrieving raw chunks at answer time.

## Who It Is For

Atomic Knowledge is a good fit if you:

- already use an agent for research, comparison, synthesis, or long-running project work
- want cross-session continuity without turning chat history into the source of truth
- are comfortable with a local markdown and filesystem workflow
- want something installable, inspectable, and portable rather than a hosted memory product

It is not the best fit if you want:

- a separate SaaS app or dashboard
- a chat-only environment with no local file access or shell execution
- a save-everything memory archive for all conversations

## Product Surface

This repository itself is the installable, platform-neutral product surface.

The root directory is meant to be the GitHub-distributed kit for cross-agent use.

## Current Status

Atomic Knowledge is currently an early open-source release.

Today it is:

- installable through a local bootstrap flow
- example-backed through `example-kb/`
- evaluable through `evals/`
- designed for agents that can read local files and run shell commands

## Autonomy Boundary

Atomic Knowledge is meant to work inside an ordinary agent chat, but its autonomy boundary stays conservative:

- read proactively for continuation, context recovery, retrieval, and lint freshness checks
- suggest ingest, candidate capture, promotion or merge, stale-candidate cleanup, or lint without writing by default
- treat clear natural-language record intent as write authorization, for example `ingest this link`, `save this as a candidate`, `merge this into the project`, or `run maintenance`
- ask explicitly before high-impact actions such as deletes, archiving, bulk cleanup, large restructures, or directory changes

Summarizing or analyzing a link is not the same as ingesting it.

## Quickstart

### Local install

```bash
bash scripts/init-kb.sh "$HOME/Desktop/My-Knowledge"
```

If you prefer a shorter alias, `init.sh` remains available as a convenience entrypoint.

This creates a new knowledge base and generates:

```text
$HOME/Desktop/My-Knowledge/AGENT.md
```

Then do one of these:

1. Put that file into your agent platform's persistent instruction surface.
2. If your platform has no persistent instruction surface, tell the agent to read that file at the start of each session.

Atomic Knowledge plugs into your existing agent workflow. It does not add a separate app, dashboard, or command surface.

See [Agent-Native Usage](docs/AGENT_NATIVE_USAGE.md) for the expected in-chat behavior.

### One-line bootstrap prompt

Copy the prompt in `BOOTSTRAP_PROMPT.md` into an agent that can read local files and run shell commands.

## Start Here

- [Kit Guide](docs/KIT_GUIDE.md) for installation and the portable kit structure
- [Agent-Native Usage](docs/AGENT_NATIVE_USAGE.md) for how the protocol fits into an existing agent conversation
- [Example Knowledge Base](example-kb/) and [Walkthrough](example-kb/WALKTHROUGH.md) for a small readable fixture and guided tour
- [Eval Scenarios](evals/README.md) for checking that an existing agent is actually integrated with the protocol
- [Optional Local Health Check](scripts/check-kb.sh) for a read-only KB structure and freshness check
- [Candidate Lifecycle](docs/CANDIDATE_LIFECYCLE.md) for how `meta/candidates/` moves through `open -> promoted | merged | dropped`
- [Lint Workflow](docs/LINT_WORKFLOW.md) for the maintenance loop that keeps the knowledge base clean and current

## Core Idea

Traditional RAG often works like this:

1. store raw files
2. retrieve chunks at query time
3. synthesize an answer from scratch

Atomic Knowledge inserts a maintained wiki between raw sources and answers:

1. raw sources are captured once
2. the agent compiles them, along with durable insights from the work around them, into wiki pages
3. future answers are built from the maintained knowledge layer
4. good answers and discussion insights can be written back as new knowledge when the user asks to keep them

This creates accumulation instead of repeated rediscovery.

## Repository Layout

```text
atomic-knowledge/
├── AGENT.md                  # portable agent protocol
├── BOOTSTRAP_PROMPT.md       # one-line install prompt for local-capable agents
├── README.md                 # repository overview
├── README.zh-CN.md           # Chinese overview
├── docs/                     # guides and protocol notes
├── evals/                    # agent integration acceptance scenarios
├── example-kb/               # small readable example knowledge base
├── schemas/                  # page schemas for all knowledge types
├── scripts/                  # init and health-check helpers
├── knowledge-base-template/  # template copied into a user KB
├── init.sh                   # optional convenience alias for the canonical initializer
├── CONTRIBUTING.md           # contributor guidance
├── AGENTS.md                 # repository maintenance instructions
└── LICENSE
```

## Knowledge Model

Atomic Knowledge uses a markdown knowledge base with these core objects:

- `raw/sources/` - immutable captures of source material
- `wiki/active.md` - current active projects, live comparisons, and open questions
- `wiki/recent.md` - recently created, updated, corrected, or superseded knowledge
- `wiki/index.md` - content-oriented catalog
- `wiki/log.md` - chronological record of ingests, queries, writebacks, and lint passes
- `wiki/concepts/` - stable ideas, methods, frameworks, definitions
- `wiki/entities/` - people, tools, companies, projects, named systems
- `wiki/projects/` - ongoing research threads and active workstreams
- `wiki/insights/` - durable takeaways, comparisons, decisions, and synthesis
- `meta/candidates/` - provisional work-memory notes that may later be promoted, merged, or dropped
- `meta/lint-status.json` - health and freshness metadata

`active.md` and `recent.md` are the entry pages for knowledge consultation. `projects` and `insights` remain the main durable work-memory layer. `meta/candidates/` is a supplementary buffer for promising but still provisional material, not a first-class truth source.

## Core Workflows

### Ingest

When the user asks to capture a source for future reuse, the agent:

1. reads the source
2. extracts key takeaways
3. stores a source capture in `raw/sources/`
4. creates or updates relevant wiki pages
5. updates `active.md`, `recent.md`, `index.md`, `log.md`, and metadata as needed

### Query

When the user asks a topic-level question, the agent:

1. reads `wiki/active.md`
2. reads `wiki/recent.md`
3. uses `wiki/index.md` to locate the relevant topic
4. reads the relevant `wiki/projects/` and `wiki/insights/` pages
5. adds `wiki/concepts/` and `wiki/entities/` only as needed
6. consults relevant `meta/candidates/` only if the formal wiki is still insufficient
7. answers with citations
8. offers writeback, or performs it only when the user's request already implies record intent

### Writeback

Write back only durable knowledge, such as:

- a useful comparison
- a stable framework
- a project thesis
- a reusable decision record
- a synthesis that will help future work

### Maintenance

Maintenance is a core workflow alongside ingest and query.

It keeps the knowledge base usable over time by:

- running lint passes over contradictions, stale claims, links, and index health
- treating `meta/candidates/` as a review queue rather than a permanent backlog
- resolving candidate notes through `open -> promoted | merged | dropped`

The agent may suggest maintenance proactively, but executing it is still a writeback workflow unless the user asked for it.

See [Lint Workflow](docs/LINT_WORKFLOW.md) for the maintenance loop and [Candidate Lifecycle](docs/CANDIDATE_LIFECYCLE.md) for candidate resolution rules.

## Cross-Agent Design

The root-level kit is designed to work across different agent platforms.

The integration pattern is simple:

1. initialize a knowledge base
2. render a concrete `AGENT.md` with the real path
3. install that protocol wherever the agent platform stores persistent instructions
4. if the platform cannot persist instructions, use the file as a startup protocol

See `docs/PLATFORM_INTEGRATION.md` for the integration model.

## Why Markdown

This project uses plain markdown because it is:

- human-readable
- diffable
- git-friendly
- easy for agents to search and edit
- portable across tools like Obsidian, editors, and local search engines

## Inspiration

- [Andrej Karpathy - LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Vannevar Bush - As We May Think (1945)](https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/)

## Thanks

Atomic Knowledge would not exist in its current form without Andrej Karpathy's [LLM Wiki note](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Thank you for the original framing and inspiration.

## License

MIT
