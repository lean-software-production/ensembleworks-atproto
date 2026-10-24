# pi.dev - How It Differs from Other AI CLI Tools (gist by rajeshpv) (source notes)

> Source: https://gist.github.com/rajeshpv/eccc1dc8d70e8cdcf948de3312ca111f
> Resolved: https://api.github.com/gists/eccc1dc8d70e8cdcf948de3312ca111f
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-04 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — Public gist by rajeshpv; no license stated. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/gist-github-com-3490aecc/001.md.
> Work: gist.github.com/rajeshpv/eccc1dc8d70e8cdcf948de3312ca111f
> Quotations: 19 characters verbatim in this file; 19 of 90 allowed for this work across the knowledge base.

## About this source

A public GitHub gist by user rajeshpv containing one file, `pi.dev.details.md`, a comparison of the pi coding agent with other AI CLI tools. It is a third-party summary, not official documentation. No publication date is shown in the content.

## Key facts

- The author describes pi as a minimal terminal coding agent by Mario Zechner, MIT licensed, installed via `npm install -g @mariozechner/pi-coding-agent`.
- It has 4 built-in tools: `read`, `write`, `edit`, `bash`.
- Four run modes: interactive TUI, print/JSON (`pi -p "query"`, `--mode json` for event streams), RPC (JSON over stdin/stdout for non-Node integrations) and SDK (embed via TypeScript API).
- The author lists features pi deliberately leaves out of core: MCP, sub-agents, permission popups, plan mode, built-in to-dos and background bash; suggested substitutes are skills, tmux, containers, files, and extensions. The author says 50+ example extensions are provided.
- Models: the author says 15+ providers; switch mid-session with `/model` or `Ctrl+L`, cycle favorites with `Ctrl+P`.
- Sessions are tree-structured JSONL files (id/parentId) in `~/.pi/agent/sessions/` organized by working directory; `/tree` navigates and branches; all branches live in one file. Flags `-c` (continue) and `-r` (resume) are mentioned.
- Sessions can be exported to HTML or uploaded to a GitHub gist with a rendered shareable URL, according to the author.
- Context controls: AGENTS.md / CLAUDE.md, SYSTEM.md, Skills (Agent Skills standard, agentskills.io), prompt templates, extension-injected context, customizable compaction.
- Per-project config under `.pi/settings.json`, `.pi/extensions/`, `.pi/skills/`.
- Monorepo packages named: `@mariozechner/pi-ai`, `@mariozechner/pi-agent`, `@mariozechner/pi-tui`. The author says "three core packages", which differs from other sources describing more packages.
- Steering: Enter sends a steering message, Alt+Enter queues a follow-up.
- Thinking level cycle: off/minimal/low/medium/high/xhigh with `Shift+Tab`.

## Related

- Official pi docs on sessions and session format, DevelopersDigest and Hoang Yell pi writeups.
