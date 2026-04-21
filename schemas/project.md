# Project Page Schema

Use a project page for an ongoing research thread, active workstream, or recurring topic that spans multiple sessions.

## When To Use

- the user is exploring a topic over time rather than solving a one-off task
- multiple sources, comparisons, or insights belong to the same thread
- there are open questions, hypotheses, or next steps worth revisiting

## Frontmatter

```yaml
---
type: project
title: Agent Memory Boundary
slug: agent-memory-boundary
tags:
  - memory
  - research
status: active
created: 2026-04-06
updated: 2026-04-06
search_anchors:
  - retrieval order
  - knowledge consultation
key_entities:
  - Atomic Knowledge
  - Mem0
current_thesis: Filesystem-first work memory is enough for the current stage if retrieval order and page maintenance stay disciplined.
open_questions:
  - When should a candidate be promoted instead of merged?
  - How should stale candidates be surfaced during lint?
related_insights:
  - wiki/insights/candidates-should-stay-supplementary.md
last_reviewed: 2026-04-06
---
```

## Field Notes

- `status`: use `active`, `paused`, or `archived`
- `search_anchors`: short phrases the user may ask with when this thread should be recovered
- `key_entities`: named tools, products, or systems that should help the project surface during retrieval
- `current_thesis`: the current best working view, short enough to scan quickly
- `open_questions`: unresolved questions that still change the direction of the work
- `related_insights`: the key insight pages this project currently depends on or produced
- `last_reviewed`: update this when the project gets a real pass even if the thesis does not change much

## Suggested Body

```markdown
# Agent Memory Boundary

## Summary

What this research thread is about and why it exists.

## Current Thesis

Current best synthesis or working thesis.

## Open Questions

- question
- question

## Related Insights

- [[candidates-should-stay-supplementary]] - guardrail for candidate usage

## Related Pages

- [[work-memory]] - core concept
- [[mem0]] - comparison target
- [[filesystem-first-query-flow]] - reusable operating sequence for retrieval

## Next Steps

- next action
```
