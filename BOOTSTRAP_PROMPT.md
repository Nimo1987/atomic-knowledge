# Bootstrap Prompt

Paste this into an agent that can read local files and run shell commands.

```text
Please bootstrap Atomic Knowledge for me from this repository. You can read local files and run shell commands, so handle the setup for me instead of asking me to figure out commands. Use `bash scripts/init-kb.sh "$HOME/Desktop/My-Knowledge"` unless I ask for a different location. Then read the generated `$HOME/Desktop/My-Knowledge/AGENT.md` and install or adapt it into this agent system's persistent instruction surface if possible; if not, use it as the startup protocol for future sessions. Keep the setup brief, ask only if you need a different path or a permission-sensitive change, and after initialization keep working with me in the same normal chat. I should not need to learn CLI, MCP, or runtime details to use Atomic Knowledge.
```

Adjust the knowledge-base path if needed.
