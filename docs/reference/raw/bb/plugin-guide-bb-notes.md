# Plugin Guide — bb (source notes)

> Source: https://getbb.app/plugin-guide
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-04 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — Footer: © 2026 Terragon Labs, Inc.; no content license. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/getbb-app-d83bf031/001.md.
> Work: https://getbb.app/plugin-guide
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

The bb Plugin Guide page (getbb.app/plugin-guide), an index of every plugin surface in the bb app, with links to per-topic slides. Footer credits Terragon Labs, Inc. No explicit date.

## Key facts

- The page groups plugin extension points into: app window, command palette, composer, home page, plugin settings page, plugin page, and plugin backend.
- App window surfaces include sidebar navigation, full-page panels, thread row status icons, replacing the thread list, sidebar footer items, thread header controls, thread menu actions, timeline entry content, rich message embeds, inline code-block renderers, message actions, in-thread forms (ask the person a question and return the answer to the agent), Thread Info rows and sections, code and diff renderers, browser toolbar controls, thread side-panel tabs, file viewers and editors, app-wide overlays and app-wide scripts.
- Composer surfaces include replacing the prompt box, banners, draft prompt state and locking, mentions (triggered by @ or other triggers), draft prompt highlighting, the + and send menus, agent providers (an agent selectable in the model picker) and inline actions.
- Home surfaces: home-screen sections and a new-thread side panel. Settings: declarative settings fields without UI code, and custom settings sections. A configuration-status warning can be shown on the plugin page.
- Plugin backend capabilities: `bb` CLI commands for people and agents; agent tools, skills and instructions injected into every agent session; background work on the bb server when no window is open; HTTP, WebSocket, RPC and realtime messaging; lifecycle events when threads change state or environments are removed; a dispatch hook that runs a check before each message reaches an agent.
- Further backend items: environment providers (new places a thread can run), machine providers (for example cloud sandboxes), machine server access, host workers running on enrolled machines, provider bridges that run an agent's sessions through a bridge shipped to each machine, plugin-private storage on the bb server, the bb SDK, a private JSON metadata record per thread, desktop browser control, AI services (models that write titles, commit messages and transcripts), host components (chat, prompt box, pickers) and testing harnesses that run without bb.
- Relevance: the dispatch hook, lifecycle events, per-thread plugin metadata, agent providers and provider bridges are candidate integration points for syncing or sharing agent sessions.

## Related

- getbb.app landing page, get-bb/bb repository docs.
