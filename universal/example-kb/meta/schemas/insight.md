# Insight Page Schema

Use an insight page for a durable conclusion, comparison, synthesis, decision record, or reusable takeaway produced through research or discussion.

## When To Use

- a result should not disappear into chat history
- a comparison or synthesis will likely be reused later
- a discussion materially changes the current understanding of a topic or project

## Frontmatter

```yaml
---
type: insight
title: Candidates Should Stay Supplementary
slug: candidates-should-stay-supplementary
tags:
  - memory
  - retrieval
status: active
created: 2026-04-06
updated: 2026-04-06
confidence: high
sources:
  - path: raw/sources/research-notes.md
    date: 2026-04-06
derived_from:
  - wiki/projects/agent-memory-boundary.md
  - wiki/concepts/work-memory.md
related_projects:
  - wiki/projects/agent-memory-boundary.md
supersedes:
  - wiki/insights/raw-candidate-notes-can-answer-directly.md
superseded_by: []
---
```

## Field Notes

- `confidence`: use `low`, `medium`, or `high` for how settled the conclusion is right now
- `derived_from`: direct upstream pages or source captures that produced this insight
- `related_projects`: projects that should surface this insight during review or retrieval
- `supersedes` and `superseded_by`: only use these when one insight clearly replaces or corrects another

## Suggested Body

```markdown
# Candidates Should Stay Supplementary

## Summary

Short explanation of the durable takeaway.

## Why It Matters

Explain the practical or strategic significance.

## Evidence

- evidence point with citation
- evidence point with citation

## Caveats

- what is still uncertain

## Related Pages

- [[agent-memory-boundary]] - project that depends on this conclusion
- [[work-memory]] - broader framing this insight sharpens
```
