# get-bb/bb#1668: Pi SDK bridge does not expose standard extension UI requests to BB (source notes)

> Source: https://github.com/get-bb/bb/issues/1668
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-07 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue: user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-3b31c6c9/001.md.
> Work: get-bb/bb#1668
> Quotations: 66 characters verbatim in this file; 66 of 90 allowed for this work across the knowledge base.

## About this source

Issue get-bb/bb#1668, "Pi SDK bridge does not expose standard extension UI requests to BB". Opened by thesobercoder on 2026-08-16; closed as completed on 2026-10-08. Labels: providers, provider-pi. One comment by ymichael.

## Key facts

- Problem: bb's Pi bridge calls `session.bindExtensions` with `mode: "rpc"` plus abort, shutdown and error handlers but passes no `uiContext`, so `ctx.hasUI` is false inside Pi extensions.
- Consequently standard extension UI calls (`ctx.ui.confirm()`, `ctx.ui.select()`, `ctx.ui.input()`, `ctx.ui.editor()`, `ctx.ui.notify()`) cannot reach bb's interface; an extension checking `ctx.hasUI` can only fail closed or use its own fallback.
- The issue states that `mode: "rpc"` does not itself create the extension UI transport when an application embeds Pi via the SDK; the embedder must supply an `ExtensionUIContext`.
- Related earlier work: issue #1391 added `bindExtensions()` so extensions receive `session_start` and `session_shutdown`; this issue covers the separate UI gap. Provider bridge work referenced as #1640.
- Expected flow: extension calls a UI method, a bb adapter creates a correlated bridge request, bb creates a pending interaction and shows it, the user answers, the response goes back through the bridge, the extension promise resolves.
- Suggested implementation: an `ExtensionUIContext` adapter in the Pi bridge; messages via the bb provider bridge protocol; approval-like requests mapped to bb's existing pending-interaction system; request IDs scoped to session, thread and turn; cancel unresolved requests on session stop or replacement; validate responses; fail closed on timeout or disconnect. Pi CLI RPC `extension_ui_request` and `extension_ui_response` messages are named as a reference.
- Scope: portable methods `confirm`, `select`, `input`, `editor`, and `notify` where applicable. `ctx.ui.custom()` is excluded since it takes an executable Pi TUI component factory that cannot be serialized.
- Acceptance criteria include `ctx.hasUI` true, validated responses, old-session responses unable to resolve new-session requests, and tests for correlation, cancellation and session replacement.
- Relevant file named: `packages/agent-runtime/src/pi/bridge/sdk-session.ts`.
- Resolution: ymichael commented on 2026-10-08 that PR #3228 fixed it; Pi select, confirm, input and editor requests now appear as answerable bb interactions.

## Related

bb provider-pi; Pi SDK and RPC docs (extension UI protocol); bb pending interactions; get-bb/bb PR #3228.
