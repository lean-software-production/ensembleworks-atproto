# Extensions 101 (source notes)

> Source: https://piagent.fyi/guides/extensions-101/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-06 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — Footer says MIT but no license text or copyright holder; treated conservatively. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/piagent-fyi-2cda8bf9/001.md.
> Work: https://piagent.fyi/guides/extensions-101
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A third-party guide titled Extensions 101 on piagent.fyi, marked Intermediate, with Last updated Jul 27, 2026. It explains how pi extensions work and says it follows the pi repo documentation in docs/extensions.md. The page footer mentions MIT but supplies no license text, so this is treated as notes.

## Key facts

- An extension is a TypeScript module running inside the pi process with the user's full system permissions. The guide stresses it is not a sandboxed plugin.
- The module default-exports a factory function receiving an `ExtensionAPI` object, conventionally named pi. Pi loads files through jiti, so no compile step is needed. The factory may be async and pi awaits it before startup continues.
- Advice: do not start long-lived background resources inside the factory; defer them to `session_start` and close them in `session_shutdown`.
- Auto-discovered locations, hot-reloadable with `/reload`: `~/.pi/agent/extensions/*.ts`, `~/.pi/agent/extensions/*/index.ts` (global) and `.pi/extensions/*.ts`, `.pi/extensions/*/index.ts` (project-local).
- Project-local extensions load only after the project is trusted (trust prompt or `/trust`).
- Quick testing uses `pi -e ./path.ts`, repeatable, combinable with `--no-extensions`.
- Extensions can be shared as pi packages from npm or git using `pi install <source>`; extra paths go under `packages` or `extensions` in `settings.json`.
- Capabilities: `pi.on` for lifecycle events (handlers can block, modify or inject), `pi.registerTool` (same name as a built-in overrides it), `pi.registerCommand`, `pi.registerShortcut`, `pi.registerFlag`, `pi.registerProvider`, and `pi.appendEntry` to persist state into the session file. UI helpers on `ctx.ui` include select, confirm, input, notify, custom, setStatus and setWidget.
- Event order: `project_trust` (user/global extensions only), `session_start` with reason startup, `resources_discover`; per prompt `input`, `before_agent_start`, `agent_start`; per turn `turn_start`, `context`, `before_provider_request`, `after_provider_response`, `tool_execution_start`, `tool_call` (can block), `tool_result` (can modify), `tool_execution_end`, `turn_end`; then `agent_end` and `agent_settled`.
- Session operations: `/new` and `/resume` fire `session_before_switch`, `session_shutdown`, `session_start`; `/compact` fires `session_before_compact` and `session_compact`; model changes fire `model_select` and `thinking_level_select`.
- Example imports come from `@earendil-works/pi-coding-agent`, `typebox`, `@earendil-works/pi-ai` and `@earendil-works/pi-tui`.
- Example extensions named in the repo examples directory: hello.ts, confirm-destructive.ts, git-checkpoint.ts, question.ts, questionnaire.ts, todo.ts, custom-compaction.ts, summarize.ts, snake.ts.
- Security note repeated: extensions execute arbitrary code, so install only from trusted sources.

## Related

- pi.dev extensions documentation (pi-dev-docs-extensions), pi packages, custom providers docs.
- Relevant to sharing sessions: `pi.appendEntry` and the session events are the hooks an ATProto publishing extension would use.
