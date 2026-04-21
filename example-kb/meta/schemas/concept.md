# Concept Page Schema

Use a concept page for a stable idea, framework, definition, method, or recurring abstraction.

## When To Use

- the same idea shows up across multiple sources, projects, or insights
- the user will likely need the concept again as a reusable lens
- the page is about the idea itself, not a named person, company, product, or ongoing project

## Frontmatter

```yaml
---
type: concept
title: Retrieval-Augmented Generation
slug: retrieval-augmented-generation
aliases:
  - RAG
tags:
  - llm
  - retrieval
status: active
created: 2026-04-06
updated: 2026-04-06
search_anchors:
  - compiled work memory
  - durable research context
key_entities:
  - Atomic Knowledge
  - Mem0
related_pages:
  - wiki/projects/agent-memory-boundary.md
  - wiki/insights/candidates-should-stay-supplementary.md
sources:
  - path: raw/sources/rag-overview.md
    date: 2026-04-06
---
```

## Field Notes

- `aliases`: alternate names worth searching or linking, not every casual synonym
- `search_anchors`: short search-like phrases that should help this page surface during retrieval
- `key_entities`: the named things most likely to co-occur with this concept in real queries
- `related_pages`: a short list of the most relevant connected pages, not a full graph
- `updated`: change this when the concept meaning, framing, or key links change

## Suggested Body

```markdown
# Retrieval-Augmented Generation

## Summary

1-2 paragraphs defining the concept in reusable terms.

## Core Points

- core idea
- practical boundary or caveat

## Related Pages

- [[agent-memory-boundary]] - where this concept matters now
- [[candidates-should-stay-supplementary]] - durable takeaway that depends on it
- [[mem0]] - comparison entity that sharpens the boundary
```
