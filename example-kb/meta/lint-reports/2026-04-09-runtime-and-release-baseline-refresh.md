---
type: lint-report
title: Runtime And Release Baseline Refresh
slug: runtime-and-release-baseline-refresh-2026-04-09
date: 2026-04-09
scope: entry-pages-candidates-and-fixture-health
reviewed_paths:
  - wiki/active.md
  - wiki/recent.md
  - wiki/index.md
  - wiki/log.md
  - wiki/projects/agent-memory-boundary.md
  - wiki/insights/candidates-should-stay-supplementary.md
  - meta/candidates/
  - meta/lint-status.json
---

# Runtime And Release Baseline Refresh

## Summary

- The example knowledge base still recovers cleanly from the entry pages and the main durable pages remain aligned around one active topic.
- The open candidate still belongs in the supplementary queue rather than being promoted into a standalone insight.
- Fixture metadata has been refreshed so the repository's runtime, MCP, CI, and validation baseline can be checked without stale-lint warnings.

## Findings

- [high] `wiki/active.md`, `wiki/recent.md`, `wiki/index.md`, and the current project/insight pages still point to the same live thread.
- [medium] [Candidate: Promotion Needs a Second Anchor](../candidates/candidate-promotion-needs-a-second-anchor.md) remains useful, but it still lacks a second durable anchor.
- [low] The fixture continues to represent a bounded work-memory example rather than a broad semantic memory system.

## Candidate Actions

- [Candidate: Candidates Should Stay Supplementary](../candidates/candidate-candidates-should-stay-supplementary.md) -> already promoted to [Candidates Should Stay Supplementary](../../wiki/insights/candidates-should-stay-supplementary.md)
- [Candidate: Promotion Needs a Second Anchor](../candidates/candidate-promotion-needs-a-second-anchor.md) -> keep open until another source or formal anchor arrives

## Recommended Updates

- Add another comparison source before turning the open candidate into a standalone insight.
- If the next source only sharpens the current thesis, merge the durable part into [Agent Memory Boundary](../../wiki/projects/agent-memory-boundary.md) instead of creating a new page.
- Refresh `wiki/recent.md` immediately when the open candidate is resolved.

## Follow-Up

The next maintenance pass should decide whether the open candidate has earned a second durable anchor. If not, merging it into the project page may still be cleaner than promotion.
