# 01 Ingest And Writeback

Use this scenario to verify that the agent can ingest new material into an existing thread, route it to the right page type, and perform durable writeback inside an ordinary conversation.

## Setup / Preconditions

- The target agent already has the Atomic Knowledge protocol installed or adapted.
- The knowledge base already contains at least one active topic or project.
- Prepare one new source that overlaps an existing thread.
- The source can be a URL, article, paper, transcript, or local markdown file.
- If you use `universal/example-kb/`, choose a new source about agent memory, work memory, retrieval discipline, or a closely related comparison. It should be different from `raw/sources/2026-04-04-mem0-overview.md`.

## What The User Says In Chat

Use a normal request such as:

`Read this new article and add anything that changes our current view on work memory vs broader memory products. If it only sharpens the current thesis, update the existing pages instead of creating a duplicate.`

This can also be phrased more casually, for example:

`Please ingest this and connect it to what we already know.`

## Workflow The Agent Should Trigger

The primary workflow is `ingest`.

Because the new source overlaps an existing topic, the agent should also do proactive knowledge consultation before deciding where the material belongs.

Expected behavior:

1. Read the source.
2. Read the current entry pages and the relevant formal pages for the overlapping topic.
3. Extract the reusable takeaways.
4. Save a new capture in `raw/sources/`.
5. Update the existing `project`, `insight`, `concept`, or `entity` pages when the material is already stable enough.
6. Create or update a candidate note only if the source or surrounding discussion introduces valuable but still provisional work memory.
7. Refresh the routing and bookkeeping pages.

The agent should not push the user into a separate ingest UI, form, or slash-command ceremony.

## KB Files The Agent Should Read First

Read these first, in this order, and stop when the routing is clear:

1. `wiki/active.md`
2. `wiki/recent.md`
3. `wiki/index.md`
4. the directly relevant `wiki/projects/*.md`
5. the directly relevant `wiki/insights/*.md`
6. the directly relevant `wiki/concepts/*.md` and `wiki/entities/*.md`
7. `meta/candidates/index.md` only if the new material may need provisional capture rather than immediate formal writeback
8. existing related `raw/sources/*.md` only if comparison against earlier grounding is needed

If you are using `universal/example-kb/`, the most likely first reads are:

- `wiki/active.md`
- `wiki/recent.md`
- `wiki/index.md`
- `wiki/projects/agent-memory-boundary.md`
- `wiki/insights/candidates-should-stay-supplementary.md`
- `wiki/concepts/work-memory.md`
- `wiki/entities/mem0.md`

## Expected Files To Update

Minimum expected updates:

- one new file in `raw/sources/`
- at least one directly relevant formal wiki page
- `wiki/recent.md`
- `wiki/log.md`
- `meta/lint-status.json` with `last_ingest`, and `last_writeback` if durable knowledge changed

Conditional but common updates:

- `wiki/active.md` if the live thesis, current project framing, or open questions changed
- `wiki/index.md` if a new page was added or discovery links changed
- `meta/candidates/<note>.md` and `meta/candidates/index.md` if the source introduced provisional but reusable work memory

## Pass / Fail Checklist

### Pass When

- The agent understands the request as a normal ingest request and proceeds with low interruption.
- The agent consults the current knowledge base before deciding where to route the new material.
- The agent creates a source capture in `raw/sources/`.
- The agent updates existing relevant pages instead of creating obvious duplicates.
- The agent uses a candidate note only for unresolved but reusable material.
- The agent refreshes the expected routing and bookkeeping files.
- The user can inspect the filesystem afterward and see a real writeback result.

### Fail When

- The agent asks the user to switch modes, use a platform-specific command, or fill out a separate ingest workflow.
- The agent skips the knowledge-base lookup even though the source clearly overlaps an existing topic.
- The agent only gives a chat summary and performs no file writeback despite the explicit save intent.
- The agent dumps transcript-like material into the wiki instead of routing stable versus provisional knowledge correctly.
- The agent creates duplicate pages when an existing project or insight was the obvious destination.
