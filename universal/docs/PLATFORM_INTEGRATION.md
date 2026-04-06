# Platform Integration

Atomic Knowledge is designed as a platform-neutral protocol.

The portable unit is a rendered `AGENT.md` file plus a local markdown knowledge base.

## Integration Model

Every agent platform needs the same four ingredients:

1. a local knowledge-base directory
2. a persistent or repeatable instruction surface
3. file read and write access
4. the ability to search local markdown files

The platform wrapper should preserve the same work-memory behavior everywhere:

- use the knowledge base mainly for long-lived research context, not persona memory
- consult entry pages before deep page reads when a research task continues earlier work
- do not force knowledge-base-first lookup for simple syntax, API, or immediate debugging tasks
- treat `meta/candidates/` as supplementary working material, not a first-class truth source
- preserve maintenance through ordinary file reads and writes, not a platform-specific scheduler or database queue

## Preferred Installation Pattern

1. Run `bash universal/scripts/init-kb.sh <path>`.
2. Generate `<path>/AGENT.md` with the real knowledge-base path.
3. Install that file into the agent platform's instruction surface.
4. Ensure the platform keeps the retrieval order defined in `AGENT.md`: `active -> recent -> index -> project -> insight -> concept/entity -> candidate`.

## Maintenance Behavior

The platform wrapper should preserve the maintenance protocol as well:

- read `meta/lint-status.json` at session start and remind the user when `last_lint` is older than 24 hours
- treat lint and candidate cleanup as normal filesystem maintenance during ordinary sessions, especially after batch ingest, multiple writebacks, or candidate-heavy work
- review open candidates within 7 days and treat open candidates older than 14 days without updates as stale
- when a stale candidate still matters, keep it open only after refreshing `updated` and tightening `next_action`
- on `promote`, `merge`, or `drop`, update the candidate note and `meta/candidates/index.md`, then update the affected wiki pages, `wiki/log.md`, and `meta/lint-status.json` as defined in `AGENT.md`

The platform does not need a background maintenance worker. The agent can do this during normal sessions by reading timestamps, reviewing candidate notes, and writing the results back to the filesystem.

## If the Platform Supports Persistent Instructions

Use one of these surfaces:

- system prompt
- project instructions
- custom instructions
- profile memory
- startup file

In this case, `AGENT.md` becomes the durable operating protocol.
The wrapper may adapt syntax to the platform, but it should not change retrieval triggers, retrieval order, candidate semantics, or maintenance defaults.

## If the Platform Does Not Support Persistent Instructions

Use `AGENT.md` as a startup protocol.

At the beginning of each new session, instruct the agent to read:

```text
<knowledge-base-path>/AGENT.md
```

This still gives consistent behavior because the protocol lives in the filesystem.

For research, continuation, comparison, or topic-level planning tasks, the platform should have the agent consult the entry pages first:

1. `wiki/active.md`
2. `wiki/recent.md`
3. `wiki/index.md`

Only then should it expand into detailed `project`, `insight`, `concept`, `entity`, and finally `candidate` pages as needed.

For simple syntax, API, execution, or immediate debugging tasks, the platform does not need to force that knowledge-base-first path.

## Adapter Strategy

The repository separates:

- `universal/` - core protocol and template
- optional platform wrappers - convenience layers outside the core protocol

Platform-specific wrappers may exist, but they should not redefine the conceptual model.

The markdown knowledge-base model should stay stable even when the surrounding agent platform changes.
That includes the work-memory boundary, the entry-page-first retrieval pattern, the rule that candidates remain supplementary rather than authoritative, and the filesystem-based maintenance loop recorded in `meta/lint-status.json` and `wiki/log.md`.
