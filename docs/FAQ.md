# Use Cases and FAQ

This page is for people who understand the basic idea, but want a simpler answer to: what is this for, and when would I actually use it?

## Typical Use Cases

### 1. Ongoing Research Topics

You keep asking your agent about the same topic over time:

- AI tools
- product strategy
- market research
- technical architecture
- a startup idea you are evaluating

Without a maintained knowledge layer, every new session tends to start from scratch.

Atomic Knowledge helps the agent continue from what you already explored.

### 2. Link-Heavy Work

You regularly send the agent:

- links
- PDFs
- notes
- transcripts
- screenshots or summaries from elsewhere

The useful result is often not the link itself, but the conclusion that emerged after discussing it.

Atomic Knowledge gives those conclusions a place to live outside chat history.

### 3. Long-Running Personal Projects

You are working through something that lasts days or weeks, for example:

- choosing a tool stack
- refining a product idea
- mapping a research direction
- comparing vendors
- writing and revising a thesis or plan

In these cases, you do not just want answers. You want continuity.

### 4. “Don’t Make Me Repeat Myself” Work

One of the most common frustrations with agents is:

- you already discussed this
- you already shared the link
- you already found the key tradeoff
- but the next session behaves like none of that happened

Atomic Knowledge exists to reduce that repetition.

## FAQ

### Do I need to switch to a new AI app?

No.

The idea is to keep using your existing agent. Atomic Knowledge is a protocol and local knowledge layer that plugs into that workflow.

### Is this just another memory plugin?

No.

Memory plugins usually focus on remembering things about the user, such as preferences or profile facts.

Atomic Knowledge focuses on remembering the work: what you and the agent have already researched, concluded, compared, or decided to keep.

### Is this just RAG?

Not exactly.

RAG usually helps an agent look up raw material at answer time.

Atomic Knowledge is about maintaining a cleaner layer above that raw material, so the agent can reuse prior conclusions instead of rediscovering them every time.

### Does it store every conversation?

No.

It is intentionally more selective than that.

The goal is not to archive all chat. The goal is to keep durable work memory.

### What kinds of things should be kept?

Examples include:

- stable comparisons
- reusable frameworks
- project-level decisions
- summaries worth keeping for future work
- unresolved but promising ideas that should stay in the candidate buffer

### What kinds of things should not be kept?

Usually not:

- random small talk
- every message in a discussion
- one-off task state
- user persona details unless they matter to the work itself

### Will the agent save things automatically without asking me?

It should not do that by default.

The intended boundary is:

- reading and lookup can be proactive
- suggestions can be proactive
- writing to the knowledge base needs user consent
- high-impact cleanup or reorganization needs explicit confirmation

### Then how do I tell the agent to save something?

Usually in ordinary language, for example:

- `ingest this link`
- `save this as a candidate`
- `merge this into the project`
- `run maintenance`

If your words already clearly mean “please record this”, the system treats that as authorization.

### Do I need to learn words like `candidate` or `insight`?

No.

Those are internal workflow labels.

In normal use, you should be able to say natural things such as:

- `把这个链接收进去。`
- `这个先记一下，先别当正式结论。`
- `这个已经比较确定了，正式记下来。`
- `把这个并到之前那个主题里。`
- `整理一下知识库。`

The system should map those plain-language requests onto the internal workflow for you.

It should prefer the language you are already using in the conversation. If that is unclear, it should fall back to your system language or another stable language preference signal.

### What does the candidate layer do?

It is a holding area for useful but not-yet-stable work memory.

That helps the system avoid two bad outcomes:

- losing a valuable idea completely
- promoting a half-baked thought into formal knowledge too early

### Who is this best for?

People who:

- already use agents often
- revisit the same topics over time
- care about continuity across sessions
- are willing to use a local markdown/file-based workflow

### Who is this not best for?

People who:

- only want one-off answers
- mainly want profile memory
- do not want any local file workflow
- use agents in environments with no file access or shell support

### What should I read first if I want to understand it quickly?

Start with:

1. [Comparison](COMPARISON.md)
2. [Agent-Native Usage](AGENT_NATIVE_USAGE.md)
3. [Example KB Walkthrough](../example-kb/WALKTHROUGH.md)
4. [Eval Scenarios](../evals/README.md)

### What should I do first if I want to try it?

1. Run `bash scripts/init-kb.sh "$HOME/Desktop/My-Knowledge"`
2. Put the generated `AGENT.md` into your agent platform, or tell the agent to read it at session start
3. Try one of the eval scenarios in `evals/`

## One-Sentence Explanation

If you need the plainest possible explanation:

Atomic Knowledge gives your existing AI assistant a cleaner long-term working memory, so it can keep building on what you already figured out together instead of starting over every new session.
