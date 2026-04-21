# Knowledge Consultation

This document explains when an agent should proactively consult the knowledge base, when it should not prioritize that lookup, and how deep it should read before answering.

The goal is not to force every request through the knowledge base. The goal is to make sure research continuity is recovered when it matters.

Consultation, continuation, context recovery, and retrieval are read-side behaviors. They should happen proactively when warranted, but they do not by themselves authorize ingest, writeback, promotion, merge, drop, or maintenance writes.

## Consult Proactively When

An agent should consult the knowledge base before answering when the request is likely to benefit from prior work-memory context.

Common triggers:

- the user is continuing an earlier topic, project, or open question
- the user asks for a comparison, recommendation, tradeoff analysis, judgment, roadmap, or synthesis
- the user shares a new link, paper, report, transcript, or notes that overlap an existing topic
- the request clearly belongs to an ongoing research thread rather than a one-off task
- prior conclusions, failed directions, or existing sources would materially improve the answer
- the agent is about to produce a topic-level conclusion, plan, or decision recommendation

Typical examples:

- `Continue the memory-system comparison from last week.`
- `Here is a new paper. Does it change our current thesis?`
- `Compare these two approaches and tell me which one fits our project better.`
- `Before you recommend a direction, check what we already learned.`

## Do Not Prioritize Lookup When

The agent should not force knowledge-base-first behavior when the task is immediate, local, or obviously unrelated to prior research.

Common non-triggers:

- simple syntax or API usage questions
- immediate debugging in the current repository, shell, logs, or runtime state
- one-off execution tasks with no broader continuity requirement
- requests that depend mainly on fresh real-time information unrelated to earlier work

Typical examples:

- `How do I parse JSON in Python?`
- `Why is this test failing in the current repo?`
- `Run this command and show me the output.`
- `What is the weather today in Shanghai?`

In these cases, a forced knowledge-base lookup adds latency without improving the answer.

## Recommended Retrieval Order

When consultation is triggered, use this order and stop when you already have enough context:

1. `wiki/active.md`
2. `wiki/recent.md`
3. `wiki/index.md`
4. relevant `wiki/projects/*.md`
5. relevant `wiki/procedures/*.md`
6. relevant `wiki/insights/*.md`
7. relevant `wiki/concepts/*.md` and `wiki/entities/*.md`
8. relevant `meta/candidates/*.md`

This order matters.

- `active.md` answers what is live right now.
- `recent.md` answers what just changed.
- `index.md` answers where the broader topic lives.
- `project` and `insight` pages hold the main reusable work memory.
- `procedure` pages hold reusable operating sequences and decision rules that should not be rediscovered in every session.
- `concept` and `entity` pages add definitional or named-thing context only after the main thread is known.
- `candidate` notes come last because they are supplementary working material, not the primary truth layer.

If several formal pages look plausible, the agent can use optional page-level hints such as `search_anchors` and `key_entities` to narrow the read set before opening more files.

The agent should not jump straight into a broad folder search unless the entry pages fail to narrow the path enough.

## Why Candidate Is Not A First-Class Truth Source

`meta/candidates/` exists to prevent valuable work-memory fragments from being lost, but it is intentionally not the same as formal wiki knowledge.

Reasons:

- a candidate may contain a promising hypothesis, reframing, or judgment that still needs validation
- a candidate can still end in `promote`, `merge`, or `drop`
- a candidate is allowed to be partial, recent, and unresolved in a way that `project` and `insight` pages should not be
- if candidates were treated as primary truth, provisional notes would outrank cleaner and more durable wiki pages

So the correct role of a candidate is:

- recover recent unresolved work
- surface a lead worth checking
- point the agent toward a project, procedure, insight, concept, entity, or source that needs confirmation

The incorrect role of a candidate is:

- serving as the only authority for a final answer
- replacing the need to update a real `project` or `insight` page
- becoming a permanent dumping ground for unresolved chat fragments

If an answer materially depends on a candidate, the agent should make that tentative status clear and, when appropriate, suggest the next step toward `promote`, `merge`, or `drop`.

## Practical Reading Depth

The knowledge base should be consulted with controlled depth, not maximum depth.

A practical pattern is:

1. read `active.md` and `recent.md` to see whether the topic is live or newly changed
2. use `index.md` to locate the right pages and sources
3. read only the directly relevant `project`, `procedure`, and `insight` pages
4. use optional `search_anchors` and `key_entities` hints when the topic could land in more than one page
5. add `concept/entity` pages only if terminology or named actors are still unclear
6. consult `candidate` notes only if the formal wiki still leaves an important gap

This keeps the agent from either missing context or reading the entire knowledge base on every research task.

## Example Decisions

Use the knowledge base first:

- `We already researched agent memory systems. Compare this new paper to our current view.`
- `Keep working on the packaging strategy and tell me what changed recently.`
- `We have discussed this company before. Should it change our roadmap?`

Do not force the knowledge base first:

- `Explain how git rebase works.`
- `Fix this TypeScript error in the current repo.`
- `Fetch today's exchange rate.`

The rule is simple: if the answer should benefit from prior compiled work memory, consult the knowledge base first. If the task is immediate and local, do not make the lookup mandatory.

If consultation surfaces a durable update worth preserving, offer the writeback unless the user already asked to record it.
