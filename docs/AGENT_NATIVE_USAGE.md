# Agent-Native Usage

This document explains how Atomic Knowledge should behave inside an existing agent conversation.

Atomic Knowledge is not a separate UI, chat mode, dashboard, or memory window.
It is a work-memory protocol that plugs into the user's existing agent workflow.
The user keeps talking to the same agent in normal language.
The agent reads proactively, but writes and maintenance stay consent-based.

## Core Expectation

The user should not need a new control surface to use the system.

- no separate memory app
- no required mode switch
- no requirement to learn special commands
- no expectation that every message becomes stored knowledge

The normal model is:

1. the user talks to the agent in ordinary language
2. the agent recognizes when the message implies `ingest`, continuation, candidate capture, candidate resolution, or maintenance
3. the agent performs the right filesystem-backed protocol actions with minimal interruption

The protocol terms are internal. Users should not need to memorize words like `candidate` or `insight` in order to use the system.
Prefer the user's current conversation language first. If that is unclear, fall back to the user's system language or another durable language preference signal.

## Autonomy Boundary

Atomic Knowledge should feel low-interruption, but the autonomy boundary is intentionally conservative:

- read proactively for continuation, context recovery, retrieval, and lint freshness checks
- suggest ingest, candidate capture, promotion or merge, stale-candidate cleanup, or lint without writing by default
- treat clear natural-language record intent as write authorization, for example `ingest this link`, `save this as a candidate`, `merge this into the project`, or `run maintenance`
- ask explicitly before high-impact actions such as deletes, archiving, bulk cleanup, large restructures, or directory changes

Summarizing or discussing a link is not the same as ingesting it.

## Natural-Language Triggers

These are typical ways a normal user may trigger the protocol without using special syntax.

| What the user says | Implied action |
| --- | --- |
| `Read this paper and add the important parts to our knowledge base.` | `ingest` |
| `We discussed agent memory systems last week. Continue from there.` | continuation plus proactive knowledge consultation |
| `This feels like the real takeaway. Keep track of it, but I am not sure it is stable yet.` | candidate capture |
| `That open note is now solid. Turn it into a proper insight.` | candidate resolution through `promote` |
| `Fold that tentative note into the current project page.` | candidate resolution through `merge` |
| `That idea did not hold up. Remove it from active work memory.` | candidate resolution through `drop` |
| `Before we keep going, clean up stale notes and check whether the wiki is still consistent.` | maintenance / lint |

The key point is that the user is not talking to a new subsystem.
They are just asking their usual agent to remember, continue, organize, and maintain shared work memory.

## Chinese Plain-Language Aliases

If the user is speaking Chinese, the agent should map ordinary Chinese phrases onto the same internal workflows. The same rule applies to any other language: prefer the language already used in the current conversation, and fall back to system language only when needed. The user should not need to say `candidate`, `insight`, `promote`, or `merge`.

| 用户自然会说的话 | 内部应映射到什么 |
| --- | --- |
| `把这个链接收进去。` | `ingest` |
| `继续我们上次聊的。` | continuation plus proactive knowledge consultation |
| `这个先记一下，先别当正式结论。` | candidate capture |
| `这个已经比较确定了，正式记下来。` | candidate resolution through `promote` or another durable writeback |
| `把这个并到之前那个主题里。` | candidate resolution through `merge` |
| `这个不成立了，先不要留着了。` | candidate resolution through `drop` |
| `整理一下知识库。` | maintenance / lint |
| `看看知识库健不健康。` | health check or lint |

The practical rule is simple:

- users should say the most natural thing in their own language
- the agent should quietly map that onto the internal workflow
- protocol words should appear only when they help explain what happened after the fact

Not every strong statement inside the conversation is a write request. If the user is only discussing, summarizing, or analyzing something, the agent may suggest capture or maintenance, but it should not persist it yet.

## In Ordinary Chat

### Ingest

The user may trigger ingest with ordinary requests such as:

- `Read this article and add anything reusable to our research notes.`
- `Here is the transcript from yesterday's talk. Ingest it and connect it to our current project.`
- `Please save this paper into the knowledge base and update anything it changes.`

The agent should treat these as normal conversation requests, not as a handoff into a separate UI flow.

Expected behavior:

1. read the source
2. extract key takeaways
3. confirm emphasis only when the source is substantial or the intended angle is ambiguous
4. save the source into `raw/sources/`
5. update the relevant formal pages when the material is stable enough
6. create or update a candidate note if the discussion also produces valuable but still provisional work memory

Low-interruption response style:

- if the user explicitly asked to add or save the material, proceed directly
- if the intent is probably research reuse but not fully explicit, ask one short confirmation question instead of starting a long ceremony
- answering questions about a link, summarizing it, or translating it is not itself ingest
- do not offer ingest for package docs, troubleshooting links, logs, or one-off bug material unless the user clearly wants long-term reuse

Good response pattern:

`I can ingest this and connect it to the current project. If it changes our thesis, I will update the relevant project or insight pages as well.`

Bad response pattern:

`Please open the ingest panel, select a source type, choose a destination page, and confirm writeback.`

### Continuation

The user may trigger continuation with phrases such as:

- `Continue the packaging strategy discussion from last week.`
- `Pick up where we left off on the agent-memory boundary.`
- `We already looked into this company. What changed?`
- `Before answering, check what we already learned about this topic.`

When continuation is obvious, the agent should proactively consult the knowledge base before answering.
That consultation is a read-side behavior, not implicit authorization to write anything back.
It should use the normal retrieval order:

1. `wiki/active.md`
2. `wiki/recent.md`
3. `wiki/index.md`
4. relevant `project` and `insight` pages
5. relevant `concept` and `entity` pages only if needed
6. relevant `candidate` notes only if the formal wiki is still insufficient

Low-interruption response style:

- do not ask `Should I check the knowledge base first?` when the continuation signal is already clear
- silently recover context, then answer from that context
- ask a brief clarifying question only when the referent is ambiguous, such as when `continue that thread` could point to more than one active project

Good response pattern:

`Picking up from our existing work on this topic, the current thesis is still X, and the most recent change is Y. Based on that, here is what I think next.`

### Candidate Capture

Candidate capture is for high-value work memory that matters, but is not yet stable enough for the formal wiki.
It still requires record intent.

Ordinary user phrases that may authorize candidate capture:

- `Keep this thought around. It could change the project direction.`
- `I am not ready to call this a conclusion yet, but we should not lose it.`
- `Save this as a tentative note linked to the current project.`
- `Keep this as a candidate until we validate it.`

A statement like `This might be the real reason the current approach feels wrong.` may justify suggesting a candidate, but by itself it is not authorization to write.

These are not requests for transcript storage.
They are natural-language requests to preserve a reusable judgment, reframing, or unresolved question.

Expected behavior:

1. decide whether the material crosses the work-memory threshold
2. check whether an existing open candidate already covers the same unresolved thread
3. create or update a note in `meta/candidates/` when the material is provisional but clearly reusable
4. link it to the relevant sources or formal pages
5. keep it out of the formal wiki until it is durable enough to promote or merge

Low-interruption response style:

- keep the acknowledgment brief and inline with the ongoing discussion
- do not make the user step through a separate capture workflow
- if the user has not actually asked to keep it, suggest the candidate instead of silently creating it
- do not create candidates for casual brainstorming, temporary task state, or raw emotional reactions

Good response pattern:

`That looks worth keeping as a candidate note because it may change the project thesis, but it still needs validation. I will keep it linked to the current project and continue from there.`

### Candidate Resolution

Candidate resolution should also work through ordinary chat.
The user does not need to speak in protocol vocabulary, but the agent should map normal language onto the existing outcomes:

- `promote`: the note becomes a new or materially revised formal page
- `merge`: the durable part belongs inside an existing formal page
- `drop`: the note should no longer occupy long-term work-memory space

Ordinary user phrases that may imply resolution:

- `That note is now solid enough to become an insight.`
- `Put the durable part into the current project page.`
- `This turned out to be noise. Drop it.`
- `We used that tentative note enough times. Clean it up properly now.`

Expected behavior:

1. resolve the candidate through `promote`, `merge`, or `drop`
2. update the candidate note status and `meta/candidates/index.md`
3. update the affected formal pages when the result is `promote` or `merge`
4. refresh `wiki/recent.md`, `wiki/active.md`, `wiki/index.md`, `wiki/log.md`, and `meta/lint-status.json` as required by the existing protocol

Low-interruption response style:

- if the user's intention is explicit, resolve it directly
- if the agent's answer materially relies on a candidate but the user did not ask to resolve it, make the tentative status clear and ask one short follow-up such as whether to promote, merge, or leave it open
- do not present a candidate-backed judgment as settled formal knowledge without saying that it is still provisional

Good response pattern:

`We are now relying on that note as a stable conclusion rather than a tentative lead. I can promote it into a formal insight and update the related project page.`

### Maintenance

Maintenance is part of ordinary agent use, not a separate admin surface.
Because maintenance writes back to the filesystem, the agent should suggest it proactively but run it only when the user asks for it or another request clearly includes maintenance intent.
The user may trigger it with phrases such as:

- `Run a lint pass before we use this for planning.`
- `Clean up stale candidate notes.`
- `Is the knowledge base still consistent?`
- `Before we continue, do a maintenance pass on this topic.`

The agent should also suggest maintenance when the normal protocol says it matters, especially when:

- `meta/lint-status.json` shows `last_lint` is older than 24 hours
- several ingests or formal page updates happened recently
- multiple candidates were created or resolved
- the agent is about to rely on older pages for a new topic-level synthesis or recommendation

Expected behavior:

1. read `meta/lint-status.json`
2. review entry pages and directly affected formal pages
3. review `meta/candidates/index.md` and the relevant open candidates
4. resolve stale or no-longer-useful candidates when appropriate
5. record the maintenance pass in the required locations

Low-interruption response style:

- a stale-lint reminder should be brief, not dominating
- do not interrupt an urgent debugging or execution task just to force a lint pass
- do not start a writeback maintenance pass only because lint is overdue; suggest it unless the user already asked for maintenance
- if the maintenance scope implies broad structural cleanup, ask before making large changes

Good response pattern:

`Lint is overdue. We do not need to stop this task right now, but before the next topic-level synthesis I should run a maintenance pass and review open candidates.`

## How The Agent Should Stay Low-Interruption

Atomic Knowledge should feel like memory discipline inside the agent, not like a second product the user has to operate.

Practical rules:

- silently consult the knowledge base when the trigger is obvious
- treat continuation, context recovery, and retrieval as proactive reads, not as write authorization
- suggest capture, promotion, merge, stale-candidate cleanup, or lint when useful, but do not persist ordinary chat without consent
- ask only short questions when the intended topic, scope, or writeback target is unclear
- do not narrate every file read or maintenance detail unless the user asked for that level of visibility
- use ordinary language first, and only surface protocol terms like `candidate` or `promote` when they help the user understand what is happening
- keep reminders brief and deferrable during unrelated execution work
- preserve the distinction between formal wiki knowledge and provisional candidate material in the answer itself

This means the agent should usually sound like a collaborator, not like a workflow engine.

## When The Agent Should Proactively Consult The Knowledge Base

The agent should proactively consult the knowledge base when prior work memory is likely to improve the answer.

Typical triggers:

- the user is continuing an earlier topic, project, or open question
- the user asks for comparison, recommendation, judgment, tradeoff analysis, roadmap, or synthesis
- the user shares new material that overlaps an existing topic or current project
- the task belongs to an ongoing research thread rather than a one-off execution request
- the agent is about to give a topic-level conclusion or plan

In these cases, the correct low-interruption behavior is usually to look up the relevant context first and then answer.
The lookup itself should not become a separate negotiation step unless the topic reference is unclear.

## When The Agent Should Not Force The Knowledge Base Into The Loop

The agent should not strongly interrupt or reroute the conversation into knowledge-base consultation when the task is immediate, local, or clearly unrelated to prior research.

Common non-triggers:

- `How do I parse JSON in Python?`
- `Fix this failing test in the current repo.`
- `Run this command and show me the output.`
- `What is the exchange rate today?`

In these cases, the agent should just do the task.
It should not block on `active.md`, ask whether to query the wiki, or start offering maintenance work unless the user explicitly wants that.

## Mental Model For The User

From the user's perspective, Atomic Knowledge should feel like this:

- `If I give the agent research material, it can ingest it.`
- `If I continue a topic, it can recover the prior thread.`
- `If we produce a valuable but still tentative judgment, it can keep that as a candidate instead of losing it.`
- `If that judgment later becomes stable, it can promote or merge it.`
- `If the knowledge base gets messy or stale, the same agent can maintain it during normal work.`

That is the intended meaning of agent-native usage.
Atomic Knowledge extends the user's existing agent with a shared work-memory protocol.
It does not ask the user to leave the conversation and operate a different system.
