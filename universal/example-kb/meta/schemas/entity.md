# Entity Page Schema

Use an entity page for a named thing: person, company, product, tool, dataset, institution, or named system.

## When To Use

- the same named thing appears across multiple sources or projects
- the entity needs its own facts, role, or comparison context
- future work will likely refer to it again by name

## Frontmatter

```yaml
---
type: entity
title: Mem0
slug: mem0
aliases:
  - mem0.ai
tags:
  - memory
  - product
status: active
created: 2026-04-06
updated: 2026-04-06
related_pages:
  - wiki/projects/agent-memory-boundary.md
  - wiki/insights/work-memory-is-not-persona-memory.md
sources:
  - path: raw/sources/mem0-overview.md
    date: 2026-04-06
---
```

## Field Notes

- `aliases`: alternate spellings, brand names, or short names worth preserving
- `related_pages`: only the pages that matter most for reuse or comparison
- `status`: usually `active` or `archived`; keep it simple unless the entity truly stops mattering

## Suggested Body

```markdown
# Mem0

## Summary

Short description of what it is and why it matters.

## Key Facts

- what it is
- role in the current research landscape

## Related Pages

- [[agent-memory-boundary]] - ongoing comparison thread
- [[work-memory-is-not-persona-memory]] - boundary this entity helps clarify
```
