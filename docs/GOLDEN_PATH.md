# Golden Path

This document shows the smallest complete Atomic Knowledge loop:

1. the user shares new material
2. the agent ingests it into the knowledge base
3. the discussion produces a high-value judgment
4. that judgment enters `meta/candidates/` first
5. it is later promoted into formal wiki knowledge or merged into an existing page
6. a later session starts from `active/recent/index`
7. the agent continues the work instead of re-researching from scratch

## Scenario

Assume the knowledge base already contains an ongoing project:

- `wiki/projects/agent-memory-boundary.md`

The user has been comparing work-memory systems and wants to keep building on that thread across sessions.

## End-to-End Flow

### 1. User shares a new link

User message:

```text
I found this article about local-first agent memory. Ingest it and see whether it changes our current view.
```

Agent behavior:

- notice that this is not a one-off URL summary; it overlaps an ongoing research thread
- consult `wiki/active.md`, `wiki/recent.md`, and `wiki/index.md` first
- locate the existing project and any related insight pages before touching the new source

Why this matters:

- the agent frames the new source against existing work
- the ingest is attached to a live topic instead of becoming an isolated note

### 2. Agent ingests the source

The agent reads the article, extracts the key takeaways, and saves a source capture under `raw/sources/`.

Typical writeback after ingest:

- add `raw/sources/2026-04-06-local-first-agent-memory.md`
- update `wiki/projects/agent-memory-boundary.md` with the new source, the adjusted thesis, or a new open question
- refresh `wiki/recent.md` so the project shows up as newly updated
- refresh `wiki/index.md` so the source and related page stay discoverable
- update `wiki/active.md` if the source changes the current active questions

At this point the source is grounded, linked, and searchable. The knowledge base now reflects that the project has moved forward.

### 3. Discussion produces a high-value judgment

After the ingest, the conversation continues:

```text
It looks like the real difference is not just local-first storage.
The useful split is that formal wiki pages hold settled work memory, while candidate notes act as a review queue for unresolved but important judgments.
```

This is valuable because it changes how the project should be operated, but it is still too fresh to present as a settled insight.

### 4. The judgment becomes a candidate first

Instead of forcing that judgment directly into `wiki/insights/`, the agent creates a candidate note such as:

- `meta/candidates/candidate-treat-candidates-as-a-review-queue.md`

And updates:

- `meta/candidates/index.md`

Why it goes to `candidate` first:

- the idea has clear reuse value
- it is linked to a real project and source
- it still needs validation, cleanup, or a better final formulation

This is the key buffer step. The work-memory spark is not lost, but the formal wiki stays clean.

### 5. The candidate is resolved and promoted

Later in the same session or a future one, the agent validates the candidate against more sources and the existing project context.

If the judgment proves durable, the agent promotes it into formal knowledge, for example:

- add `wiki/insights/candidates-should-stay-supplementary.md`
- update `wiki/projects/agent-memory-boundary.md` so the project points to the new insight in `related_insights` or the body text
- refresh `wiki/recent.md`
- refresh `wiki/index.md`

The candidate note is then marked as resolved according to the lifecycle already defined by the protocol:

- `promoted` if it became a standalone insight
- `merged` if it only belonged inside an existing `project`, `concept`, or `entity`
- `dropped` if later work showed it had no lasting value

The important rule is that `candidate` is transitional. It is not the final destination.

### 6. A new session starts later

In a later session, the user says:

```text
Continue the memory-system design work. What should we tighten next?
```

Before broad search, the agent follows the normal retrieval order:

1. `wiki/active.md`
2. `wiki/recent.md`
3. `wiki/index.md`

That quickly surfaces:

- the still-active project `wiki/projects/agent-memory-boundary.md`
- the recently added insight `wiki/insights/candidates-should-stay-supplementary.md`
- any related sources or pages already linked from the index

Only then does the agent read the detailed project and insight pages it actually needs.

### 7. The agent continues from compiled knowledge

Because the previous session wrote back both the project update and the promoted insight, the new session does not need to rebuild the topic from raw articles.

The agent can now say things like:

- the current thesis is still X
- the new source strengthened Y
- one unresolved question is Z
- the next step is to validate whether another candidate should be promoted or merged

That is the real product behavior: future work begins from `what we have already figured out`, not from a blank page.

## File-Level Summary

The loop above usually touches these layers in order:

1. `raw/sources/` for source capture
2. `wiki/projects/` and possibly `wiki/insights/` for formal work-memory updates
3. `meta/candidates/` for provisional but valuable judgments
4. `wiki/active.md`, `wiki/recent.md`, and `wiki/index.md` as the retrieval entry points for later sessions

## Why This Is The Golden Path

- New material enters through ingest, not loose chat memory.
- High-value but unresolved thinking is preserved in `meta/candidates/` instead of being lost.
- Formal wiki pages stay reserved for durable knowledge.
- New sessions start from `active/recent/index`, then expand only where needed.
- The agent keeps advancing the same research thread rather than repeating the same summary work.
