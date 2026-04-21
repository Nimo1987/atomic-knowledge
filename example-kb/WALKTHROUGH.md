# Example KB Walkthrough

Treat `example-kb/` as a tiny finished knowledge base that has already been used for a few sessions.

The point of this walkthrough is not to explain the whole protocol again. It is to show where to look first, what each page is doing, and how this example lines up with the acceptance scenarios in `evals/`.

## Best First Read

If you only want the fastest possible tour, read these pages in order:

1. [wiki/active.md](wiki/active.md)
2. [wiki/recent.md](wiki/recent.md)
3. [wiki/index.md](wiki/index.md)
4. [wiki/projects/agent-memory-boundary.md](wiki/projects/agent-memory-boundary.md)
5. [wiki/procedures/filesystem-first-query-flow.md](wiki/procedures/filesystem-first-query-flow.md)
6. [wiki/insights/candidates-should-stay-supplementary.md](wiki/insights/candidates-should-stay-supplementary.md)
7. [meta/candidates/index.md](meta/candidates/index.md)
8. [meta/lint-reports/2026-04-06-example-maintenance-pass.md](meta/lint-reports/2026-04-06-example-maintenance-pass.md)

That sequence answers the main questions a new user usually has:

- What topic is active right now?
- What changed most recently?
- Which pages matter?
- What is the current project thesis?
- Which reusable procedure should run?
- What conclusion is already durable?
- What is still unresolved?
- Has this KB actually been maintained?

## What You Are Looking At

This example has one central thread: Atomic Knowledge should behave like compiled `work memory`, not like a broad `remember everything` memory layer.

The pages are small, but together they show a complete lifecycle:

- [raw/sources/2026-04-04-mem0-overview.md](raw/sources/2026-04-04-mem0-overview.md): one grounded source capture
- [wiki/projects/agent-memory-boundary.md](wiki/projects/agent-memory-boundary.md): the live project thread
- [wiki/procedures/filesystem-first-query-flow.md](wiki/procedures/filesystem-first-query-flow.md): the reusable query playbook for continuation work
- [wiki/insights/candidates-should-stay-supplementary.md](wiki/insights/candidates-should-stay-supplementary.md): one promoted durable rule
- [meta/candidates/candidate-promotion-needs-a-second-anchor.md](meta/candidates/candidate-promotion-needs-a-second-anchor.md): one open unresolved note
- [meta/candidates/candidate-candidates-should-stay-supplementary.md](meta/candidates/candidate-candidates-should-stay-supplementary.md): one resolved candidate showing the promotion history
- [meta/lint-reports/2026-04-06-example-maintenance-pass.md](meta/lint-reports/2026-04-06-example-maintenance-pass.md): one maintenance pass showing cleanup and review behavior

That is why this fixture stays small but still feels complete.

## Page Roles

- [wiki/active.md](wiki/active.md): current projects, live comparisons, and open questions. Read this first when you need present-tense context.
- [wiki/recent.md](wiki/recent.md): newest changes. Read this next when you want to recover what happened lately.
- [wiki/index.md](wiki/index.md): broader catalog. Use it once you know the current thread and need the full page map.
- [wiki/projects/agent-memory-boundary.md](wiki/projects/agent-memory-boundary.md): the main project page. This is the best single page for understanding the current thesis.
- [wiki/procedures/filesystem-first-query-flow.md](wiki/procedures/filesystem-first-query-flow.md): the reusable query playbook that keeps retrieval entry-page-first and candidate-last.
- [wiki/insights/candidates-should-stay-supplementary.md](wiki/insights/candidates-should-stay-supplementary.md): the main durable conclusion already promoted from candidate to formal insight.
- [wiki/concepts/work-memory.md](wiki/concepts/work-memory.md): reusable definition of the target concept.
- [wiki/entities/mem0.md](wiki/entities/mem0.md): the comparison entity that sharpens the boundary.
- [meta/candidates/index.md](meta/candidates/index.md): the provisional queue. Read this when you are deciding whether there is unresolved material to promote, merge, refresh, or drop.
- [wiki/log.md](wiki/log.md): reverse-chronological record of ingest, promotion, and maintenance actions.

## Route 1: Ingest

Use this route when the user brings a new source that overlaps the same topic.

Read in this order:

1. [wiki/active.md](wiki/active.md)
2. [wiki/recent.md](wiki/recent.md)
3. [wiki/index.md](wiki/index.md)
4. [wiki/projects/agent-memory-boundary.md](wiki/projects/agent-memory-boundary.md)
5. [wiki/procedures/filesystem-first-query-flow.md](wiki/procedures/filesystem-first-query-flow.md)
6. [wiki/insights/candidates-should-stay-supplementary.md](wiki/insights/candidates-should-stay-supplementary.md)
7. [wiki/concepts/work-memory.md](wiki/concepts/work-memory.md)
8. [wiki/entities/mem0.md](wiki/entities/mem0.md)
9. [meta/candidates/index.md](meta/candidates/index.md) only if the new material feels valuable but still provisional
10. [raw/sources/2026-04-04-mem0-overview.md](raw/sources/2026-04-04-mem0-overview.md) only if you need to compare against the existing grounding

What this route demonstrates in the example:

- the KB already has one source and one active thread
- new material should usually update existing pages, not create duplicates
- reusable procedures sit between the project thesis and final conclusions
- candidate capture is available, but only for unresolved reusable judgments

Matching eval: [../evals/01-ingest-and-writeback.md](../evals/01-ingest-and-writeback.md)

## Route 2: Query / Continuation

Use this route when the user says things like `continue our earlier thread`, `based on our knowledge base`, or asks for a comparison or synthesis that should reuse existing work.

Read in this order:

1. [wiki/active.md](wiki/active.md)
2. [wiki/recent.md](wiki/recent.md)
3. [wiki/index.md](wiki/index.md)
4. [wiki/projects/agent-memory-boundary.md](wiki/projects/agent-memory-boundary.md)
5. [wiki/procedures/filesystem-first-query-flow.md](wiki/procedures/filesystem-first-query-flow.md)
6. [wiki/insights/candidates-should-stay-supplementary.md](wiki/insights/candidates-should-stay-supplementary.md)
7. [wiki/concepts/work-memory.md](wiki/concepts/work-memory.md) if the answer needs the definition layer
8. [meta/candidates/candidate-promotion-needs-a-second-anchor.md](meta/candidates/candidate-promotion-needs-a-second-anchor.md) only if the formal pages do not already settle the answer

What this route demonstrates in the example:

- formal wiki pages answer the main question
- reusable procedures keep the lookup path explicit instead of implicit
- the candidate layer is supplementary, not the first authority
- the answer should clearly separate settled pages from tentative notes

Matching eval: [../evals/02-research-query.md](../evals/02-research-query.md)

## Route 3: Candidate Resolution

Use this route when the user wants to resolve an existing candidate through `promote`, `merge`, or `drop`.

Read in this order:

1. [meta/candidates/index.md](meta/candidates/index.md)
2. [meta/candidates/candidate-promotion-needs-a-second-anchor.md](meta/candidates/candidate-promotion-needs-a-second-anchor.md)
3. [wiki/active.md](wiki/active.md)
4. [wiki/recent.md](wiki/recent.md)
5. [wiki/projects/agent-memory-boundary.md](wiki/projects/agent-memory-boundary.md)
6. [wiki/procedures/filesystem-first-query-flow.md](wiki/procedures/filesystem-first-query-flow.md)
7. [wiki/insights/candidates-should-stay-supplementary.md](wiki/insights/candidates-should-stay-supplementary.md) to avoid duplicating an already-settled rule

What this route demonstrates in the example:

- there is one open candidate ready for a real decision
- the natural destination is usually the project page, not a new insight page
- the procedure page helps check whether the candidate really belongs in an operating rule
- the resolved candidate example shows what a completed lifecycle looks like

Matching eval: [../evals/03-candidate-resolution.md](../evals/03-candidate-resolution.md)

## Route 4: Maintenance

Use this route before relying on the KB for a new synthesis, after several updates, or when the candidate queue may have gone stale.

Read in this order:

1. `meta/lint-status.json`
2. [wiki/active.md](wiki/active.md)
3. [wiki/recent.md](wiki/recent.md)
4. [wiki/index.md](wiki/index.md)
5. [wiki/projects/agent-memory-boundary.md](wiki/projects/agent-memory-boundary.md)
6. [wiki/procedures/filesystem-first-query-flow.md](wiki/procedures/filesystem-first-query-flow.md)
7. [wiki/insights/candidates-should-stay-supplementary.md](wiki/insights/candidates-should-stay-supplementary.md)
8. [meta/candidates/index.md](meta/candidates/index.md)
9. [meta/candidates/candidate-promotion-needs-a-second-anchor.md](meta/candidates/candidate-promotion-needs-a-second-anchor.md)
10. [meta/lint-reports/2026-04-06-example-maintenance-pass.md](meta/lint-reports/2026-04-06-example-maintenance-pass.md) if you need the prior baseline

What this route demonstrates in the example:

- maintenance is not just syntax checking
- entry pages, procedure pages, and candidate queue are reviewed together
- lint output becomes durable filesystem state, not just chat commentary

Matching eval: [../evals/04-maintenance-pass.md](../evals/04-maintenance-pass.md)

## Example KB To Eval Mapping

| Eval | Example KB anchor | Why it fits |
| --- | --- | --- |
| `01-ingest-and-writeback.md` | `wiki/projects/agent-memory-boundary.md`, `wiki/procedures/filesystem-first-query-flow.md`, `wiki/concepts/work-memory.md`, `wiki/entities/mem0.md` | There is already one active topic, so a new source has an obvious destination and a known retrieval path. |
| `02-research-query.md` | `wiki/active.md`, `wiki/recent.md`, `wiki/projects/agent-memory-boundary.md`, `wiki/procedures/filesystem-first-query-flow.md`, `wiki/insights/candidates-should-stay-supplementary.md` | These pages already settle both the retrieval path and the main rule. |
| `03-candidate-resolution.md` | `meta/candidates/candidate-promotion-needs-a-second-anchor.md` -> `wiki/projects/agent-memory-boundary.md` | The fixture already contains one open note with a natural merge target. |
| `04-maintenance-pass.md` | `meta/lint-status.json`, `meta/candidates/index.md`, `wiki/log.md`, `meta/lint-reports/2026-04-06-example-maintenance-pass.md` | The baseline maintenance artifacts already exist, so the user can rehearse a real pass. |

## If You Want The Smallest Useful Tour

Read only these six files:

1. [wiki/active.md](wiki/active.md)
2. [wiki/recent.md](wiki/recent.md)
3. [wiki/projects/agent-memory-boundary.md](wiki/projects/agent-memory-boundary.md)
4. [wiki/procedures/filesystem-first-query-flow.md](wiki/procedures/filesystem-first-query-flow.md)
5. [wiki/insights/candidates-should-stay-supplementary.md](wiki/insights/candidates-should-stay-supplementary.md)
6. [meta/candidates/index.md](meta/candidates/index.md)

That is the most compact path for understanding what the KB currently believes, which procedure it expects the agent to run, what is still open, and how the example should behave under the acceptance scenarios.
