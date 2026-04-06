---
type: lint-report
title: Example Maintenance Pass
slug: example-maintenance-pass-2026-04-06
date: 2026-04-06
scope: entry-pages-and-candidates
reviewed_paths:
  - wiki/active.md
  - wiki/recent.md
  - wiki/index.md
  - wiki/projects/agent-memory-boundary.md
  - wiki/insights/candidates-should-stay-supplementary.md
  - meta/candidates/
---

# Example Maintenance Pass

## Summary

- Entry pages and detailed pages are aligned around one active topic, so a new session can recover context quickly.
- The promoted candidate is correctly linked to its destination insight and no longer appears in the open queue.
- One open candidate remains valuable but is still too narrow for promotion.

## Findings

- [high] `wiki/active.md`, `wiki/recent.md`, and `wiki/index.md` all surface the same live project and its main insight.
- [medium] [Candidate: Promotion Needs a Second Anchor](../candidates/candidate-promotion-needs-a-second-anchor.md) is useful, but it still depends on one active thread rather than broader confirmation.
- [low] The current comparison is anchored by one source capture, so the example should not over-claim beyond the work-memory boundary it already supports.

## Candidate Actions

- [Candidate: Candidates Should Stay Supplementary](../candidates/candidate-candidates-should-stay-supplementary.md) -> already promoted to [Candidates Should Stay Supplementary](../../wiki/insights/candidates-should-stay-supplementary.md)
- [Candidate: Promotion Needs a Second Anchor](../candidates/candidate-promotion-needs-a-second-anchor.md) -> keep open until another source or second formal anchor arrives

## Recommended Updates

- Add one more comparison source before turning the open candidate into a standalone insight.
- If the next source only sharpens the current thesis, merge the durable part into [Agent Memory Boundary](../../wiki/projects/agent-memory-boundary.md) instead of creating a new page.
- Refresh `wiki/recent.md` immediately when the open candidate is resolved.

## Follow-Up

The next maintenance pass should check whether the open candidate still deserves to stay open. If it remains single-threaded after another session, merging it into the project page may be cleaner than promotion.
