# Bootstrap Prompt

Paste the line below into an agent that can read local files and run shell commands:

```text
Please install the platform-neutral version of Atomic Knowledge from this repository: read `universal/README.md`, run `bash universal/scripts/init-kb.sh "$HOME/Desktop/My-Knowledge"`, then read the generated `$HOME/Desktop/My-Knowledge/AGENT.md` and adapt or install its instructions into this agent system's persistent instruction surface. After installation, keep the user in the same ordinary chat workflow: interpret natural-language requests like `ingest this link`, `continue our earlier topic`, `save this as a candidate`, `promote this candidate`, `merge this into the project or insight`, `run maintenance`, `review open candidates`, and `check knowledge-base health` as workflow intents rather than requiring platform-specific commands or extra UI. Read proactively for continuation and context recovery, but keep writes consent-based: suggest ingest or maintenance when useful, do not treat summarizing a link as ingest, and ask explicitly before deletes, bulk cleanup, or structural reorganization. Execute clear authorized cases directly with low interruption, and ask only short clarifying questions when the target or writeback action is genuinely ambiguous. If this platform has no persistent instruction surface, treat that file as the startup protocol for future sessions.
```

Adjust the knowledge-base path if needed.
