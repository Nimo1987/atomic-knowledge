#!/usr/bin/env bash

set -euo pipefail

SCRIPT_NAME="$(basename "$0")"
KB_INPUT="${1:-.}"

ok_count=0
warn_count=0
fail_count=0
info_count=0

usage() {
    printf 'Usage: %s [knowledge-base-root]\n' "$SCRIPT_NAME"
    printf 'Run a read-only health check against an Atomic Knowledge base.\n'
}

trim() {
    local value="$1"

    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"

    printf '%s\n' "$value"
}

resolve_path() {
    local target="$1"
    local parent
    local base

    if [ -d "$target" ]; then
        (
            cd "$target"
            pwd -P
        )
        return
    fi

    parent="$(dirname "$target")"
    base="$(basename "$target")"

    if [ -d "$parent" ]; then
        printf '%s/%s\n' "$(cd "$parent" && pwd -P)" "$base"
        return
    fi

    printf '%s\n' "$target"
}

report() {
    local level="$1"
    local message="$2"

    printf '[%s] %s\n' "$level" "$message"

    case "$level" in
        OK)
            ok_count=$((ok_count + 1))
            ;;
        WARN)
            warn_count=$((warn_count + 1))
            ;;
        FAIL)
            fail_count=$((fail_count + 1))
            ;;
        INFO)
            info_count=$((info_count + 1))
            ;;
    esac
}

report_ok() {
    report "OK" "$1"
}

report_warn() {
    report "WARN" "$1"
}

report_fail() {
    report "FAIL" "$1"
}

report_info() {
    report "INFO" "$1"
}

print_section() {
    printf '\n== %s ==\n' "$1"
}

check_dir() {
    local relative_path="$1"

    if [ -d "$KB_DIR/$relative_path" ]; then
        report_ok "directory present: $relative_path"
    else
        report_fail "missing directory: $relative_path"
    fi
}

check_file() {
    local relative_path="$1"

    if [ -f "$KB_DIR/$relative_path" ]; then
        report_ok "file present: $relative_path"
    else
        report_fail "missing file: $relative_path"
    fi
}

json_raw_value() {
    local key="$1"
    local file_path="$2"

    awk -v key="$key" '
        $0 ~ "\"" key "\"[[:space:]]*:" {
            line = $0
            sub(/^[^:]*:[[:space:]]*/, "", line)
            sub(/[[:space:]]*,[[:space:]]*$/, "", line)
            print line
            exit
        }
    ' "$file_path"
}

json_string_or_null() {
    local raw_value

    raw_value="$(trim "$(json_raw_value "$1" "$2")")"

    if [ -z "$raw_value" ]; then
        return 1
    fi

    if [ "$raw_value" = "null" ]; then
        printf 'null\n'
        return 0
    fi

    case "$raw_value" in
        \"*\")
            raw_value="${raw_value#\"}"
            raw_value="${raw_value%\"}"
            printf '%s\n' "$raw_value"
            ;;
        *)
            return 1
            ;;
    esac
}

json_number() {
    local raw_value

    raw_value="$(trim "$(json_raw_value "$1" "$2")")"

    case "$raw_value" in
        ''|*[!0-9]*)
            return 1
            ;;
        *)
            printf '%s\n' "$raw_value"
            ;;
    esac
}

frontmatter_value() {
    local key="$1"
    local file_path="$2"

    awk -v key="$key" '
        NR == 1 {
            if ($0 !~ /^---[[:space:]]*$/) {
                exit
            }
            in_frontmatter = 1
            next
        }
        in_frontmatter && /^---[[:space:]]*$/ {
            exit
        }
        in_frontmatter && $0 ~ "^" key ":[[:space:]]*" {
            line = $0
            sub("^" key ":[[:space:]]*", "", line)
            print line
            exit
        }
    ' "$file_path"
}

epoch_from_timestamp() {
    local value="$1"
    local bsd_value

    epoch_from_timestamp_bsd() {
        local format="$1"
        local input="$2"

        TZ=UTC date -j -f "$format" "$input" "+%s" 2>/dev/null
    }

    epoch_from_timestamp_gnu() {
        local input="$1"

        date -u -d "$input" "+%s" 2>/dev/null
    }

    case "$value" in
        ????-??-??T??:??:??Z)
            epoch_from_timestamp_bsd "%Y-%m-%dT%H:%M:%SZ" "$value" || epoch_from_timestamp_gnu "$value"
            ;;
        ????-??-??)
            epoch_from_timestamp_bsd "%Y-%m-%d" "$value" || epoch_from_timestamp_gnu "$value"
            ;;
        ????-??-??T??:??:??[+-]??:??)
            bsd_value="$(printf '%s' "$value" | sed -E 's/([+-][0-9]{2}):([0-9]{2})$/\1\2/')"
            epoch_from_timestamp_bsd "%Y-%m-%dT%H:%M:%S%z" "$bsd_value" || epoch_from_timestamp_gnu "$value"
            ;;
        *)
            return 1
            ;;
    esac
}

relative_path() {
    local path="$1"

    printf '%s\n' "${path#$KB_DIR/}"
}

count_markdown_files() {
    find "$@" -type f -name '*.md' 2>/dev/null | wc -l | tr -d '[:space:]'
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    usage
    exit 0
fi

if [ "$#" -gt 1 ]; then
    usage >&2
    exit 1
fi

KB_DIR="$(resolve_path "$KB_INPUT")"
NOW_EPOCH="$(date -u +%s)"

printf 'Atomic Knowledge Health Check\n'
printf 'KB root: %s\n' "$KB_DIR"

if [ ! -d "$KB_DIR" ]; then
    report_fail "knowledge base root does not exist or is not a directory"
    printf '\nSummary: %s OK, %s INFO, %s WARN, %s FAIL\n' "$ok_count" "$info_count" "$warn_count" "$fail_count"
    exit 1
fi

print_section "Required Structure"

required_directories=(
    "raw"
    "raw/sources"
    "wiki"
    "wiki/concepts"
    "wiki/entities"
    "wiki/projects"
    "wiki/procedures"
    "wiki/insights"
    "meta"
    "meta/candidates"
    "meta/lint-reports"
)

required_files=(
    "wiki/active.md"
    "wiki/recent.md"
    "wiki/index.md"
    "wiki/log.md"
    "meta/candidates/index.md"
    "meta/lint-reports/index.md"
    "meta/lint-status.json"
)

for directory in "${required_directories[@]}"; do
    check_dir "$directory"
done

for file_path in "${required_files[@]}"; do
    check_file "$file_path"
done

print_section "Local Schemas"

if [ -d "$KB_DIR/meta/schemas" ]; then
    report_ok "directory present: meta/schemas"

    schema_files=(
        "meta/schemas/concept.md"
        "meta/schemas/entity.md"
        "meta/schemas/project.md"
        "meta/schemas/procedure.md"
        "meta/schemas/insight.md"
        "meta/schemas/candidate.md"
        "meta/schemas/lint-report.md"
    )

    for schema_file in "${schema_files[@]}"; do
        if [ -f "$KB_DIR/$schema_file" ]; then
            report_ok "file present: $schema_file"
        else
            report_warn "missing local schema mirror: $schema_file"
        fi
    done
else
    report_warn "missing local schema mirror: meta/schemas (the KB may still rely on canonical schemas stored elsewhere)"
fi

print_section "Lint Status"

LINT_STATUS_FILE="$KB_DIR/meta/lint-status.json"

if [ -f "$LINT_STATUS_FILE" ]; then
    schema_version="$(json_string_or_null "schema_version" "$LINT_STATUS_FILE" || true)"
    last_lint="$(json_string_or_null "last_lint" "$LINT_STATUS_FILE" || true)"
    lint_count="$(json_number "lint_count" "$LINT_STATUS_FILE" || true)"
    total_pages="$(json_number "total_pages" "$LINT_STATUS_FILE" || true)"
    total_sources="$(json_number "total_sources" "$LINT_STATUS_FILE" || true)"

    missing_lint_fields=0

    if [ -n "$schema_version" ] && [ "$schema_version" != "null" ]; then
        report_ok "lint status schema_version: $schema_version"
    else
        report_fail "lint status missing string field: schema_version"
        missing_lint_fields=1
    fi

    if [ -n "$last_lint" ]; then
        :
    else
        report_fail "lint status missing field: last_lint"
        missing_lint_fields=1
    fi

    if [ -n "$lint_count" ]; then
        report_ok "lint status lint_count: $lint_count"
    else
        report_fail "lint status missing numeric field: lint_count"
        missing_lint_fields=1
    fi

    if [ -n "$total_pages" ]; then
        report_ok "lint status total_pages: $total_pages"
    else
        report_fail "lint status missing numeric field: total_pages"
        missing_lint_fields=1
    fi

    if [ -n "$total_sources" ]; then
        report_ok "lint status total_sources: $total_sources"
    else
        report_fail "lint status missing numeric field: total_sources"
        missing_lint_fields=1
    fi

    if [ "$missing_lint_fields" -eq 0 ]; then
        if [ "$last_lint" = "null" ]; then
            report_warn "lint has not run yet: last_lint is null"
        else
            if lint_epoch="$(epoch_from_timestamp "$last_lint")"; then
                lint_age_seconds=$((NOW_EPOCH - lint_epoch))

                if [ "$lint_age_seconds" -lt 0 ]; then
                    report_warn "last_lint is in the future: $last_lint"
                else
                    lint_age_hours=$((lint_age_seconds / 3600))

                    if [ "$lint_age_seconds" -gt 86400 ]; then
                        report_warn "lint is older than 24 hours: $last_lint (${lint_age_hours}h ago)"
                    else
                        report_ok "lint freshness is within 24 hours: $last_lint (${lint_age_hours}h ago)"
                    fi
                fi
            else
                report_warn "could not parse last_lint timestamp: $last_lint"
            fi
        fi

        if [ -d "$KB_DIR/wiki" ] && [ -d "$KB_DIR/meta/candidates" ] && [ -d "$KB_DIR/meta/lint-reports" ]; then
            actual_pages="$(count_markdown_files "$KB_DIR/wiki" "$KB_DIR/meta/candidates" "$KB_DIR/meta/lint-reports")"
            report_info "actual tracked page count: $actual_pages"

            if [ "$last_lint" = "null" ]; then
                report_info "stored page count is a bootstrap value until the first lint pass"
            elif [ "$actual_pages" = "$total_pages" ]; then
                report_ok "stored page count matches actual content"
            else
                report_warn "stored page count differs from actual content: status=$total_pages, actual=$actual_pages"
            fi
        fi

        if [ -d "$KB_DIR/raw/sources" ]; then
            actual_sources="$(count_markdown_files "$KB_DIR/raw/sources")"
            report_info "actual raw source count: $actual_sources"

            if [ "$last_lint" = "null" ]; then
                report_info "stored source count is a bootstrap value until the first lint pass"
            elif [ "$actual_sources" = "$total_sources" ]; then
                report_ok "stored source count matches actual content"
            else
                report_warn "stored source count differs from actual content: status=$total_sources, actual=$actual_sources"
            fi
        fi
    fi
fi

print_section "Candidate Freshness"

candidate_total=0
candidate_open=0
candidate_resolved=0
candidate_review_due=0
candidate_stale=0
candidate_unknown=0
review_due_details=()
stale_details=()

if [ -d "$KB_DIR/meta/candidates" ]; then
    while IFS= read -r candidate_file; do
        candidate_total=$((candidate_total + 1))

        candidate_status="$(trim "$(frontmatter_value "status" "$candidate_file" || true)")"

        case "$candidate_status" in
            open)
                candidate_open=$((candidate_open + 1))
                ;;
            promoted|merged|dropped)
                candidate_resolved=$((candidate_resolved + 1))
                continue
                ;;
            '')
                report_warn "candidate note missing status frontmatter: $(relative_path "$candidate_file")"
                candidate_unknown=$((candidate_unknown + 1))
                continue
                ;;
            *)
                report_warn "candidate note has unexpected status '$candidate_status': $(relative_path "$candidate_file")"
                candidate_unknown=$((candidate_unknown + 1))
                continue
                ;;
        esac

        candidate_date="$(trim "$(frontmatter_value "updated" "$candidate_file" || true)")"

        if [ -z "$candidate_date" ]; then
            candidate_date="$(trim "$(frontmatter_value "created" "$candidate_file" || true)")"
        fi

        if [ -z "$candidate_date" ]; then
            report_warn "open candidate note missing created/updated date: $(relative_path "$candidate_file")"
            candidate_unknown=$((candidate_unknown + 1))
            continue
        fi

        if candidate_epoch="$(epoch_from_timestamp "$candidate_date")"; then
            candidate_age_days=$(((NOW_EPOCH - candidate_epoch) / 86400))

            if [ $((NOW_EPOCH - candidate_epoch)) -lt 0 ]; then
                report_warn "open candidate note has a future date: $(relative_path "$candidate_file") ($candidate_date)"
                candidate_unknown=$((candidate_unknown + 1))
                continue
            fi

            if [ "$candidate_age_days" -ge 14 ]; then
                candidate_stale=$((candidate_stale + 1))
                stale_details[${#stale_details[@]}]="$(relative_path "$candidate_file") | ${candidate_age_days}d since $candidate_date"
            elif [ "$candidate_age_days" -ge 7 ]; then
                candidate_review_due=$((candidate_review_due + 1))
                review_due_details[${#review_due_details[@]}]="$(relative_path "$candidate_file") | ${candidate_age_days}d since $candidate_date"
            fi
        else
            report_warn "open candidate note has an unparseable date: $(relative_path "$candidate_file") ($candidate_date)"
            candidate_unknown=$((candidate_unknown + 1))
        fi
    done < <(find "$KB_DIR/meta/candidates" -type f -name '*.md' ! -name 'index.md' 2>/dev/null | sort)

    report_info "candidate notes: total=$candidate_total, open=$candidate_open, resolved=$candidate_resolved"

    if [ "$candidate_stale" -gt 0 ]; then
        report_warn "stale open candidates: $candidate_stale"
        for detail in "${stale_details[@]}"; do
            report_info "stale candidate: $detail"
        done
    else
        report_ok "stale open candidates: none"
    fi

    if [ "$candidate_review_due" -gt 0 ]; then
        report_info "open candidates due for review soon: $candidate_review_due"
        for detail in "${review_due_details[@]}"; do
            report_info "review due candidate: $detail"
        done
    else
        report_ok "open candidates due for review soon: none"
    fi

    if [ "$candidate_unknown" -gt 0 ]; then
        report_warn "candidate notes with incomplete or unparseable freshness metadata: $candidate_unknown"
    else
        report_ok "candidate note freshness metadata is parseable"
    fi
fi

print_section "Summary"

printf 'Summary: %s OK, %s INFO, %s WARN, %s FAIL\n' "$ok_count" "$info_count" "$warn_count" "$fail_count"

if [ "$fail_count" -gt 0 ]; then
    printf 'Result: FAIL\n'
    exit 1
fi

if [ "$warn_count" -gt 0 ]; then
    printf 'Result: PASS WITH WARNINGS\n'
    exit 0
fi

printf 'Result: PASS\n'
