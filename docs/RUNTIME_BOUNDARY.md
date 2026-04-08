# Runtime Boundary

Atomic Knowledge remains a chat-native, protocol-first system.

This note defines which capabilities should stay in the protocol and agent judgment layer, which capabilities are suitable for runtime assistance, and which capabilities should stay out of the V1 runtime.

## Boundary Rule

The runtime exists to help an agent execute bounded, mechanical knowledge-base steps more reliably. It is not a replacement for agent judgment, and it should not turn Atomic Knowledge into a command-driven system for end users.

## Boundary Table

| Capability | Owner | Reason |
|------------|-------|--------|
| interpreting user intent | Protocol / Agent Judgment | Natural-language intent mapping is semantic judgment, not a deterministic filesystem operation. |
| deciding whether the user asked for analysis vs writeback | Protocol / Agent Judgment | This is an authorization and autonomy decision that depends on conversational meaning. |
| deciding whether material is durable | Protocol / Agent Judgment | Durability is a reuse and quality judgment, not a structural check. |
| deciding `candidate` vs `insight` vs `project` vs `merge` | Protocol / Agent Judgment | Routing depends on meaning, confidence, reuse horizon, and relation to existing knowledge. |
| deciding when explicit confirmation is required | Protocol / Agent Judgment | Confirmation policy is part of safe agent behavior for high-impact actions. |
| producing final synthesis / explanation for the user | Protocol / Agent Judgment | The final answer requires interpretation, prioritization, and user-facing communication. |
| initializing a knowledge base | Runtime | This is a bounded setup operation over a known filesystem structure. |
| running a health check | Runtime | Health checks are repeatable inspections over directories, files, and freshness metadata. |
| generating a recommended context/read set | Runtime | A runtime can assemble a stable starting read set from entry pages and known structure without deciding the final answer. |
| validating structure/frontmatter/links | Runtime | Validation is a mechanical consistency check over markdown content and knowledge-base structure. |
| automatic ingest summarization | Out Of Scope For V1 | This adds interpretation and implicit content processing pressure that should stay under agent judgment in V1. |
| semantic/vector retrieval as the main memory layer | Out Of Scope For V1 | The markdown filesystem remains the source of truth, not a vector-first memory system. |
| auto-promotion of candidates | Out Of Scope For V1 | Promotion changes knowledge status and should not happen without explicit judgment about durability and destination. |
| bulk autonomous maintenance refactors | Out Of Scope For V1 | Large-scale cleanup and reorganization are high-impact operations that require conservative human-facing control. |
| persona-memory features | Out Of Scope For V1 | Atomic Knowledge is not a persona-memory product. |
| transcript archive system | Out Of Scope For V1 | Atomic Knowledge is not intended to become a raw conversation archive. |
| end-user command vocabulary or CLI-first workflow | Out Of Scope For V1 | The product direction remains chat-native rather than command-driven. |

## What Should Stay Protocol-Only

Keep capabilities in the protocol and agent layer when they require interpreting conversation meaning, applying autonomy rules, making durability judgments, or deciding how to explain outcomes back to the user.

In practice, the protocol owns intent interpretation, write authorization, page-type routing, confirmation boundaries, and final synthesis.

## What Fits Runtime-Assisted

Use the runtime for bounded operations that act on the knowledge base structure directly and can be executed consistently without deciding what the user meant or what the knowledge means.

For V1, this supports a small execution layer around initialization, health checking, recommended context/read-set generation, and structural validation.

## What Should Not Enter V1 Runtime

Do not use the V1 runtime to automate semantic memory behavior, implicit summarization, candidate resolution, bulk autonomous cleanup, persona storage, or transcript archiving.

Those directions would blur the protocol boundary and push Atomic Knowledge toward a different product shape than the current chat-native markdown system.
