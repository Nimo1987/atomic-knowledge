# Candidate Lifecycle

This document explains why `meta/candidates/` exists, how a candidate moves through `open -> promoted / merged / dropped`, what each outcome means, what knowledge-base updates each outcome should trigger, and how to keep the candidate layer from turning into a dump of unresolved chat fragments.

Candidate capture and candidate resolution follow the same autonomy boundary as the rest of the protocol: the agent may suggest a candidate or a resolution proactively, but it should create or resolve notes only when the user asked to keep, save, promote, merge, drop, or run maintenance.

## Why Candidate Exists

`meta/candidates/` is a buffer for provisional but valuable work memory.

The buffer exists because real agent collaboration often produces material that clearly matters but is not yet ready for the formal wiki.
Typical examples include:

- a promising hypothesis that could change the current project thesis
- a reframing that might later deserve its own insight page
- a high-value open question that needs another source or another session to resolve
- a judgment that is linked to real pages and sources, but still needs validation or cleanup

Without a candidate layer, the agent faces a bad choice:

- write too early into `wiki/projects/`, `wiki/insights/`, `wiki/concepts/`, or `wiki/entities/`, which pollutes the formal wiki
- or leave the idea in chat, where it may be lost before the next session

Candidate notes solve that by acting as a transitional layer.
They preserve the work-memory spark without pretending it is already settled knowledge.

This is also why a candidate is not a first-class truth source.
It is supplementary working material that may still be revised, absorbed, or removed.

## Lifecycle

The lifecycle stays intentionally simple:

`open -> promoted | merged | dropped`

The point is not to model many intermediate states.
The point is to keep the note obviously provisional until the knowledge base decides what durable form, if any, it should take.

## `open`

`open` means the note is still provisional and unresolved.

An `open` candidate should already be worth keeping around.
It should not be a raw chat dump or a placeholder with no direction.

An `open` candidate should usually have:

- a concrete `why_it_matters`
- a specific `next_action`
- a clear `related_topic`
- direct grounding in `derived_from`

Before creating a new note, the agent should check `meta/candidates/index.md` and related open candidates first.
If the new material belongs to the same unresolved thread, updating the existing candidate is better than creating a near-duplicate.

Default review expectations:

- review an `open` candidate when it is used in an answer
- review it when its related formal pages materially change
- review it during lint
- review it no later than 7 days after its `created` or `updated` date
- treat it as stale after 14 days with no review, update, promote, merge, or drop

Example:

- after ingesting a new article, the agent notices a strong but still unproven judgment about how candidate notes should interact with lint; it creates an `open` candidate instead of immediately writing a new insight page

## `promoted`

`promoted` means the candidate has graduated into first-class formal knowledge.

This usually means one of two things:

- the candidate became a new standalone formal page, usually an `insight`
- the candidate drove a major formal page revision where the judgment now deserves durable, explicit treatment rather than remaining provisional

Promotion is the right outcome when the candidate itself has become a stable reusable unit.

Typical updates for `promoted`:

- update the candidate note with `status: promoted`, `updated`, `resolved_at`, `resolution_target`, and a short `resolution_note`
- update `meta/candidates/index.md`
- create or materially revise the destination formal page
- refresh `wiki/recent.md`
- refresh `wiki/index.md` when a new page was added or discoverability changed
- refresh `wiki/active.md` when the promoted result changes a live thesis, active project, or open question
- append a concise maintenance entry to `wiki/log.md`
- update `meta/lint-status.json`; because `promote` writes durable knowledge back into the formal wiki, update `last_writeback` as part of that maintenance pass

Example:

- `candidate-treat-candidates-as-a-review-queue.md` is validated across the active project and recent sources, then becomes `wiki/insights/candidates-should-stay-supplementary.md`

## `merged`

`merged` means the durable part of the candidate mattered, but it did not need to survive as its own first-class page.

This is the right outcome when the note mainly belongs inside an existing `project`, `insight`, `concept`, or `entity` page.
The candidate helped the agent get there, but the final durable form is an update to a page that already existed.

Typical updates for `merged`:

- update the candidate note with `status: merged`, `updated`, `resolved_at`, `resolution_target`, and a short `resolution_note`
- update `meta/candidates/index.md`
- update the destination formal page with the durable part of the note
- refresh `wiki/recent.md`
- refresh `wiki/active.md` when the merge changes a live thesis, active project, or open question
- refresh `wiki/index.md` only if discoverability changed
- append a concise maintenance entry to `wiki/log.md`
- update `meta/lint-status.json`; because `merge` writes durable knowledge back into the formal wiki, update `last_writeback` as part of that maintenance pass

Example:

- a candidate that tightens the current thesis for `wiki/projects/agent-memory-boundary.md` is folded into that project page rather than becoming a separate insight

## `dropped`

`dropped` means the note no longer deserves space in long-term work memory.

This does not mean the note was useless.
It means later review showed that it should not remain active knowledge material.

Common reasons to drop a candidate:

- the judgment was disproven or superseded
- the note turned out to be a one-session speculation with no durable reuse value
- the note duplicated a cleaner existing page and added no new durable knowledge
- the note should never have been a candidate because it was really temporary task state, persona material, or transcript-like residue

Typical updates for `dropped`:

- update the candidate note with `status: dropped`, `updated`, `resolved_at`, and a short `resolution_note`
- update `meta/candidates/index.md`
- update `wiki/active.md` or `wiki/recent.md` only if the dropped note had materially affected current work and that routing now needs cleanup
- append a concise maintenance entry to `wiki/log.md`
- update `meta/lint-status.json`

`dropped` usually does not need a `resolution_target` because nothing absorbed it.

Example:

- a candidate created from a fast debugging hunch is later judged to be one-off execution context rather than durable work memory, so it is marked `dropped`

## What Each Outcome Means For The Knowledge Base

The meaning of the outcomes is intentionally different:

- `promoted`: this idea is now durable enough to stand as formal knowledge
- `merged`: this idea mattered, but the durable destination was an existing page rather than a new first-class unit
- `dropped`: this idea should not continue occupying long-term work-memory space

That distinction is what keeps the candidate layer honest.
Every resolved candidate should tell the future reader whether the note became durable knowledge, fed a durable page, or was intentionally discarded.

## How To Keep Candidates From Becoming A Dumping Ground

Candidate quality is mostly maintained by disciplined intake and disciplined cleanup.

Use these rules:

- create a candidate only when the material changes direction, has clear reuse value, links to existing pages or sources, or forms a trackable open question
- do not store persona notes, raw transcripts, temporary task tracking, or casual speculation with no reusable structure
- check `meta/candidates/index.md` before creating a new note and prefer updating an existing candidate when the thread is already open
- keep `next_action` small and concrete so the note can realistically move toward resolution
- treat candidates as supplementary material in retrieval, not as the default authority for final conclusions
- when an answer materially depends on a candidate, suggest the next step toward `promote`, `merge`, or `drop` unless the user already asked to resolve it
- during lint, treat stale candidates as resolution work by default rather than carrying them forward indefinitely

The key principle is simple: candidates are a buffer, not a backlog target.
If the layer keeps growing without resolution, the maintenance workflow is not finished.
