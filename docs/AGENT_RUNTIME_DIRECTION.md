# Agent Runtime Direction

Atomic Knowledge remains a chat-native product.

The main user interaction surface is an ordinary natural-language conversation with an agent. Users should not be expected to learn a command vocabulary, adopt a command-first workflow, or manage the system through a user-facing CLI.

The markdown filesystem remains the source of truth. The knowledge base stays inspectable, editable, portable, and platform-neutral even if an execution layer is added around it.

## Direction

- Atomic Knowledge is chat-native, not CLI-first.
- The primary entry point for ordinary users is natural-language chat.
- Any future runtime should be positioned as an agent-facing execution layer over the existing filesystem protocol.
- If a CLI exists, it should be treated as a developer or debugging helper, not as the main product entry.
- The V1 direction is a small runtime surface for high-value agent actions, not a MemPalace-style complete software product.

## Product Boundary

Atomic Knowledge should not move toward a store-everything memory product. It should not default to vector storage as the primary system of record, and it should not introduce a user-visible command system that makes ordinary usage more complex.

The purpose of a runtime, if introduced, is to help agents execute the existing protocol more reliably. It is not to replace the markdown knowledge base, hide the filesystem behind a proprietary application layer, or redefine the product as a command-driven tool.

## V1 Scope

- `init`
- `check`
- `context`
- `validate`

## Out Of Scope

- transcript archive
- vector search as primary storage
- end-user CLI workflow
- AAAK-like compression layer
