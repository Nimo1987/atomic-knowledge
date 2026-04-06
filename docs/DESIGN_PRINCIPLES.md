# Design Principles

Atomic Knowledge is a filesystem-first `work memory` protocol for long-term research collaboration.

The goal is to keep what the user and agent have already figured out together in a form that stays reusable across sessions, projects, and agent platforms.

## Work Memory, Not Persona Memory

Atomic Knowledge stores durable research context:

- source-grounded findings
- reusable comparisons and syntheses
- project theses and decision rationales
- recurring open questions and verified dead ends

It does not aim to store every conversation detail, user persona preference, or routine task trace.

## Knowledge Is More Than Ingest

`raw/sources/` matters, but source ingest is only part of the system.

Important knowledge also appears when the user and agent compare options, refine a thesis, reject a bad direction, or turn scattered inputs into a reusable conclusion. The system should preserve those outcomes too.

That is why the model has both:

- formal wiki pages for stable knowledge
- `meta/candidates/` for high-value but still provisional work memory

The candidate layer exists to catch useful conversation sparks without forcing them into a formal page too early.

Candidate notes are a staging buffer, not a permanent archive. They should eventually be promoted, merged, or dropped.

## Keep The Formal Wiki Clean

The formal wiki should stay readable and durable.

That is why the structure separates:

- `wiki/active.md` for what is currently in motion
- `wiki/recent.md` for what changed lately
- `wiki/index.md` for the broader catalog
- `meta/candidates/` for material that still needs review

This gives the agent a clear entry path for retrieval and gives the user a clean distinction between settled knowledge and provisional notes.

## Markdown First

Markdown is the primary knowledge format because it matches the goals of the project:

- it is portable across agent platforms
- it is easy for users to inspect and edit directly
- it works well with ordinary filesystem tools and version control
- it keeps content and light structure together in one place

The schemas in `schemas/` already define the small amount of structure the pages need. Simple frontmatter plus markdown is enough for the current stage.

## Why Not A Database As The Primary Storage Layer

The current goal is a portable protocol, not a tightly coupled application stack.

Making a database the primary substrate would add operational weight and reduce the portability that makes this repository useful across many agent systems. It would also make the mainline harder to inspect, copy, and evolve as a simple filesystem kit.

This does not rule out search indexes, caches, or database-backed tools later. It only means the database should be a derived or optional layer, not the source of truth.

## Why Not Sidecar JSON For Every Page

Per-page sidecar JSON files split one logical document into two files that must stay synchronized.

That creates friction for a markdown-first workflow:

- users naturally edit the markdown page directly
- agents may update the content without updating the sidecar in lockstep
- duplicated metadata can drift from the page it describes
- review gets harder because meaning is split across files

For the current stage, page-local structure belongs in markdown frontmatter, and only a small amount of global machine metadata should live outside pages, such as `meta/lint-status.json`.

## Practical Direction

The mainline model stays intentionally simple:

- `raw/` preserves source captures
- `wiki/` holds compiled knowledge
- `meta/candidates/` buffers provisional work memory
- lightweight metadata supports maintenance without replacing markdown as the primary layer

This keeps the protocol inspectable, editable, and usable in real research workflows before adding heavier infrastructure.
