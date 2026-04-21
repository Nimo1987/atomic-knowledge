---
type: lint-report
title: Procedure And Retrieval Refresh
slug: procedure-and-retrieval-refresh-2026-04-21
date: 2026-04-21
scope: procedures-entry-pages-and-fixture-health
reviewed_paths:
  - wiki/active.md
  - wiki/recent.md
  - wiki/index.md
  - wiki/projects/agent-memory-boundary.md
  - wiki/procedures/filesystem-first-query-flow.md
  - wiki/insights/candidates-should-stay-supplementary.md
  - wiki/concepts/work-memory.md
  - wiki/entities/mem0.md
  - meta/candidates/
  - meta/lint-status.json
---

# Procedure And Retrieval Refresh

## Summary

- The fixture now includes a reusable procedure layer between the project thesis and the promoted insight.
- Entry pages, formal pages, and retrieval hints remain aligned around one active thread.
- The open candidate still stays open, but its `updated` date and next action were refreshed during this pass.

## Findings

- [high] [Filesystem-First Query Flow](../../wiki/procedures/filesystem-first-query-flow.md) makes the default continuation path explicit without turning retrieval into a heavy infrastructure layer.
- [medium] `search_anchors` and `key_entities` help narrow nearby pages, but they only work as hints because the markdown pages remain the truth layer.
- [medium] [Candidate: Promotion Needs a Second Anchor](../candidates/candidate-promotion-needs-a-second-anchor.md) still lacks the second durable anchor needed for promotion.

## Candidate Actions

- [Candidate: Promotion Needs a Second Anchor](../candidates/candidate-promotion-needs-a-second-anchor.md) -> kept open, refreshed `updated`, and tightened `next_action`
- [Candidate: Candidates Should Stay Supplementary](../candidates/candidate-candidates-should-stay-supplementary.md) -> already promoted to [Candidates Should Stay Supplementary](../../wiki/insights/candidates-should-stay-supplementary.md)

## Recommended Updates

- Add another grounded comparison source before deciding whether the open candidate becomes its own insight.
- If the next durable support is procedural rather than conceptual, merge the reusable part into [Filesystem-First Query Flow](../../wiki/procedures/filesystem-first-query-flow.md) instead of creating a new page.
- Keep retrieval hints short so they stay useful as page-level anchors rather than turning into a parallel tagging system.

## Follow-Up

The next maintenance pass should resolve whether the open candidate belongs in the project page, the procedure page, or a new insight after a second durable anchor appears.
