# 04 Maintenance Pass

Use this scenario to verify that the agent can perform a practical lint and candidate-review pass, then record the result in the knowledge base rather than leaving the maintenance outcome only in chat.

## Setup / Preconditions

- The target agent already has the Atomic Knowledge protocol installed or adapted.
- The knowledge base already contains entry pages, formal pages, and at least one candidate or recent writeback to review.
- If you use `universal/example-kb/`, the baseline maintenance artifacts are already present in `meta/lint-status.json`, `wiki/log.md`, and `meta/lint-reports/2026-04-06-example-maintenance-pass.md`.
- This scenario is especially useful when `last_lint` is older than 24 hours, several pages changed recently, or the user wants to rely on the knowledge base for a new synthesis or plan.

## What The User Says In Chat

Use a normal request such as:

`Before we rely on this for planning, run a maintenance pass. Check whether active, recent, index, and the open candidates still line up, and clean up anything stale.`

This can also be phrased more casually, for example:

`Do a lint pass and review the candidate queue before we continue.`

## Workflow The Agent Should Trigger

The primary workflow is `lint` or `maintenance`.

Expected behavior:

1. Read `meta/lint-status.json`.
2. Review the entry pages for discoverability and routing health.
3. Review the directly affected formal pages for contradictions, stale claims, or missing links.
4. Review `meta/candidates/index.md` and the relevant open candidate notes as a maintenance queue.
5. Resolve, refresh, or keep candidates open with a specific reason.
6. Record the maintenance result in the required bookkeeping files.

The agent should treat this as a real knowledge-base pass, not as a superficial syntax check and not as a separate admin UI flow.

## KB Files The Agent Should Read First

Read these first, in this order:

1. `meta/lint-status.json`
2. `wiki/active.md`
3. `wiki/recent.md`
4. `wiki/index.md`
5. the directly affected `wiki/projects/*.md`, `wiki/insights/*.md`, `wiki/concepts/*.md`, or `wiki/entities/*.md`
6. `meta/candidates/index.md`
7. the relevant open `meta/candidates/*.md`
8. prior lint reports only if they help compare what changed since the last maintenance pass

If you are using `universal/example-kb/`, the likely first reads are:

- `meta/lint-status.json`
- `wiki/active.md`
- `wiki/recent.md`
- `wiki/index.md`
- `wiki/projects/agent-memory-boundary.md`
- `wiki/insights/candidates-should-stay-supplementary.md`
- `meta/candidates/index.md`
- `meta/candidates/candidate-promotion-needs-a-second-anchor.md`

## Expected Files To Update

Required updates:

- `meta/lint-status.json`
- `wiki/log.md`

Updates when the pass finds real maintenance work:

- `wiki/active.md`
- `wiki/recent.md`
- `wiki/index.md`
- any corrected or relinked formal wiki pages
- `meta/candidates/index.md`
- any candidate notes that were refreshed, promoted, merged, or dropped

Optional update:

- a durable lint report such as `meta/lint-reports/<date>-<slug>.md`

## Pass / Fail Checklist

### Pass When

- The agent reads the maintenance freshness metadata first.
- The agent reviews entry pages and candidate queue as part of the same maintenance loop.
- The agent makes concrete decisions about stale or relevant candidates instead of leaving them as an untouched backlog.
- The agent records the maintenance result in `meta/lint-status.json` and `wiki/log.md`.
- The agent updates any touched routing or formal pages when the pass reveals a real inconsistency or cleanup need.
- The agent asks before making large structural changes beyond a normal maintenance pass.

### Fail When

- The agent treats lint as only a syntax or formatting check.
- The agent says the knowledge base looks fine without reviewing the candidate queue.
- The agent performs no bookkeeping updates after a real maintenance pass.
- The agent deletes or restructures large parts of the knowledge base without asking.
- The agent requires a platform-specific maintenance command or separate admin surface instead of handling the request in normal chat.
