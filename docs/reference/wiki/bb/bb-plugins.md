# bb Plugin System

> Sources: get-bb/bb `docs/configuration.md` (Michael Yong / bb contributors, MIT), undated; Diffuzmetall/bb-plugin-pi-command-sync README (MIT); getbb.app Plugin Guide (Terragon Labs, notes only); get-bb/bb issue #3621 (notes only); all collected 2026-10-23; source inventory: get-bb/bb: docs/configuration.md (Copyright (c) 2026 Michael Yong, get-bb/bb; Unknown); Diffuzmetall/bb-plugin-pi-command-sync (Copyright (c) 2026 bb-plugin-pi-command-sync contributors, Diffuzmetall/bb-plugin-pi-command-sync; Unknown); Plugin Guide — bb (source notes) (attributed source notes; Unknown); get-bb/bb#3621: Plugin-originated thread messages are indistinguishable from user input (initiator=user, senderThreadId=null) (source notes) (attributed source notes; Unknown); Bb Plugin Authoring (source notes) (attributed source notes; Unknown); Changelog - bb (source notes) (attributed source notes; Unknown); get-bb/marketplace#410: Add plugin entry: hooks (source notes) (attributed source notes; Unknown); get-bb/bb#4809: Thread list: date group headings (Today, Yesterday, …) in the Custom organization's Threads section (source notes) (attributed source notes; Unknown); get-bb/bb: packages/plugin-sdk/README.md (Copyright (c) 2026 Michael Yong, get-bb/bb; Unknown)
> Raw: [bb configuration.md](../../raw/bb/get-bb-bb-docs-configuration-md.md); [bb-plugin-pi-command-sync](../../raw/bb/diffuzmetall-bb-plugin-pi-command-sync.md); [getbb.app Plugin Guide (notes)](../../raw/bb/plugin-guide-bb-notes.md); [get-bb/bb#3621 (notes)](../../raw/bb/get-bb-bb-3621-plugin-originated-thread-messages-are-notes.md); [bb-plugin-authoring-notes](../../raw/pi/bb-plugin-authoring-notes.md); [changelog-bb-notes](../../raw/bb/changelog-bb-notes.md); [get-bb-marketplace-410-add-plugin-entry-hooks-notes](../../raw/bb/get-bb-marketplace-410-add-plugin-entry-hooks-notes.md); [get-bb-bb-4809-thread-list-date-group-headings-today-notes](../../raw/bb/get-bb-bb-4809-thread-list-date-group-headings-today-notes.md); [get-bb-bb-packages-plugin-sdk-readme-md](../../raw/bb/get-bb-bb-packages-plugin-sdk-readme-md.md)
> Updated: 2026-10-24

## Overview

bb plugins are on by default. The configuration doc calls them "full-trust code running inside the bb server process". Each plugin gets its own SQLite database, a secrets directory and rotating logs under the bb data directory. Plugins can come from git or npm sources and from marketplaces. A session-sharing integration built as a bb plugin would therefore run with full server privileges. It can keep its own state, such as published-record mappings, in its per-plugin database.

## Plugin state and distribution

- State lives under `<dataDir>/plugins/<id>/`:
  - `data.db`: per-plugin SQLite
  - `secrets/`: secret settings and the plugin HTTP token
  - `logs/`: JSONL, rotated at 5MB, read with `bb plugin logs <id>`
- Managed installs for `git:` and `npm:` sources live under `<dataDir>/plugins/git/` and `npm/`.
- Marketplace catalogs are stored in the bb database. The reserved `bb-community` marketplace comes from `BB_MARKETPLACE_URL`, and a `git:` marketplace reads `marketplace.json`. The server checks installed plugins for updates every 6 hours but never applies them automatically.
- Settings change through Settings → Installed plugins, `bb plugin config <id> set <key> <value>`, or SDK `plugins.updateSettings`. Running plugins receive changes live.
- A repository can index several plugins through a strict `.bb/plugins.json` manifest. Its `schemaVersion` must be `1`, and invalid files are rejected whole.

## Plugin surfaces (Plugin Guide)

The getbb.app Plugin Guide indexes surfaces in seven groups: app window, command palette, composer, home page, plugin settings page, plugin page and plugin backend. The ones most relevant to session sharing are:

- **Backend**
  - lifecycle events when threads change state or environments are removed
  - a **dispatch hook** that runs a check before each message reaches an agent (a natural gate for remote participation)
  - HTTP / WebSocket / RPC / realtime messaging
  - background work on the server with no window open
  - plugin-private server storage
  - a private JSON metadata record per thread
  - agent tools, skills and instructions injected into every session
  - `bb` CLI commands
- **Providers and machines**
  - agent providers (selectable in the model picker)
  - **provider bridges** that run an agent's sessions through a bridge shipped to each machine
  - environment and machine providers
  - host workers on enrolled machines
- **UI**
  - thread header controls and thread menu actions (e.g. a "share" action)
  - timeline entry content and rich message embeds (rendering remote replies)
  - in-thread forms that ask the person a question and return the answer to the agent
  - side-panel tabs (e.g. a team activity feed)

## Bundled and builtin plugins of note

- **Official bundled plugins:** GitHub, Docs, Memory, Tasks.
- **BB guide:** injects an introduction and bundled skills into agent configuration.
- **Storage & retention:** disabled by default. Archive and delete policies run through the SDK thread APIs.
- **Connect / bb account:** remote access tunnel. See [bb Architecture and Data Model](bb-architecture.md).
- **ACP providers:** `customAgents` and the ACP registry.
- **MCP server:** disabled by default.

## Known extension-point gaps

- **Attribution:** messages a plugin sends into a thread are recorded as user-initiated, with no plugin identity (bb#3621, reported on 0.43.0, reproduced on 0.44.0). A sharing plugin that injects remote replies would inherit this until it is fixed. The current configuration doc says SDK sends carry `originPluginId` and telemetry distinguishes a `plugin` initiator; whether that resolves the stored attribution is disputed (see the Status block in the linked article). See [Message Provenance and Attribution](../security-privacy/message-provenance-and-attribution.md).
- **Cross-plugin provider hooks:** [bb Pi Provider Integration](bb-pi-provider-integration.md) documents a concrete gap. In BB 0.45.0 the plugin SDK had no additive API for one plugin to add native-command roots to another plugin's provider. The command-sync addon worked around this by patching the installed `provider-pi` bundle.

## See Also

- [bb Architecture and Data Model](bb-architecture.md)
- [bb Pi Provider Integration](bb-pi-provider-integration.md)
- [Pi Extensions](../pi/pi-extensions.md)

## Authoring contract and lifecycle obligations

The Skills Directory mirror of bb’s authoring guidance says installed SDK declarations and repository source define the contract for the installed bb version. It emphasizes boundary validation, server-side secret settings, bounded command/tool output and disposal of listeners and services. Experimental public APIs are marked separately from stable surfaces. Directory security grades are listing metadata, not a sandbox guarantee for a full-trust plugin.

## Release-specific dispatch and UI changes

The captured changelog describes saved drafts, browser annotations, provider handoffs and additional plugin UI and CLI surfaces. Dispatch-hook authors must account for queued messages and initiator/sender metadata rather than assuming a singular requester. Several surfaces are explicitly experimental. The changelog also describes server/plugin-state migration separately from provider sessions and workspaces, which stay on their execution machines; moving the server is not a session export.

## Hooks marketplace review and fail-open gates

The merged Hooks marketplace submission describes shell/webhook reactions and outgoing-message policy gates. Its security review says gates proceed on errors by default and have a limited dispatch budget; commands execute with the server user’s access. This makes Hooks an automation surface whose failure policy must be understood before treating it as an access-control boundary. A case-sensitive dependency bundling failure was reported and a dependency pin retested before approval, illustrating that marketplace admission is release-specific.

## Thread-list preferences as an extension example

The open thread-list date-grouping request shows the sidebar itself implemented as a plugin with synced preferences, CLI control and bundled skill documentation. It proposes grouping by local calendar day without changing underlying thread ownership or nesting. The prototype is an author’s branch awaiting sign-off, not a shipped preference. This is a concrete example of plugin-owned presentation state distinct from the event stream an exporter would consume.

## SDK facade and explicit UI targets

The Plugin SDK README identifies exported backend and app declarations as authoritative and the frontend facade as replaced by bb’s shared runtime during plugin build. Composer customization and file previews use host APIs; file targets name their workspace/host/thread scope instead of inferring an ambient workspace. Several panel and preview requests return whether the host accepted the request. A sharing UI should handle a declined navigation intent and validate targets rather than assume that a rendered control guarantees access.
