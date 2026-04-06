#!/usr/bin/env bash

set -euo pipefail

escape_sed_replacement() {
    printf '%s' "$1" | sed -e 's/[&|\\]/\\&/g'
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_DIR="$ROOT_DIR/knowledge-base-template"
AGENT_TEMPLATE="$ROOT_DIR/AGENT.md"
SCHEMAS_DIR="$ROOT_DIR/schemas"
KB_DIR="${1:-$HOME/Desktop/My-Knowledge}"

if [ -e "$KB_DIR" ] && [ -n "$(ls -A "$KB_DIR" 2>/dev/null)" ]; then
    printf "Target directory is not empty: %s\n" "$KB_DIR" >&2
    printf "Choose an empty path or remove the existing directory first.\n" >&2
    exit 1
fi

mkdir -p "$KB_DIR"
cp -R "$TEMPLATE_DIR/." "$KB_DIR/"
mkdir -p "$KB_DIR/meta/schemas" "$KB_DIR/meta/candidates" "$KB_DIR/meta/lint-reports"
cp -R "$SCHEMAS_DIR/." "$KB_DIR/meta/schemas/"

TODAY="$(date +%Y-%m-%d)"

cat > "$KB_DIR/wiki/active.md" <<EOF
# Active Work

> Read this first for the current projects, live comparisons, and open questions.

> Last updated: $TODAY

## Active Projects

(none)

## Live Comparisons

(none)

## Open Questions

(none)
EOF

cat > "$KB_DIR/wiki/recent.md" <<EOF
# Recent Updates

> Read this early for newly created, updated, corrected, or superseded knowledge.

> Last updated: $TODAY

## Recent Updates

| Date | Page | Change |
|------|------|--------|
| $TODAY | Knowledge base | Initialized |
EOF

cat > "$KB_DIR/wiki/index.md" <<EOF
# Knowledge Base Index

> Last updated: $TODAY
> Start with \`wiki/active.md\` and \`wiki/recent.md\` for current context. Use this page as the broader catalog. Check \`meta/candidates/index.md\` only for provisional follow-up leads.

## Entry Pages

- \`active.md\`: current projects, live comparisons, and open questions
- \`recent.md\`: newest additions, updates, corrections, and supersessions

## Projects

(none)

## Concepts

(none)

## Entities

(none)

## Insights

(none)

## Sources

| File | Date | Related Pages |
|------|------|---------------|
EOF

cat > "$KB_DIR/wiki/log.md" <<EOF
# Knowledge Base Log

> Reverse-chronological record of ingests, queries, writebacks, lint passes, and candidate cleanup.

<!-- Format: ## [YYYY-MM-DD] type | title -->
<!-- type: init, ingest, query, synthesize, lint, cleanup -->

## [$TODAY] init | Knowledge base initialized

- Initialized with the Atomic Knowledge root-level kit.
- Created starter pages for active work, recent updates, candidates, and lint reports.
EOF

cat > "$KB_DIR/meta/candidates/index.md" <<EOF
# Candidate Buffer

> Review queue for provisional work memory that may later be promoted, merged, or dropped.

> Check this page before creating a new candidate. Review it during lint and cleanup passes.

## Review Rules

- Reuse an existing note when the new material belongs to the same unresolved thread.
- Review open candidates when they are used, when related formal pages change, during lint, or within 7 days of \`created\` or \`updated\`.
- Treat open candidates older than 14 days as stale unless a maintenance pass refreshes \`updated\` and tightens \`next_action\`.

## Open Candidates

| Note | Related Topic | Updated | Next Action |
|------|---------------|---------|-------------|
| (none) | - | - | - |

## Recently Resolved

| Note | Outcome | Resolved At | Target |
|------|---------|-------------|--------|
| (none) | - | - | - |
EOF

cat > "$KB_DIR/meta/lint-reports/index.md" <<EOF
# Lint Reports

> Maintenance log for lint and cleanup passes. Store one markdown report per pass using \`meta/schemas/lint-report.md\`.

> Use this page to track recent reports and follow-up work.

## Reports

| Date | Report | Scope | Follow-Up |
|------|--------|-------|-----------|
| (none) | - | - | - |

## Review Notes

- Review \`meta/candidates/index.md\` as the candidate maintenance queue during each pass.
- Link follow-up actions to the specific report when a pass promotes, merges, or drops notes.
EOF

cat > "$KB_DIR/meta/lint-status.json" <<EOF
{
  "schema_version": "ak-v1",
  "last_lint": null,
  "lint_count": 0,
  "last_ingest": null,
  "last_writeback": null,
  "total_pages": 0,
  "total_sources": 0
}
EOF

ESCAPED_KB_DIR="$(escape_sed_replacement "$KB_DIR")"
sed "s|{{KNOWLEDGE_BASE_PATH}}|$ESCAPED_KB_DIR|g" "$AGENT_TEMPLATE" > "$KB_DIR/AGENT.md"

printf "Atomic Knowledge initialized at: %s\n" "$KB_DIR"
printf "Generated protocol file: %s/AGENT.md\n" "$KB_DIR"
printf "Next step: load that file into your agent platform or ask the agent to read it at session start.\n"
