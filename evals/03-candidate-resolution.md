# 03 Candidate Resolution

Use this scenario to verify that the agent can resolve an existing candidate note through a real lifecycle transition and update both the candidate layer and the formal wiki correctly.

This scenario uses `merge` as the concrete outcome because it tests whether the agent can fold durable material into an existing page instead of creating unnecessary new pages.

## Setup / Preconditions

- The target agent already has the Atomic Knowledge protocol installed or adapted.
- The knowledge base already contains at least one open candidate linked to a live topic.
- The user already knows which existing formal page should absorb the durable part.
- If you use `example-kb/`, the built-in open candidate is `meta/candidates/candidate-promotion-needs-a-second-anchor.md`, and the natural destination page is `wiki/projects/agent-memory-boundary.md`.

## What The User Says In Chat

Use a normal request such as:

`That open note about requiring a second anchor is useful, but it belongs in the current project rather than its own insight page. Merge the durable part into the project and close the candidate.`

This can also be phrased more casually, for example:

`Fold that open note into the project and resolve it.`

## Workflow The Agent Should Trigger

The primary workflow is `candidate resolution` with a `merge` outcome.

Expected behavior:

1. Read the candidate queue and the specific target note.
2. Read the destination formal page and any nearby pages needed to avoid duplicate or conflicting writeback.
3. Move the durable part into the destination page.
4. Mark the candidate as resolved through `merged`.
5. Refresh the candidate index and the relevant entry pages.
6. Record the maintenance and writeback result.

The agent should not leave the user to manually edit candidate metadata or close the note by hand.

## KB Files The Agent Should Read First

Read these first, in this order:

1. `meta/candidates/index.md`
2. the target `meta/candidates/<note>.md`
3. `wiki/active.md`
4. `wiki/recent.md`
5. the destination `wiki/projects/*.md` or other target formal page
6. any directly related `wiki/insights/*.md`, `wiki/concepts/*.md`, or `wiki/entities/*.md` needed to check for overlap and avoid duplication

If you are using `example-kb/`, the likely first reads are:

- `meta/candidates/index.md`
- `meta/candidates/candidate-promotion-needs-a-second-anchor.md`
- `wiki/active.md`
- `wiki/recent.md`
- `wiki/projects/agent-memory-boundary.md`
- `wiki/insights/candidates-should-stay-supplementary.md`

## Expected Files To Update

Minimum expected updates:

- the resolved `meta/candidates/<note>.md`
- `meta/candidates/index.md`
- the destination formal page, usually in `wiki/projects/` or `wiki/insights/`
- `wiki/recent.md`
- `wiki/log.md`
- `meta/lint-status.json` with `last_writeback`

Conditional but common updates:

- `wiki/active.md` if the live thesis or open questions changed
- `wiki/index.md` if discoverability links changed

## Pass / Fail Checklist

### Pass When

- The agent resolves the note through the requested lifecycle outcome rather than leaving it open.
- The candidate note receives real resolution metadata such as status and updated or resolved information.
- The durable material appears in the destination formal page.
- The candidate index reflects that the note is no longer open.
- The recent and bookkeeping pages are refreshed.
- The agent avoids creating a new standalone page when the request clearly called for a merge.

### Fail When

- The agent only talks about the resolution in chat and does not update the files.
- The agent creates a new insight page even though the user clearly asked for a merge into an existing page.
- The agent updates the formal page but forgets to resolve the candidate note or candidate index.
- The agent treats candidate resolution as a manual admin task instead of a normal conversation workflow.
- The agent skips the destination-page read and creates duplicate or conflicting content.
