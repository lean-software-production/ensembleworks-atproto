# Extensions (source notes)

> Source: https://pi.ubitools.com/extensions/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-01 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: unknown — Mirror footer: (c) 2026 Community contributors; no license stated on the mirror. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/pi-ubitools-com-b65e1c1e/001.md.
> Work: earendil-works/pi:packages/coding-agent/docs/extensions.md
> Quotations: 37 characters verbatim in this file; 37 of 90 allowed for this work across the knowledge base.

## About this source

A web rendering of the pi coding agent's Extensions documentation, hosted at pi.ubitools.com (footer credits community contributors; no license statement was found). The text matches the opening and structure of the extensions document in the earendil-works/pi repository, so it is treated as a mirror of that work. The page shows no publication date. These are factual notes, not the original text.

## Key facts

- Extensions are TypeScript modules that extend pi's behavior: they can subscribe to lifecycle events, register custom tools callable by the model, add commands, and more.
- Auto-discovery locations are `~/.pi/agent/extensions/` (global) and `.pi/extensions/` (project-local). The command `pi -e ./path.ts` is recommended only for quick tests, and auto-discovered extensions can be hot-reloaded with `/reload`.
- Security stance of the docs: extensions run with full system permissions and can execute arbitrary code, so only trusted sources should be installed. Project-local extension entries load only after the project is trusted.
- A `project_trust` event fires before pi decides whether to trust a project with dynamic configs (`.pi` or `.agents/skills`); handlers return one of yes, no or undecided. The first yes or no decision from a user, global or CLI extension wins.
- `ctx.isProjectTrusted()` reports whether project-local trust is active, and is meant to be used before reading project-local extension configuration.
- Session lifecycle events documented: `session_start` (with reasons such as startup, new, resume, fork and reload), `session_before_switch`, `session_before_fork`, `session_before_compact` / `session_compact`, `session_before_tree` / `session_tree`, and `session_shutdown`. Several of the before-events can cancel or customize the action.
- State persistence: `pi.appendEntry` stores extension state in the session without taking part in model context. On reload, extensions rebuild state by scanning `ctx.sessionManager.getEntries()` for custom entries with their own `customType`.
- Alternative state pattern: keep state in tool result details so it branches correctly with the session tree, rebuilt from `ctx.sessionManager.getBranch()` at session start.
- `pi.sendMessage` injects a custom message with a `customType`, `content`, `display` flag and `details`; delivery modes are steer (default), followUp and nextTurn, plus an option to trigger a turn when idle.
- `pi.sendUserMessage` sends an actual user message that appears as if typed by the user and always triggers a turn. Input events carry a source of interactive, rpc or extension. Observation: this is the same user-attribution concern raised in a bb issue about plugin-originated messages for plugins, but here pi itself labels the source.
- `ctx.sessionManager` is read-only access to session state: `getEntries()`, `getBranch()`, `getLeafId()`. The docs point to the session-format document for entry types.
- `pi.setSessionName` / `pi.getSessionName` manage the display name, and `pi.setLabel` attaches labels to entry ids.
- `pi.registerMessageRenderer` customizes how messages with a `customType` render in the TUI.
- Mode behavior table: interactive mode has `ctx.mode` of tui with UI; RPC mode (`--mode rpc`) has UI via a JSON protocol; JSON mode (`--mode json`) streams events to stdout without UI; print mode (`-p`) runs extensions that cannot prompt.
- Example use cases listed include permission gates (confirm before destructive commands), path protection (block writes to `.env`), git checkpointing, custom compaction and external integrations such as webhooks.
- `pi.registerProvider` and `pi.unregisterProvider` let extensions add or remove model providers; `pi.exec` runs commands; `pi.events` is an event bus between extensions.
- Observation: a sharing extension for ATProto could hook `session_start`, `session_shutdown` and the agent events, and use `appendEntry` to remember what has been published, without altering model context.

## Quotations

- The documentation warns that extensions "run with your full system permissions" (pi extensions docs, mirrored).

## Related

pi coding agent, SessionManager, session format version 3, extension API, RPC mode, project trust, bb Pi provider (which runs Pi in RPC mode per a bb plugin README).
Relation to the other mirror (hochej.github.io): that mirror is an older snapshot; it still uses session switch and session fork after-events and shows no `project_trust` event.
