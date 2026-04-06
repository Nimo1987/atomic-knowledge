# Example Knowledge Base

This is a small but realistic Atomic Knowledge fixture.

It is not a template. It is meant to feel like a real, already-used knowledge base that has gone through ingest, synthesis, candidate handling, and maintenance around one live topic: the boundary between `work memory` and broader memory products such as `mem0`.

The example intentionally stays small:

- 1 source capture in `raw/sources/`
- 1 active project in `wiki/projects/`
- 1 durable insight in `wiki/insights/`
- 1 concept and 1 comparison entity in `wiki/`
- 1 open candidate and 1 resolved candidate in `meta/candidates/`
- 1 maintenance report in `meta/lint-reports/`

## Start Here

If you are new to the repo, use this reading order:

1. [WALKTHROUGH.md](WALKTHROUGH.md)
2. [wiki/active.md](wiki/active.md)
3. [wiki/recent.md](wiki/recent.md)
4. [wiki/index.md](wiki/index.md)
5. [wiki/projects/agent-memory-boundary.md](wiki/projects/agent-memory-boundary.md)
6. [wiki/insights/candidates-should-stay-supplementary.md](wiki/insights/candidates-should-stay-supplementary.md)
7. [meta/candidates/index.md](meta/candidates/index.md)

That path gives you, in order: what is live now, what changed recently, where the pages are, what the main project believes, what durable rule has already been promoted, and what is still unresolved.

## Scenario Anchors

Use these pages as the main anchors for common workflows:

- `ingest`: start with [wiki/active.md](wiki/active.md), [wiki/recent.md](wiki/recent.md), [wiki/index.md](wiki/index.md), then the relevant formal pages under `wiki/`
- `query` / `continuation`: start with the same entry pages, then rely mainly on the project and insight pages; use candidate notes only if formal pages still leave a gap
- `candidate resolution`: start with [meta/candidates/index.md](meta/candidates/index.md), then the target candidate note and its destination formal page
- `maintenance`: start with `meta/lint-status.json`, then review `wiki/active.md`, `wiki/recent.md`, `wiki/index.md`, the relevant formal pages, and the candidate queue

## Use With `evals/`

This example is the easiest fixture for rehearsing the acceptance scenarios in [../evals/](../evals/):

- [01-ingest-and-writeback.md](../evals/01-ingest-and-writeback.md): add a second source to the existing `work memory` vs `mem0` thread
- [02-research-query.md](../evals/02-research-query.md): answer from the current record about whether candidates should stay supplementary
- [03-candidate-resolution.md](../evals/03-candidate-resolution.md): resolve the open candidate by merging or otherwise closing it correctly
- [04-maintenance-pass.md](../evals/04-maintenance-pass.md): run a real maintenance review against the entry pages, candidate queue, and existing lint artifacts

For the full route-by-route tour, read [WALKTHROUGH.md](WALKTHROUGH.md).

This example also includes a local `meta/schemas/` mirror so it behaves like a real installed knowledge base during walkthroughs, acceptance checks, and health-check runs.
