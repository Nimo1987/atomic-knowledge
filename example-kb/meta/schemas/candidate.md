# Candidate Note Schema

Use a candidate note for provisional but valuable work memory that is not yet stable enough for the formal wiki.

A candidate is transitional work memory. It should stay lightweight and eventually end in `promoted`, `merged`, or `dropped`.

## When To Use

- a conversation produces a promising hypothesis, reframing, or open question with future reuse value
- the material clearly matters to an existing topic, but it still needs validation, synthesis, or cleanup
- writing it directly into `concept`, `entity`, `project`, or `insight` would be premature today

Do not use a candidate note for persona notes, raw transcript storage, or one-off task tracking.

## Lifecycle

`open -> promoted | merged | dropped`

Keep the state simple. The goal is to record whether the note is still provisional and, if it is no longer open, what resolved it.

## Frontmatter

```yaml
---
type: candidate
title: Candidate: Treat Candidates as a Review Queue
slug: candidate-treat-candidates-as-a-review-queue
status: open
created: 2026-04-06
updated: 2026-04-06
related_topic: agent-memory-boundary
derived_from:
  - wiki/projects/agent-memory-boundary.md
  - raw/sources/research-notes.md
why_it_matters: This would change how candidate cleanup and promotion are handled across the knowledge base.
next_action: Validate the idea against the lint workflow, then promote it into an insight or drop it.
---
```

When the candidate is resolved, add the smallest useful resolution metadata:

```yaml
resolved_at: 2026-04-09
resolution_target: wiki/insights/candidates-should-stay-supplementary.md
resolution_note: Promoted after review confirmed the judgment held across the related project and source notes.
```

## Field Notes

- `status`: use `open`, `promoted`, `merged`, or `dropped`
- `resolved_at`: add this when the candidate is no longer `open`
- `resolution_target`: the page path that absorbed or replaced the candidate; omit this when the outcome is simply `dropped`
- `resolution_note`: one short sentence explaining why the candidate was promoted, merged, or dropped
- `related_topic`: one primary topic, thread, or page path; keep secondary links in the body
- `derived_from`: direct source or page paths that triggered the note, not a raw chat dump
- `why_it_matters`: one sentence on why this note has reuse value
- `next_action`: the smallest next step that could resolve or advance the note; this is mainly for `open` candidates
- `updated`: refresh this when the note changes or when resolution metadata is added so stale candidates are easier to spot

## Suggested Body

```markdown
# Candidate: Treat Candidates as a Review Queue

## Summary

Short description of the provisional idea, judgment, or open question.

## Provisional Notes

- supporting point
- supporting point

## Open Questions

- what still needs to be checked

## Related Pages

- [[agent-memory-boundary]] - project this could update
- [[candidates-should-stay-supplementary]] - possible destination if validated

## Resolution

Use this only when the candidate is no longer open.

- outcome and why
- destination page if promoted or merged
```
