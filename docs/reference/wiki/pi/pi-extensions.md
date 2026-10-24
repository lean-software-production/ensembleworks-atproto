# Pi Extensions

> Sources: pi Extensions docs as mirrored at pi.ubitools.com (community mirror, newer snapshot) and hochej.github.io/pi-mono (older snapshot), both undated, collected 2026-10-23 (notes only; mirrors carry no license); source inventory: Extensions (source notes) (attributed source notes; Unknown); Extensions - pi (source notes) (attributed source notes; Unknown); Extensions 101 (source notes) (attributed source notes; Unknown); Pi Coding Agent (Mario Zechner and contributors, Pi coding agent documentation (pi.dev); Unknown); Pi Extension Development (source notes) (attributed source notes; Unknown); earendil-works/pi: packages/coding-agent/examples/sdk/06-extensions.ts (Copyright (c) 2025 Mario Zechner, earendil-works/pi; Unknown); Extension: The branchWithSummary method does not actually implement Tree Navigation (source notes) (attributed source notes; Unknown)
> Raw: [pi extensions docs, ubitools mirror (notes)](../../raw/pi/extensions-notes.md); [pi extensions docs, hochej mirror (notes)](../../raw/pi/extensions-pi-notes.md); [extensions-101-notes](../../raw/pi/extensions-101-notes.md); [pi-dev-docs-extensions](../../raw/pi/pi-dev-docs-extensions.md); [pi-extension-development-notes](../../raw/pi/pi-extension-development-notes.md); [earendil-works-pi-packages-coding-agent-examples-sdk-06](../../raw/pi/earendil-works-pi-packages-coding-agent-examples-sdk-06.md); [extension-the-branchwithsummary-method-does-not-actually-notes](../../raw/pi/extension-the-branchwithsummary-method-does-not-actually-notes.md)
> Updated: 2026-10-24

## Overview

Pi extensions are TypeScript modules that subscribe to lifecycle events, register tools the model can call, add commands, renderers and model providers, and persist state inside the session file. They run with full system permissions. Pi loads them automatically from a global directory and a project-local one, and project-local extensions load only after the project is trusted. For session sharing, an extension can observe every session lifecycle event and read the session tree through a read-only `sessionManager`. It can record its own bookkeeping in custom entries that stay out of model context, and it can inject steering or follow-up messages, which is a plausible path for remote participation.

## Loading and trust

- Auto-discovery: `~/.pi/agent/extensions/` (global) and `.pi/extensions/` (project-local). `pi -e ./path.ts` is for quick tests. `/reload` hot-reloads auto-discovered extensions.
- Security stance: extensions can execute arbitrary code, so the docs say to install only trusted sources.
- Project trust appears only in the newer snapshot. A `project_trust` event fires before pi decides whether to trust a project with dynamic configs. Handlers answer yes, no or undecided, and the first yes/no from a user, global or CLI extension wins. `ctx.isProjectTrusted()` reports the outcome.

## Session lifecycle events

- Newer snapshot: `session_start` carries reasons such as startup, new, resume, fork and reload. It sits alongside `session_before_switch`, `session_before_fork`, `session_before_compact` / `session_compact`, `session_before_tree` / `session_tree` and `session_shutdown`. Several "before" events can cancel or customise the action.
- Older snapshot: switch and fork had their own after-events (`session_switch`, `session_fork`). The newer text routes them through shutdown plus a fresh `session_start` with a reason.

> **Status: Outdated** (2026-10-23)
> The separate `session_switch`/`session_fork` events appear only in the older hochej.github.io mirror. The newer pi.ubitools.com mirror replaces them with `session_start` reasons (per the mirror notes). The upstream repo and pi.dev lifecycle sources linked below now corroborate the newer runtime lifecycle; older callback names remain snapshot-specific.

## State, messages and session access

- `pi.appendEntry` stores extension state in the session without entering model context. That is the `custom` entry type in [Pi Session File Format](pi-session-format.md). On reload, an extension rebuilds its state by scanning `ctx.sessionManager.getEntries()` for its own `customType`.
- Alternative: keep state in tool-result details so it branches with the tree, and rebuild it from `getBranch()`.
- `ctx.sessionManager` gives read-only access to `getEntries()`, `getBranch()` and `getLeafId()`.
- `pi.sendMessage` injects a custom message, delivered as steer (default), followUp or nextTurn, and can trigger a turn when idle.
- `pi.sendUserMessage` sends a message that appears as if typed by the user and always triggers a turn. Input events are labelled with a source: interactive, rpc or extension. Both messaging paths matter for provenance; see [Message Provenance and Attribution](../security-privacy/message-provenance-and-attribution.md).
- Other APIs: `pi.setSessionName`, `pi.setLabel`, `pi.registerMessageRenderer`, `pi.registerProvider` / `unregisterProvider`, `pi.exec` and the `pi.events` bus.

## Modes

Extensions run in every mode, with different UI capabilities. Interactive TUI mode has full UI. RPC mode (`--mode rpc`) exposes UI over a JSON protocol, and this is the mode bb uses; see [bb Pi Provider Integration](../bb/bb-pi-provider-integration.md). JSON mode (`--mode json`) streams events without UI. Print mode (`-p`) cannot prompt the user.

## Relevance to a sharing extension

The sources' own example use cases include permission gates, path protection, git checkpointing, custom compaction and webhook integrations. A sharing extension would:

1. hook session start and shutdown plus agent events to publish entries;
2. use `appendEntry` to remember what has been published;
3. potentially accept remote input through `sendMessage` or `sendUserMessage`.

Step 3 inherits pi's trust model (full permissions, no sandbox), so remote participation needs its own permission gate.

## See Also

- [Pi Session File Format](pi-session-format.md)
- [bb Plugin System](../bb/bb-plugins.md)
- [Message Provenance and Attribution](../security-privacy/message-provenance-and-attribution.md)

## Resource lifetime across session boundaries

The piagent Extensions guide recommends deferring long-lived sockets, watchers and processes until session start, then closing them on shutdown. An async factory can register startup capabilities, but a factory invocation need not imply an active session. This matters for publishers: start/stop hooks must not leak duplicate subscriptions across reloads. The guide also distinguishes tool registration from lifecycle handlers and confirms that extensions share process permissions.

## Upstream runtime and settle boundary

The pi.dev extension documentation confirms the same-process trust model and instructs authors to close session-scoped resources with idempotent shutdown handlers. Reload replaces the runtime; code resumed after reload must not reuse old state. A prompt can trigger multiple low-level agent runs through retries, recovery or queued work before the settled event. A publisher should therefore distinguish end of a low-level run from completion of the whole user request. Personal and explicit command-line extensions can participate in project trust before project extensions load.

## Older marketplace API snapshot

The LobeHub extension-development listing documents a default factory, tool registration, command handlers and state reconstruction from branch entries. It uses older mariozechner imports and older schema-library imports.

> **Status: Outdated** (2026-10-24)
> This marketplace snapshot is useful as a pattern catalog, but its import paths and callback signatures should be checked against the upstream extension document already linked here before use. It does not override the current runtime contract.

## Embedded SDK resource loading example

The upstream SDK example constructs a resource loader with additional extension paths and inline factories, reloads it, and supplies it to session creation. It uses an in-memory session manager and disposes the session in a finally block. Thus event subscriptions in an embedder need not imply a durable file exists; a collector must distinguish storage choice from the availability of extension hooks.

## Tree mutation must respect the context boundary

The closed branchWithSummary issue records a tree/context mismatch after an extension cast a read-only session manager to a writable one during a running tool. The maintainer attributes the mismatch to bypassing the API contract: the stored tree moved while the in-flight model buffer did not. Command-context navigation synchronizes both. This is evidence against mutating history through a cast, not evidence that normal tree navigation fails. Runtime hardening was requested separately.

## Related compiled concepts

- [Pi Architecture and Operations](pi-architecture-and-operations.md)
