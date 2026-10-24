# Changelog - bb (source notes)

> Source: https://getbb.app/changelog
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-07 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — no license statement found in page HTML. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/getbb-app-c453d492/001.md.
> Work: https://getbb.app/changelog
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

The bb changelog page on getbb.app as fetched. The extraction contains one entry, release 0.43.3, dated September 18, 2026 (the page's own date for that release).

## Key facts

- Release 0.43.3 headline themes: saved drafts, browser annotations, live browser previews.
- A Drafts plugin is bundled and on by default; messages saved from composers can be sent later.
- Handoffs were redesigned: handoff from the follow-up composer keeps the draft and workspace, to another provider or another model of the same provider.
- Settings let users choose per provider whether finished turns collapse; Claude Code defaults to expanded.
- BB Guide now tells agents to wait for a user request before creating or messaging other bb threads (an agent-safety guardrail).
- An Agent Annotations plugin lets users select elements in bb's desktop browser and comment; the agent receives element details and React component info.
- Headless Browser Automation sessions show a live preview in chat.
- Project environment variables override machine-wide defaults for agent turns, terminals and project setup; import from a `.env` file.
- Experimental: moving the bb server data and plugin state to another enrolled machine; repositories, workspaces and provider sessions stay on their machines.
- Experimental multi-machine picker separates machine selection from environment selection.
- Provider Usage unifies pooled and machine-local accounts; custom ACP agents can opt into usage reporting; nested bb instances can use the parent's Account Pooler for Claude and Codex.
- A persistent telemetry opt-out exists in settings.
- Fixes: clearing Pi context starts a fresh session; ACP question cancellation and late answers handled more reliably; failed voice recordings retained, upload limit raised to 20 MB.
- CLI: `bb diagnostics cli-errors` summarizes local command failures; finished terminal output stays readable for 30 minutes after exit; `terminal read` and `terminal wait` improved; local attachments upload before CLI thread requests; `bb plugin rpc list` and `bb plugin rpc inspect` inspect plugin RPCs.
- Plugin APIs: `app.commands.register` for app commands; `defineCli` and `cliCommand` for CLI commands; experimental browser extensions; experimental composer controls; `bb.ui.requestInput` forms can outlive the agent's turn; experimental `experimental_discoverRpc` to publish method descriptions and schemas; experimental dispatch context exposing queued messages with author and origin; dependent threads that archive or delete with their owner; SDK access to project environment variables; experimental `hosts.experimental_reconcile` for suspended machines.
- Upgrade note for plugin authors: `app.slots.commandPaletteAction` stays as a deprecated alias for `app.commands.register`; dispatch hooks use `queuedMessages`, `initiator` and `senderThreadId` instead of the old singular queue and requester fields.
- The release thanks external contributors by GitHub handle.

## Related

bb plugins and SDK; ACP; Pi provider integration; get-bb/bb issues and marketplace.
