# Pi Extension Development (source notes)

> Source: https://lobehub.com/skills/kanatti-pipi-pi-extension-dev
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-06 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — No license statement for this content on the page. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/lobehub-com-e54b3abb/001.md.
> Work: https://lobehub.com/skills/kanatti-pipi-pi-extension-dev
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A LobeHub Skills Marketplace listing titled Pi Extension Development, a quick reference for writing pi extensions, apparently from a user repo called pipi (kanatti). It uses the older `@mariozechner/pi-coding-agent` package scope. Published date is not shown. No license statement for the content appears on the page.

## Key facts

- Extensions are TypeScript modules with a default exported function taking `ExtensionAPI`, which can subscribe to events and register tools, commands and shortcuts.
- Imports listed: `@mariozechner/pi-coding-agent`, `@sinclair/typebox` for tool parameter schemas, `@mariozechner/pi-ai` (StringEnum, for Google-compatible enums) and `@mariozechner/pi-tui`. Newer pi docs use the @earendil-works scope, so the scope here is outdated.
- Lifecycle events shown: `session_start`, `session_shutdown`, `before_agent_start` (can return an extra message and a modified system prompt). Tool events: `tool_call` (can return a block result) and `tool_result`. Turn events: `turn_start`, `turn_end`, `context` (can replace messages before the LLM call).
- Tool registration takes name, label, description, parameters, and `execute(toolCallId, params, signal, onUpdate, ctx)`, returning content plus details. Optional `renderCall` and `renderResult` give custom rendering.
- Tool output should be truncated; the sample uses `truncateHead` with `DEFAULT_MAX_BYTES` (50KB) and `DEFAULT_MAX_LINES` (2000).
- Commands use `pi.registerCommand`; the handler can read `ctx.sessionManager.getEntries()`.
- `ctx` properties include ui, hasUI (false in print mode), cwd, sessionManager, model, modelRegistry, `isIdle()`, `abort()`, `shutdown()`, `getContextUsage()`.
- API methods include `pi.sendMessage`, `pi.sendUserMessage`, `pi.appendEntry`, `pi.setSessionName`, `pi.setLabel`, `pi.getActiveTools`, `pi.setActiveTools`, `pi.setModel`, `pi.setThinkingLevel`, and an event bus `pi.events`.
- State advice: store state in tool result details so branching works; rebuild it at `session_start` by walking `ctx.sessionManager.getBranch()`. Session entries have a type and a message with toolName and details.
- Discovery locations: `~/.pi/agent/extensions/*.ts`, `.pi/extensions/*.ts`, `extensions/*/index.ts`, or an `extensions` array in settings. Test with `pi -e ./extension.ts`.

## Related

- Official pi extensions docs, piagent.fyi Extensions 101 guide.
