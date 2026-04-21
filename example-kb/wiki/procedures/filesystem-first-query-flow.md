---
type: procedure
title: Filesystem-First Query Flow
slug: filesystem-first-query-flow
tags:
  - retrieval
  - workflow
status: active
created: 2026-04-21
updated: 2026-04-21
search_anchors:
  - retrieval order
  - continue earlier topic
  - knowledge consultation
key_entities:
  - Atomic Knowledge
  - Mem0
related_pages:
  - wiki/projects/agent-memory-boundary.md
  - wiki/insights/candidates-should-stay-supplementary.md
  - wiki/concepts/work-memory.md
---

# Filesystem-First Query Flow

## Summary

Use this procedure when a user asks to continue an earlier topic, compare options based on prior work, or answer from the knowledge base. The goal is to recover compiled work memory through a small, predictable read path instead of broad file search.

## Triggers

- The user says `continue our earlier thread`, `based on our knowledge base`, or asks for a topic-level comparison.
- The answer would benefit from prior conclusions, open questions, or reusable operating rules.
- The task is not just a local syntax, API, or immediate debugging question.

## Steps

1. Read [active.md](../active.md), [recent.md](../recent.md), and [index.md](../index.md).
2. Open the most relevant [project](../projects/agent-memory-boundary.md) page.
3. Open the matching procedure or operating-rule page before broadening the search.
4. Read the relevant [insight](../insights/candidates-should-stay-supplementary.md), then add [concept](../concepts/work-memory.md) or [entity](../entities/mem0.md) pages only if they sharpen the answer.
5. Consult candidate notes only when the formal wiki still leaves a meaningful gap.

## Guardrails

- Do not skip the entry pages just because a folder search finds a plausible file name.
- Treat `search_anchors` and `key_entities` as narrowing hints, not as a replacement for reading the page.
- Do not present candidate notes as settled truth when the formal wiki already answers the question.

## Related Pages

- [Agent Memory Boundary](../projects/agent-memory-boundary.md)
- [Candidates Should Stay Supplementary](../insights/candidates-should-stay-supplementary.md)
- [Work Memory](../concepts/work-memory.md)
- [Mem0](../entities/mem0.md)
