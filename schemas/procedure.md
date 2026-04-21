# Procedure Page Schema

Use a procedure page for a recurring workflow, operating playbook, or durable decision rule that the user and agent should execute consistently.

## When To Use

- the same sequence keeps showing up across sessions
- the workflow should be reused instead of rediscovered from chat history
- the page is about how to operate, not only what is true

## Frontmatter

```yaml
---
type: procedure
title: Filesystem-First Query Flow
slug: filesystem-first-query-flow
tags:
  - retrieval
  - workflow
status: active
created: 2026-04-09
updated: 2026-04-09
search_anchors:
  - retrieval order
  - continue earlier topic
key_entities:
  - Atomic Knowledge
  - Mem0
related_pages:
  - wiki/projects/agent-memory-boundary.md
  - wiki/insights/candidates-should-stay-supplementary.md
---
```

## Field Notes

- `status`: usually `active` or `archived`
- `search_anchors`: short phrases the agent is likely to search or mentally map from the user's wording
- `key_entities`: named tools, products, or systems that should help this page surface during retrieval
- `related_pages`: only the most useful pages that help execute or justify the procedure

## Suggested Body

```markdown
# Filesystem-First Query Flow

## Summary

Short explanation of what this procedure is for and when it should be used.

## Triggers

- user wording that should activate the procedure
- situations where the procedure should not be skipped

## Steps

1. first step
2. second step
3. fallback step

## Guardrails

- what this procedure should not do
- what still requires extra confirmation

## Related Pages

- [[agent-memory-boundary]] - project this procedure supports
- [[candidates-should-stay-supplementary]] - insight that constrains the workflow
```
