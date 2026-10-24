# Pi Agent in Practice: Setup, Custom Extensions & 5 Best Practices (source notes)

> Source: https://hoangyell.com/pi-agent-setup-best-practices/
> Collected: 2026-10-23
> Published: 2026-09-25
> Representation: Source notes written by fetcher-04 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — Footer: © 2026 Hoang Yell; no content license. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/hoangyell-com-fc5d650d/001.md.
> Work: https://hoangyell.com/pi-agent-setup-best-practices/
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A hands-on guide by Hoang Yell (blog hoangyell.com), dated September 25 on the page (the year runs into the reading-time text), covering setup, extensions and practices for the pi coding agent. Third-party and informal (it includes a homelab sidebar and SEO-style boxes); several claims differ from other pi sources, so treat as secondary.

## Key facts

- Install: `npm install -g --ignore-scripts @earendil-works/pi-coding-agent`, or a script at pi.dev/install.sh; the guide says Node.js 22.19 or higher is required. Verify with `pi --version`.
- Auth: `/login` stores keys in `~/.pi/agent/auth.json` with `0600` permissions, per the guide; env vars such as `ANTHROPIC_API_KEY` also work. Local models are configured in `~/.pi/agent/models.json` (example uses Ollama at `http://localhost:11434/v1` with api `openai-completions`).
- Tools: the guide says 7 built-in tools (`read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`) and says older guides listing 4 are outdated; restrict with `--tools`. This contradicts the gist and the DevelopersDigest article, which describe 4 default tools with grep, find, ls optional.
- Four-tier customization ladder: prompt templates (markdown in `~/.pi/agent/templates/`), Agent Skills (`SKILL.md` in `~/.pi/agent/skills/` or `.agents/skills/`), TypeScript extensions (`~/.pi/agent/extensions/`), and custom providers via `models.json`.
- Extension API example: default export taking `ExtensionAPI`; `registerCommand` and an event hook on `tool_call` to intercept `bash` calls and throw to block; `ctx.ui.notify` for messages; load with `pi --extension ./guardrails.ts`; `/reload` hot-reloads.
- Execution modes: interactive, print (`-p`), JSON event stream (`pi --mode json`), RPC (`pi --mode rpc`, stdin/stdout JSONL, suited to custom GUI or IDE clients).
- Session commands: `/tree`, `/fork` (new session from a prior user prompt), `/clone` (duplicate active branch), `/resume` (picker to search, rename or prune). Sessions are stored as a JSONL tree.
- The guide says pi propagates an `x-session-id` header through compatible inference gateways, to help provider-side prompt caching.
- Steering: `Enter` steers, `Alt + Enter` queues a follow-up, `Esc` aborts and returns the buffer to the editor.
- Safety caveats stated by the author: `trust.json` only manages command execution approval and is not a process sandbox; recommends Docker or `bwrap` for untrusted code. Warns about context saturation (use `/compact`).
- Package count: refers to a 7-package monorepo in a linked article (differs from the 5 packages in DevelopersDigest and 3 in the gist); also says pi-ai talks to 20+ providers.
- Relevance for session sharing: JSONL tree sessions, RPC mode and `--mode json` event streams are candidate hooks for exporting or syncing sessions.

## Related

- Official pi docs, DevelopersDigest deep dive, the author's Pi Mono explainer.
