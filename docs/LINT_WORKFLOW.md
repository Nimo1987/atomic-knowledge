# Lint Workflow

This document explains what lint means in Atomic Knowledge, when it should run, what it should check, where the results should be recorded, and how stale candidate review participates in the same maintenance loop.

In this repository, lint is not just a syntax or schema check.
It is a practical knowledge-base maintenance pass over the markdown filesystem.
The goal is to keep the formal wiki trustworthy, the entry pages current, and `meta/candidates/` small enough to stay useful.

Reading lint freshness is a proactive behavior. Running a lint pass is still a writeback action, so the agent should suggest it when appropriate and execute it when the user asks for maintenance or another request clearly includes maintenance intent.

## What Lint Is For

Lint exists to keep the knowledge base usable as ongoing work memory rather than a pile of disconnected markdown files.

A lint pass should help the agent and user answer questions like:

- Are the current `project` and `insight` pages still consistent with newer sources and newer conclusions?
- Do `wiki/active.md`, `wiki/recent.md`, and `wiki/index.md` still point at the right things?
- Are there duplicate pages, missing cross-links, or orphaned pages that make retrieval worse?
- Are open candidates still worth keeping open, or should they now be promoted, merged, or dropped?

That makes lint a maintenance workflow for knowledge quality, freshness, and discoverability.

## Typical Triggers

Read `meta/lint-status.json` proactively.

Suggest lint when:

- `meta/lint-status.json` shows that `last_lint` is older than 24 hours
- the agent is about to rely on older `project` or `insight` pages for a new topic-level synthesis, recommendation, or roadmap

Run lint when the user explicitly asks whether the knowledge base is still clean, current, or internally consistent, or another request clearly includes maintenance intent, especially when:

- a batch ingest or several formal page updates changed the shape of the knowledge base
- multiple candidates were created, resolved, or left open in a short period
- candidate review or stale-note cleanup is already part of the requested work

Lint does not require a background worker.
The normal model is that the agent performs the pass during an ordinary session by reading timestamps, entry pages, formal pages, and candidate notes, then writing the maintenance results back to the filesystem.

## What A Lint Pass Checks

Lint can be broad or focused.
For example, one pass may review the whole knowledge base, while another may focus only on candidate maintenance for one active project.

Typical checks include:

- contradictions between pages
- stale claims that were superseded by newer sources or newer insights
- orphan pages with no meaningful inbound references
- missing pages for recurring concepts, entities, projects, procedures, or insights
- missing or weak cross-links
- index mismatches between the entry pages and the underlying wiki pages
- opportunities to merge near-duplicate pages
- open candidates that should no longer stay open

In practice, a useful lint pass usually reads at least:

- `meta/lint-status.json` for maintenance freshness
- `wiki/active.md`, `wiki/recent.md`, and `wiki/index.md` for discoverability and routing health
- the directly affected `project`, `procedure`, `insight`, `concept`, or `entity` pages for contradictions or stale claims
- `meta/candidates/index.md` and the relevant open candidate notes for cleanup decisions

## Where Lint Results Go

After an authorized lint pass, the maintenance result should be written back to the knowledge base rather than left only in chat.

Core writeback locations:

- `meta/lint-status.json`: update `last_lint`, increment `lint_count`, and recount `total_pages` and `total_sources` when feasible; if the lint pass also writes durable knowledge through a `promote` or `merge`, update `last_writeback` as well. Use `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SSZ`, or an ISO 8601 timestamp with an explicit UTC offset.
- `wiki/log.md`: add a concise record of what the lint pass checked and what concrete actions it took
- `wiki/active.md`: refresh it when the lint result changes a live thesis, active project, or open question
- `wiki/recent.md`: refresh it when the lint pass materially changes formal knowledge, especially after `promote` or `merge`, and after `drop` only if active work was materially changed
- `wiki/index.md`: refresh it when a new page was added or discoverability links changed
- touched formal pages: update any `project`, `procedure`, `insight`, `concept`, or `entity` page that was corrected, merged, or relinked during lint
- `meta/candidates/index.md`: refresh it whenever candidate status or candidate discoverability changed
- the candidate notes themselves: update `status`, `updated`, and any resolution metadata when a note is promoted, merged, or dropped

Optional writeback:

- a human-readable markdown lint report that follows the `lint-report` schema when the user wants a durable maintenance review or the pass is substantial enough to justify a separate report

The required maintenance record is still `meta/lint-status.json` plus `wiki/log.md`.
A dedicated lint report is an extra explanation layer, not a required replacement.

## Candidate Stale Review During Lint

Candidate cleanup is part of lint, not a separate system.

The protocol already defines the default review rules:

- review an `open` candidate when it is used in an answer, when its related formal pages change, during lint, or no later than 7 days after its `created` or `updated` date
- treat an `open` candidate as stale after 14 days with no review, update, promote, merge, or drop
- stale does not mean auto-delete; it means the next maintenance pass should resolve the note or explicitly refresh it

During lint, `meta/candidates/index.md` should be treated as a maintenance queue.
The agent should open the relevant candidate notes, look at `created`, `updated`, `next_action`, and their relationship to the current formal wiki, then decide whether the candidate should stay open.

Default handling for a stale candidate during lint:

- `promote` it if the judgment is now durable enough to become first-class formal knowledge
- `merge` it if the durable part belongs inside an existing `project`, `procedure`, `insight`, `concept`, or `entity` page
- `drop` it if it no longer has long-term reuse value
- keep it `open` only when it still clearly matters, and in that case refresh `updated` and tighten `next_action`

This rule is what keeps `meta/candidates/` from becoming a permanent backlog.

If the pass expands into deletes, archiving changes, bulk cleanup, large restructures, or directory changes, pause and get explicit confirmation before doing that higher-impact work.

## Practical Example

Assume the user has been iterating on `wiki/projects/agent-memory-boundary.md` across several sessions.
In the last two days, the agent has:

- ingested two new sources into `raw/sources/`
- updated one `project` page and one `insight` page
- created two new candidate notes in `meta/candidates/`

Before answering `Before we rely on this for planning, run a maintenance pass and tell me what we should tighten next.`, the agent runs a lint pass.

The pass might do this:

- read `wiki/active.md`, `wiki/recent.md`, and `wiki/index.md` to make sure the recent project, procedure, and insight updates are discoverable
- read the affected `project`, `procedure`, and `insight` pages to see whether any older wording now conflicts with the new source-backed conclusion
- review `meta/candidates/index.md` and the two open candidates
- merge one candidate into the existing project page because it only clarifies the current thesis
- drop the other because it turned out to be a one-session speculation with no durable reuse value
- record the maintenance pass in `wiki/log.md`
- update `meta/lint-status.json`

That is the intended workflow.
Lint keeps the formal wiki clean enough to trust, and it keeps candidates moving toward resolution instead of accumulation.
