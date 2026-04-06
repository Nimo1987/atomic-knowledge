# Repository Agent Instructions

This `AGENTS.md` is for agents working on the Atomic Knowledge repository itself.

It is not the end-user install artifact.

## Source of Truth

- `universal/` is the mainline product surface
- prefer evolving the platform-neutral protocol before adding any platform-specific packaging

## Editing Priorities

1. Keep the main concept platform-neutral.
2. Treat `universal/AGENT.md` as the canonical portable protocol.
3. Avoid reintroducing platform-specific assumptions into the mainline docs.
4. Prefer a self-contained filesystem-based protocol over platform-specific glue.

## Documentation Rules

- Root `README.md` should describe the universal mainline first.
- Universal docs should explain cross-agent behavior, not only one platform.
- Installation instructions should assume the repository itself is the GitHub-distributed product.

## Knowledge Model

The mainline model includes:

- `raw/sources`
- `wiki/concepts`
- `wiki/entities`
- `wiki/projects`
- `wiki/insights`

Do not collapse `projects` and `insights` back into generic notes unless there is a strong reason.

## Compatibility

- prefer generic filesystem workflows that can be adopted by many agent systems
- avoid coupling the project to one agent vendor or one instruction mechanism
