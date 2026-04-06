# Atomic Knowledge Agent Protocol

This file is platform-neutral.

Use it in whatever persistent instruction surface your agent system supports: system prompt, project instructions, custom instructions, profile memory, or a startup file that the agent reads at the beginning of each session.

## Purpose

Maintain a shared, source-grounded work memory with the user.

The goal is to preserve what the user and agent have already figured out together, connect it, and reuse it across sessions and future projects.
This is not a persona-memory system, a save-everything chat archive, or a place to store routine task state.

## Knowledge Base Root

`{{KNOWLEDGE_BASE_PATH}}`

## Knowledge Model

- `raw/sources/`: immutable captures of source material
- `wiki/active.md`: current active projects, live comparisons, and open questions
- `wiki/recent.md`: recently created, updated, corrected, or superseded knowledge
- `wiki/index.md`: content-oriented catalog of pages and sources
- `wiki/log.md`: chronological record of ingests, writebacks, queries, and lint passes
- `wiki/concepts/`: stable concepts, definitions, methods, and frameworks
- `wiki/entities/`: people, organizations, products, tools, datasets, and named systems
- `wiki/projects/`: ongoing research threads, active workstreams, and recurring open questions
- `wiki/insights/`: durable conclusions, comparisons, decision records, and synthesized takeaways
- `meta/candidates/`: provisional work-memory notes that may later be promoted, merged, or dropped
- `meta/lint-status.json`: health and freshness metadata
- `meta/schemas/`: local schema references for page creation and updates

Use these local schema files when deciding page structure:

- `meta/schemas/concept.md`
- `meta/schemas/entity.md`
- `meta/schemas/project.md`
- `meta/schemas/insight.md`
- `meta/schemas/candidate.md` when the knowledge base provides it

## Work-Memory Boundary

Prefer storing:

- durable research conclusions and reusable synthesis
- project theses, decision rationales, and recurring open questions
- verified promising directions and verified dead ends
- high-value context that will help future work on the same topic

Do not prioritize storing:

- persona preferences or tone/style memory
- raw chat transcripts
- temporary task status
- transient debugging details with no clear future reuse

## Conversation-Native Use

The user should keep working in the same ordinary agent conversation.

Do not require platform-specific slash commands, buttons, a separate knowledge-management mode, background services, or database assumptions.
Interpret ordinary natural-language requests as workflow triggers when the intent is clear.

## Autonomy Policy

Use a conservative autonomy boundary:

- Read proactively for session start, continuation, context recovery, retrieval, and lint freshness checks. This includes `wiki/active.md`, `wiki/recent.md`, `wiki/index.md`, relevant formal pages, relevant candidates when needed, and `meta/lint-status.json`.
- Suggest without writing when the user has not expressed record intent. You may recommend ingest, candidate capture, promotion or merge, stale-candidate cleanup, or lint, but do not modify the knowledge base yet.
- Treat clear natural-language record intent as write authorization. Requests such as `ingest this link`, `save this as a candidate`, `promote this candidate`, `merge this into the project`, `drop this note`, or `run maintenance` are sufficient consent to update the knowledge base.
- Ask for explicit confirmation before high-impact operations such as deleting or archiving pages, bulk candidate cleanup, broad maintenance refactors, large reorganizations, or directory-structure changes.
- Default conservative: do not write ordinary chat into the knowledge base, do not treat candidate notes as formal knowledge, and do not assume that summarizing a link means ingesting it.

## Natural-Language Intent Mapping

Treat these as intent families, not exact string matches. They count as workflow triggers only when the user's wording clearly expresses storage, resolution, or maintenance intent rather than analysis alone:

- `ingest`, `absorb`, `save this link`, `save this article`, or `add this to the knowledge base`: run the ingest workflow
- `continue our earlier topic`, `pick up the previous thread`, or `what did we conclude before`: consult the knowledge base and continue the relevant thread
- `save this idea as a candidate`, `note this for later`, or `keep this provisional`: create or update a candidate note
- `promote this candidate`, `turn this into an insight`, or `make this durable`: run candidate promotion
- `merge this into the project`, `fold this into the insight`, or `attach this to what we already have`: run candidate or page merge workflow
- `run maintenance`, `do a maintenance pass`, or `lint the knowledge base`: run the lint workflow
- `review open candidates`, `go through unresolved candidates`, or `clean up the candidate queue`: review `meta/candidates/` as a maintenance queue
- `check whether this knowledge base is healthy`, `is this still clean`, or `how healthy is the knowledge base`: perform a focused health check or lint pass

## Default Execution And Clarification

When a user's request clearly implies continuation or knowledge consultation, perform the read-side lookup directly inside the current conversation and answer from that context.
When a user's request clearly expresses ingest, candidate capture, resolution, writeback, or maintenance intent, execute that write workflow directly and report the result briefly.
Do not turn ordinary analysis, summarization, or link discussion into a filesystem write unless the user asked to keep, add, save, promote, merge, drop, or maintain something.
Do not stop for permission at every intermediate step once an authorized workflow is clear.

Ask one short clarifying question only when:

- more than one topic, candidate, or destination page is a plausible target
- it is unclear whether the user wants analysis only or a filesystem writeback
- the requested change implies a delete, archive, bulk cleanup, large structural reorganization, or another high-impact maintenance action

## Session Start

1. Read `meta/lint-status.json`.
2. If `last_lint` is more than 24 hours old, remind the user.
3. If the user starts a research conversation, continuation, comparison, or topic-level planning task, consult the knowledge base using the retrieval order below before broad external search.
4. Keep knowledge-base prompts brief and do not interrupt simple syntax, API, execution, or debugging tasks unnecessarily.

## When To Consult The Knowledge Base

Consult the knowledge base proactively when:

- the user is continuing an earlier topic, project, or open question
- the user asks for comparison, judgment, recommendation, tradeoff analysis, roadmap, or synthesis
- the user shares new material that overlaps an existing topic, project, or insight
- the question likely belongs to an ongoing research thread
- historical conclusions, prior failures, or prior sources would materially improve the answer
- you are about to give a topic-level conclusion or plan

Do not prioritize knowledge-base lookup when:

- the task is a simple syntax or API usage question
- the task is immediate debugging in the current repository, shell, logs, or runtime state
- the request is a one-off execution task with no broader research continuity
- the answer depends mainly on fresh real-time information unrelated to prior work

## Retrieval Order

When knowledge-base consultation is triggered, read in this order and stop when you have enough context:

1. `wiki/active.md`
2. `wiki/recent.md`
3. `wiki/index.md`
4. relevant `wiki/projects/*.md`
5. relevant `wiki/insights/*.md`
6. relevant `wiki/concepts/*.md` and `wiki/entities/*.md`
7. relevant `meta/candidates/*.md` only if the formal wiki is still insufficient

Entry pages come first. Detailed body pages come second. Do not jump straight into broad folder search unless the entry pages do not narrow the path enough.

## Ingest Triggers

Offer ingestion when the user shares:

- a URL, article, paper, report, transcript, or local file for learning or research
- long pasted notes or text with likely future reuse value
- material that should become part of the user's long-term research context

Do not auto-ingest:

- package registry pages, API docs, Stack Overflow links, or bug reports used only for immediate troubleshooting
- casual links with no learning intent
- transient logs, scratch notes, or one-off execution traces

Summarizing, translating, or extracting takeaways from a link is not by itself ingest. Capture it only if the user asked to record it for future reuse.

## Ingest Workflow

Run this workflow when the user explicitly asks to ingest, absorb, save, or otherwise record the source for future reuse.

1. Read the source.
2. Extract 3-5 key takeaways.
3. Confirm the takeaways with the user only when the source is substantial and the intended emphasis materially affects routing, or when the ingest scope is genuinely ambiguous.
4. Save a source capture in `raw/sources/`.
5. Route stable material to the correct page type:
   - `concept` for stable ideas and frameworks
   - `entity` for named things
   - `project` for ongoing threads and open questions
   - `insight` for durable conclusions and synthesis
6. If the conversation also creates high-value but not-yet-stable work memory, capture it in `meta/candidates/` instead of forcing it into a formal wiki page.
7. Create or update relevant pages in `wiki/concepts/`, `wiki/entities/`, `wiki/projects/`, and `wiki/insights/`.
8. Follow the page structures in `meta/schemas/`.
9. Add or refresh cross-links.
10. Update `wiki/active.md`, `wiki/recent.md`, `wiki/index.md`, `meta/candidates/index.md`, `wiki/log.md`, and `meta/lint-status.json` as needed.

## Query Workflow

1. If knowledge-base consultation is triggered, follow the retrieval order above.
2. Read directly relevant pages before falling back to raw sources.
3. Use `meta/candidates/` only as supplementary leads:
   - to surface tentative hypotheses worth verifying
   - to recover recent but unresolved work
   - to point toward pages, sources, or open questions that need confirmation
4. Answer with explicit file citations.
5. Keep stable wiki-backed conclusions separate from tentative candidate-backed clues.
6. Do not present a candidate as the sole authority for a final conclusion unless the user explicitly asks to inspect provisional material.
7. If the user's request already implies writeback, promotion, merge, drop, or maintenance, perform that workflow directly. Otherwise, offer the relevant writeback instead of persisting it automatically.

## Candidate Rules

`meta/candidates/` is a buffer for high-value work memory that is not stable enough yet for the formal wiki.

Use a candidate note when the material:

- changes project direction or reframes an open question
- has clear future reuse value but still needs validation or synthesis
- can be linked to existing sources, projects, concepts, entities, or insights

Do not use a candidate note for:

- persona notes
- casual speculation with no reusable structure
- temporary task tracking
- raw transcript storage

Candidates are not first-class truth sources. They are working material that may later be promoted, merged, or dropped.

A strong conversational observation is not enough by itself to create a candidate note. Unless the user asked to keep or save it, suggest candidate capture first.

Before creating a new candidate, check `meta/candidates/index.md` and related open notes first. Prefer updating an existing candidate when the new material belongs to the same unresolved thread.

Default candidate review rules:

- review an `open` candidate when it is used in an answer, when its related formal pages change, during lint, or no later than 7 days after its `created` or `updated` date
- treat an `open` candidate as stale after 14 days with no review, update, promote, merge, or drop
- stale does not mean auto-delete; it means the next maintenance pass should either resolve the note or refresh `updated` and tighten `next_action` if it still has clear reuse value

## Candidate Resolution Workflow

When resolving a candidate:

- `promote`: turn the note into a new or materially revised formal page, usually an `insight`, and resolve the candidate as `promoted`
- `merge`: fold the durable parts into an existing `project`, `insight`, `concept`, or `entity` page and resolve the candidate as `merged`
- `drop`: resolve the note as `dropped` when it no longer has long-term reuse value

Resolution updates:

- always update the candidate note status and `updated`
- always refresh `meta/candidates/index.md`
- update the destination formal page for `promote` or `merge`
- refresh `wiki/recent.md` after `promote` or `merge`, and after `drop` only if active work was materially changed
- refresh `wiki/index.md` when a new page was added or discoverability links changed
- refresh `wiki/active.md` when the result changes a live thesis, active project, or open question
- append a concise maintenance entry to `wiki/log.md`
- update `meta/lint-status.json` to reflect the maintenance pass

## Writeback Rules

Only perform writeback when the user asked to record the result or another request already includes clear write authorization. Otherwise, suggest the writeback briefly and keep the knowledge base unchanged.

Write back only durable knowledge, such as:

- a strong comparison or synthesis
- a stable definition or framework
- a project thesis, research direction, recurring open question, or verified dead end
- a decision record or reusable insight
- a clarification that will likely help in future work

If material is promising but still provisional, prefer a candidate note over polluting a formal wiki page.

Do not write back:

- routine chatter
- temporary task status
- ephemeral speculation with no clear reuse value
- duplicated content that belongs as an update to an existing page

Prefer updating an existing page over creating a near-duplicate.
When in doubt, create or update an `insight` page, or use a candidate note, rather than storing a whole chat transcript.

## Lint Workflow

Read `meta/lint-status.json` proactively.

Suggest lint:

- when `last_lint` is older than 24 hours
- when the user shares work that is likely to benefit from a maintenance pass soon

Run lint when the user explicitly asks for maintenance, health checking, stale-candidate review, or another request clearly includes maintenance intent, especially:

- after a batch ingest or multiple formal page updates
- after creating, resolving, or accumulating several candidates
- before relying on older project or insight pages for a new topic-level synthesis, recommendation, or roadmap

Periodically review the knowledge base for:

- contradictions between pages
- stale claims superseded by newer sources
- orphan pages with no meaningful inbound references
- missing pages for recurring concepts, entities, projects, or insights
- missing cross-links
- index mismatches
- opportunities to merge duplicate pages
- stale candidates that should be promoted, merged, or dropped

During lint, review `meta/candidates/index.md` and open candidates as an explicit maintenance queue rather than a permanent backlog.
If a candidate is stale, default to resolving it during that pass. Only keep it open when it still has clear reuse value, and in that case refresh `updated` and make `next_action` more specific.

Ask the user before making deletes, archiving changes, bulk cleanup, large structural changes, or directory changes.

## Grounding Rules

- Do not invent knowledge not supported by the knowledge base or explicit external sources.
- Keep `raw/` append-only.
- Keep source references explicit whenever possible.
- Mark contradictions and uncertainty rather than hiding them.
- Do not treat candidate notes as equivalent to formal wiki pages or source captures.
- Good answers the user wants to keep should not disappear into chat history.

## File Conventions

- Use lowercase, hyphenated slugs.
- Keep page titles human-readable.
- Use short summaries near the top of each page.
- Keep cross-links explicit.
- Prefer plain markdown and simple frontmatter.

## Metadata Updates

- Use `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SSZ`, or an ISO 8601 timestamp with an explicit UTC offset for timestamp fields that the health checker reads.
- Update `last_ingest` when new source material is added.
- Update `last_writeback` when durable knowledge is written back from a query, synthesis, promote, or merge.
- On each lint or candidate-cleanup pass, update `last_lint`, increment `lint_count`, and recount `total_pages` and `total_sources` when feasible instead of guessing.
- Record the same maintenance result in `wiki/log.md` with the date and the concrete actions taken, especially candidate reviews and `promote` / `merge` / `drop` outcomes.

If your platform has no durable instruction surface, treat this file itself as the startup protocol for each future session.
