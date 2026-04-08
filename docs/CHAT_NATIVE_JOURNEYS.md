# Chat-Native Journeys

Atomic Knowledge should be usable through ordinary conversation.

The normal entry point for an ordinary user is chat with an agent, not a command surface. If a runtime exists, it should stay behind the agent as a hidden helper for bounded mechanical steps. The user should not need to learn internal workflow words such as `candidate`, `insight`, or `merge` in order to install, ingest, continue a topic, or run maintenance.

The interaction rule is simple:

- the user expresses intent in natural language
- the agent maps that intent onto the protocol workflow
- the runtime, if present, helps only with mechanical execution behind the scenes
- the user does not need to learn commands, switch modes, or understand the underlying file structure
- high-impact operations should still keep an explicit confirmation boundary

## Bootstrap / First Setup

### User Says

- `Set up Atomic Knowledge for this folder.`
- `Help me start a knowledge base for this project.`
- `I want this agent to remember our research here.`

### Agent Does

- Interprets the request as a setup intent inside the current conversation.
- Creates or prepares the knowledge base in the chosen location.
- Explains only the minimum the user needs to know to keep working in chat.
- Connects the setup to the user's existing agent workflow rather than sending the user into a separate tool or admin mode.
- Asks before directory changes or other setup choices that have broader impact.

### What The User Should Not Need To Do

- Learn a bootstrap command or shell workflow.
- Read the protocol first just to get started.
- Understand the full knowledge model before using it.
- Choose internal storage terms or page types during setup.

### Possible Hidden Runtime Help

- Initialize the knowledge-base structure behind the agent.
- Check that the required files and directories exist after setup.
- Validate that the initialized structure is consistent.
- Stay optional. If no runtime exists, the agent can still carry out the setup through the filesystem protocol directly.

## Ingest New Material

### User Says

- `Read this article and add the reusable parts to our knowledge base.`
- `Save this paper so we can build on it later.`
- `Put this transcript into our ongoing research.`

### Agent Does

- Treats the request as natural-language ingest intent rather than waiting for a command.
- Reads the material, extracts the important takeaways, and updates the right knowledge pages.
- Keeps the workflow inside the same chat instead of asking the user to choose internal destinations or labels.
- Distinguishes between analysis and storage. If the user only wants a summary, the agent should not silently ingest it.
- Uses normal language in the reply, even if the underlying protocol uses more specific internal terms.

### What The User Should Not Need To Do

- Run an `ingest` command.
- Manually choose between `candidate`, `insight`, `project`, or `merge`.
- Copy content into the right folders by hand.
- Learn the writeback structure before asking the agent to save something.

### Possible Hidden Runtime Help

- Confirm that the knowledge base is available and healthy before the write.
- Run bounded validation after the agent updates pages and links.
- Refresh structural status checks so the ingest does not leave the knowledge base in a broken state.
- Leave source interpretation, routing, and durability judgment to the agent rather than the runtime.

## Continue An Earlier Topic

### User Says

- `Continue our earlier discussion about agent memory.`
- `What did we conclude last time about this company?`
- `Before answering, check what we already know about this topic.`

### Agent Does

- Interprets the request as a continuation or knowledge consultation request.
- Recovers the relevant context from the knowledge base before answering.
- Uses the prior work to continue the thread in ordinary language.
- Asks a short clarifying question only if more than one earlier topic is a plausible match.
- Keeps read-side lookup proactive while treating writeback as a separate consent boundary.

### What The User Should Not Need To Do

- Remember file names or directory paths.
- Search the wiki manually before asking the question.
- Switch into a retrieval mode.
- Learn internal concepts like `recent`, `active`, `candidate`, or page routing rules.

### Possible Hidden Runtime Help

- Assemble a recommended read set from entry pages and known structure.
- Check whether the knowledge base is in a usable state before the agent relies on it.
- Support consistent context recovery without deciding what the user means.
- Leave interpretation, synthesis, and the final answer to the agent.

## Run Maintenance

### User Says

- `Run maintenance on the knowledge base.`
- `Clean up stale notes before we continue.`
- `Check whether this knowledge base is still healthy.`

### Agent Does

- Treats the request as maintenance intent expressed in ordinary language.
- Reviews the knowledge base for consistency, stale areas, and follow-up actions that fit the existing protocol.
- Explains the result in user-facing language instead of requiring the user to understand internal maintenance categories.
- Proceeds directly for ordinary maintenance steps that the request already authorizes.
- Stops for explicit confirmation before deletes, archives, bulk cleanup, large restructures, or other high-impact changes.

### What The User Should Not Need To Do

- Run a lint or check command manually.
- Inspect metadata files just to know whether maintenance is needed.
- Understand candidate queues, merge rules, or internal resolution states before asking for cleanup.
- Switch into a separate admin workflow.

### Possible Hidden Runtime Help

- Run health checks over the knowledge-base structure.
- Validate links, frontmatter, and other bounded consistency rules.
- Surface structural issues so the agent can decide what to fix or explain.
- Stay limited to mechanical checks, while the agent keeps responsibility for judgment and confirmation boundaries.

## Design Rule

If a new capability requires an ordinary user to first learn commands, adopt a mode switch, or understand the internal knowledge model before they can use it successfully, that capability is moving away from the current direction.

The default direction is chat-native: the user talks naturally, the agent maps intent to protocol behavior, and any runtime help stays hidden behind that experience.
