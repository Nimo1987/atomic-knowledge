# Lint Report Schema

Use a lint report for a human-readable maintenance pass over the knowledge base or one focused part of it.

This is a markdown-first review document, not a JSON-first machine report. Keep the metadata light and put the actual maintenance judgment in the body.

## When To Use

- a lint pass reviews freshness, structure, cross-links, duplicates, or candidate backlog
- the user needs a durable maintenance report that explains what was checked and what should change next
- the output should guide promotion, merge, drop, cleanup, or follow-up work

## Frontmatter

```yaml
---
type: lint-report
title: Candidate Maintenance Review
slug: candidate-maintenance-review-2026-04-06
date: 2026-04-06
scope: candidate-maintenance
reviewed_paths:
  - meta/candidates/
  - wiki/recent.md
  - wiki/projects/
---
```

## Field Notes

- `date`: the date of the review pass
- `scope`: a short label for what this report mainly reviewed
- `reviewed_paths`: only the paths actually checked during this pass
- keep findings, actions, and recommendations in markdown sections rather than encoding them as nested frontmatter data

## Suggested Body

```markdown
# Candidate Maintenance Review

## Summary

Short paragraph or 2-4 bullets describing the overall health of the reviewed area.

## Findings

- [high] Two candidate notes appear ready for promotion because the same judgment now shows up in the project page and recent source captures.
- [medium] `meta/candidates/index.md` still lists one candidate that was already merged into `wiki/projects/agent-memory-boundary.md`.
- [low] One project page links to a candidate but does not yet link to the newer insight that replaced it.

## Candidate Actions

- `candidate-treat-candidates-as-a-review-queue.md` -> promote to `wiki/insights/candidates-should-stay-supplementary.md`
- `candidate-keep-every-chat-fragment.md` -> drop because it does not meet the work-memory boundary
- `candidate-lint-should-surface-stale-notes.md` -> merge into `wiki/projects/agent-memory-boundary.md`

## Recommended Updates

- refresh `wiki/recent.md` after the promotion and merge pass
- update `wiki/projects/agent-memory-boundary.md` to point at the promoted insight
- remove stale candidate references from `meta/candidates/index.md`

## Follow-Up

Optional. Use this section for deferred checks, sequencing notes, or a suggested next lint pass.
```
