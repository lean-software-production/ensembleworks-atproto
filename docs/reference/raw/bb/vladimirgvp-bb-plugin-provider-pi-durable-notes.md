# VladimirGVP/bb-plugin-provider-pi-durable (source notes)

> Source: https://github.com/VladimirGVP/bb-plugin-provider-pi-durable
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-05 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — GitHub API reports no license detected for repo. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-205bad1b/001.md.
> Work: VladimirGVP/bb-plugin-provider-pi-durable
> Quotations: 21 characters verbatim in this file; 21 of 90 allowed for this work across the knowledge base.

## About this source

README and repository metadata of a GitHub repository `VladimirGVP/bb-plugin-provider-pi-durable`, a provider plugin for the BB IDE (Beyond Boundaries) that runs BB threads on a "Pi Durable" engine. The repo is a fork of `VanDalkvist/bb-plugin-provider-pi-durable`, created 2026-10-15, with 0 stars. No license is detected by the GitHub API (the README's License section says `MIT`, but no license file was detected). No explicit publication date.

## Key facts

- Purpose: run BB IDE threads with the Pi Durable runtime, where each thread is backed by a transactional SQLite store, `session.sqlite`.
- Claimed benefits: no token loss on crash or `kill -9`, deterministic thread resumption, a persistent task graph, and subagent orchestration.
- Ships a pre-bundled RPC bridge runner at `dist/runner/index.js`, so no external binaries are needed.
- Design invariant: the plugin is a thin protocol bridge (a pure bidirectional adapter) and does not own prompts, agent rules or domain mechanics.
- Four "territories": (1) BB IDE host and UI using Plugin SDK and JSON-RPC methods `turn/start`, `turn/delta`, `thread/stop`; (2) Pi Durable core `@earendil-works/pi-durable` with FSM tasks, SQLite WAL persistence, copy-on-write forks, document mounts and deterministic replay; (3) the Pi ecosystem `@earendil-works/pi-coding-agent` with settings, MCP discovery and `~/.pi/agent/settings.json`; (4) the provider plugin itself.
- The plugin translates BB JSON-RPC requests into Pi Durable harness commands and FSM events into BB wire events and chat deltas. Transport is JSON-RPC over stdio.
- Some upstream primitives (foreground subagents, multi-process SQLite session lockfile management) exist only in `packages/coding-agent/src/experimental/durable/`; they are copied into `src/runner/upstream/` with provenance.
- Features: terminal widget streaming bash output, diff viewer for `edit` and `write` tool calls, thinking accordion, context window meter, output capture for `bb thread output <thread-id>`, model switching (Google Antigravity, Anthropic, OpenAI) with thinking levels `none`, `low`, `medium`, `high`, `xhigh`, `max`.
- MCP servers are read from `~/.pi/agent/mcp.json` and tools from `settings.json`; credentials come from `~/.pi/agent/auth.json` after logging in via the `pi` CLI.
- Requirements: BB IDE `>= 0.45.0`; Node.js `>= 22.19.0` (for built-in `node:sqlite`).
- Session directory: `~/.bb/pi-bridge-sessions/`.
- Environment overrides: `BB_PI_DURABLE_PACKAGE_PATH`, `BB_PI_DURABLE_BRIDGE_COMMAND`, `BB_PI_DURABLE_BRIDGE_ARGS` (JSON array, default `[]`).
- Top-level repo files include `AGENTS.md`, `PLUGIN_OVERVIEW.md`, `CHANGELOG.md`, `server.ts`, `app.tsx` and directories `skills`, `src`, `tests`, `docs`.

## Related

- BB IDE plugin SDK, Pi coding agent, pi-durable (earendil-works), upstream repo `VanDalkvist/bb-plugin-provider-pi-durable`.
