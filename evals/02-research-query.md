# 02 Research Query

Use this scenario to verify that the agent can recover prior work-memory context before answering a research question, and that it treats formal wiki pages as the primary authority during retrieval.

## Setup / Preconditions

- The target agent already has the Atomic Knowledge protocol installed or adapted.
- The knowledge base already contains an active project or reusable research thread.
- The user asks a continuation, comparison, recommendation, tradeoff, or synthesis question that should benefit from prior work-memory context.
- If you use `example-kb/`, the natural topic is the boundary between compiled work memory and broader memory products.

## What The User Says In Chat

Use a normal request such as:

`We already worked on this topic. Based on what is in our knowledge base, should candidate notes stay supplementary during retrieval, or should they become equal sources? Please answer from the existing record and cite the files you rely on.`

This can also be phrased more loosely, for example:

`Continue our earlier thread and tell me what we currently believe.`

## Workflow The Agent Should Trigger

The primary workflow is `query` with proactive knowledge consultation.

Expected behavior:

1. Recover context from the knowledge base before answering.
2. Read entry pages first, then the directly relevant formal pages.
3. Use candidate notes only if the formal wiki still leaves an important gap.
4. Answer with explicit file citations.
5. Keep stable wiki-backed conclusions separate from tentative candidate-backed clues.

The agent should not stop to ask `Should I check the knowledge base first?` when the continuation signal is already obvious.

## KB Files The Agent Should Read First

Read these first, in this order, and stop when the answer is grounded enough:

1. `wiki/active.md`
2. `wiki/recent.md`
3. `wiki/index.md`
4. the directly relevant `wiki/projects/*.md`
5. the directly relevant `wiki/insights/*.md`
6. the directly relevant `wiki/concepts/*.md` and `wiki/entities/*.md` only if needed
7. relevant `meta/candidates/*.md` only if the formal wiki is still insufficient

If you are using `example-kb/`, the likely path is:

- `wiki/active.md`
- `wiki/recent.md`
- `wiki/index.md`
- `wiki/projects/agent-memory-boundary.md`
- `wiki/insights/candidates-should-stay-supplementary.md`
- `wiki/concepts/work-memory.md`
- `meta/candidates/candidate-promotion-needs-a-second-anchor.md` only if the formal pages do not already settle the answer

## Expected Files To Update

Default expectation:

- no filesystem writeback is required for this scenario

Optional but acceptable writeback:

- `wiki/log.md` if the implementation records durable query events

This scenario should still pass with no file modifications if the answer is fully grounded in existing pages and the user did not clearly request writeback.

## Pass / Fail Checklist

### Pass When

- The agent recognizes the message as a continuation or synthesis request.
- The agent consults the knowledge base before answering.
- The agent follows the documented retrieval order rather than jumping straight to broad search or candidate notes.
- The answer cites the files that ground the conclusion.
- The answer clearly distinguishes settled formal knowledge from any still-open candidate material.
- The agent keeps the interaction low interruption and does not force a separate protocol ceremony.

### Fail When

- The agent answers from scratch without consulting the knowledge base.
- The agent treats an open candidate as settled truth when the formal wiki already provides the main answer.
- The agent relies on external web research first even though the question is clearly about prior internal work.
- The agent insists on unnecessary writeback for a normal research query that did not request it.
- The answer has no file grounding or collapses formal and provisional material into one undifferentiated conclusion.
