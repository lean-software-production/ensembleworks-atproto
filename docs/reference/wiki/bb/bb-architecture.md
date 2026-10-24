# bb Architecture and Data Model

> Sources: get-bb/bb `docs/system-overview.md` and `docs/configuration.md` (Michael Yong / bb contributors, MIT), undated; Flavio Copes, "How bb, the programmable IDE for coding agents, is built" (page marked updated Oct 21, 2026; notes only); getbb.app landing page (Terragon Labs, notes only); all collected 2026-10-23; source inventory: get-bb/bb: docs/system-overview.md (Copyright (c) 2026 Michael Yong, get-bb/bb; Unknown); get-bb/bb: docs/configuration.md (Copyright (c) 2026 Michael Yong, get-bb/bb; Unknown); How bb, the programmable IDE for coding agents, is built (source notes) (attributed source notes; Unknown); bb (source notes) (attributed source notes; Unknown); get-bb/bb#4214: Let one bb server be shared by a team (multiple users, per-user threads and machines) (source notes) (attributed source notes; Unknown); get-bb/bb#5552: Public request-aware handoff ownership for safe provider fallback (source notes) (attributed source notes; Unknown); get-bb/bb-lite (get-bb/bb-lite contributors (see LICENSE); Unknown); get-bb/bb: packages/bb-app/README.md (get-bb/bb contributors; Unknown); get-bb/bb#1573: Make threads.stop release idle agent runtimes and document hidden worker cleanup (source notes) (attributed source notes; Unknown)
> Raw: [bb system-overview.md](../../raw/bb/get-bb-bb-docs-system-overview-md.md); [bb configuration.md](../../raw/bb/get-bb-bb-docs-configuration-md.md); [Flavio Copes on bb internals (notes)](../../raw/bb/how-bb-the-programmable-ide-for-coding-agents-is-built-notes.md); [getbb.app landing page (notes)](../../raw/bb/bb-notes.md); [get-bb-bb-4214-let-one-bb-server-be-shared-by-a-team-notes](../../raw/bb/get-bb-bb-4214-let-one-bb-server-be-shared-by-a-team-notes.md); [get-bb-bb-5552-public-request-aware-handoff-ownership-for-notes](../../raw/bb/get-bb-bb-5552-public-request-aware-handoff-ownership-for-notes.md); [get-bb-bb-lite](../../raw/bb/get-bb-bb-lite.md); [get-bb-bb-packages-bb-app-readme-md](../../raw/bb/get-bb-bb-packages-bb-app-readme-md.md); [get-bb-bb-1573-make-threads-stop-release-idle-agent-notes](../../raw/bb/get-bb-bb-1573-make-threads-stop-release-idle-agent-notes.md)
> Updated: 2026-10-24

## Overview

bb is an "agentic IDE" built from four runtime pieces: a central **server**, a **host daemon** on each execution machine, a web **app**, and the `bb` **CLI** with an SDK. The server keeps all state in one SQLite database and streams change notifications over WebSocket. Work happens in **threads**. Each thread produces an append-only, server-sequenced stream of provider-neutral events. Agent output from Codex, Claude Code, Pi and ACP agents is normalised into that one stream by adapters, which makes bb's thread events the natural export point for sharing sessions. Thread events live in the server database, not in per-session files, so external sync goes through bb's API, SDK or plugins. The exception is pi's own bridge session files; see [bb Pi Provider Integration](bb-pi-provider-integration.md). Licensing and project status are covered in [bb Project Status, Licensing and Contribution](bb-project-status.md).

## Runtime pieces

- **Server**: the central hub. It keeps state in SQLite, exposes an HTTP API and pushes change notifications over WebSocket. It describes itself as stateless, with the DB as the source of truth. It routes work to hosts over the daemon WebSocket.
- **Host daemon**: runs on each enrolled machine. It handles host RPC, provisions workspaces, runs agent provider processes and posts events back. It also exposes a local HTTP API for co-located app/CLI operations.
- **App**: web UI for inspecting projects and threads and for steering work.
- **CLI (`bb`)**: described as a first-class interface for users *and agents*, with the same capabilities as the app. The landing page stresses that any program can drive the same CLI, from scripts and cron to chat bots, for example with `bb spawn`.

Two contract packages fence the boundaries. `@bb/server-contract` covers client↔server HTTP and WebSocket. `@bb/host-daemon-contract` covers server↔daemon commands, events and session lifecycle. Implementation packages never import across them.

## Data model

- **Project**: the top-level container, usually one repository. It has one or more sources, and local-path sources are tied to a specific host.
- **Thread**: the unit of work. It holds a conversation with an agent provider, lifecycle state and an append-only event stream (messages, tool calls, file changes). A thread is *standard* or *manager*, and threads can own child threads for delegation. According to Copes, manager threads are ordinary threads given the bb CLI through a built-in skill (`bb thread wait`, `bb thread output`).
- **Environment**: binds a workspace directory to a host. It is either managed (cleaned up once no unarchived thread uses it, and possibly an isolated Git worktree) or unmanaged. Copes lists its lifecycle as provisioning, ready, retiring, destroying, destroyed.
- **Host**: a long-lived daemon identity. The server runs on one host (`primaryHostId`) and can enroll more.

Lifecycle rules matter for anything that mirrors threads externally:
- `lifecycleOwnerThreadId` is set once and is independent of sidebar parent, fork source and visibility.
- Archiving an owner archives its dependents.
- Deletion recurses through children and lifecycle dependents.
- An archived thread keeps running for an undo grace period (`ARCHIVE_UNDO_GRACE_MS`).

## Event pipeline (per Copes' source reading)

1. `bb thread spawn` creates a thread row, commonly with status `starting`, before any agent process exists.
2. The server sends `thread.start` to the daemon over WebSocket-as-RPC. Command results are separate from thread events.
3. The daemon hands the thread to `@bb/agent-runtime`. It has adapters for Codex (app-server protocol), Claude Code, Pi and ACP agents, and they convert provider output into shared thread events such as `turn/started` and `turn/completed`.
4. The daemon batches ordinary events for up to 100 milliseconds and flushes important ones (approvals, completed turns, interruptions) immediately. **The queue is in memory, so events are lost if the daemon crashes before delivery.**
5. The server checks that the thread belongs to the posting daemon's host. It writes events in one SQLite transaction with a monotonically increasing per-thread sequence number. Clients can request everything after a given sequence, which suits an incremental exporter.
6. Thread state (idle, starting, active, stopping, error) is driven by events such as `run.started` and `stop.settled`, using compare-and-swap writers. Stale events become recorded no-ops.

Copes adds a caveat: normalising events does not make providers identical. Resume, approvals, models and tool semantics still differ.

## Configuration, machines and trust

- Packaged settings live in `~/.bb/config.json`. Provider credentials live in `~/.bb/env.json` (redacted by `bb-app env list`), and SSH targets in `~/.bb/client.json`. Each agent uses the user's own provider subscription.
- **Multi-machine**: each machine has a `maxPermissionMode` ceiling (default `full`), and every thread on that machine is resolved down to it. Only an owner session can set the ceiling; it is deliberately absent from the SDK and CLI. Daemons auto-update from the owning server, retrying "from 5 seconds to 5 minutes".
- **Remote access**: a signed-in server is reachable at `https://<handle>.getbb.app` via the builtin connect plugin, and `bb plugin disable connect` cuts off all remote access. Copes reports that bb's docs warn that binding the server to a public interface exposes an unauthenticated command and file-reading API.
- **Custom ACP agents**: added as `customAgents` entries with provider id `acp-<id>`. A custom agent's command is local code execution and works only with a co-located daemon. See [Agent Client Protocol (ACP)](../agent-protocols/agent-client-protocol.md).
- **MCP server plugin** (disabled by default): an approved remote app can run *any* `bb` command. Loopback access needs no sign-in.

Remote participation in a bb thread would pass through these same trust surfaces. The machine permission ceiling is an existing bb-side control a sharing integration can rely on. The loopback API's lack of credentials is a known weakness; see [Message Provenance and Attribution](../security-privacy/message-provenance-and-attribution.md).

## See Also

- [bb Plugin System](bb-plugins.md)
- [bb Pi Provider Integration](bb-pi-provider-integration.md)
- [bb Project Status, Licensing and Contribution](bb-project-status.md)
- [Pi Session File Format](../pi/pi-session-format.md)

## Multi-user sharing is a requested boundary

The open team-server request argues, from a source reading rather than a live multi-person test, that one server identity and visible/hidden threads do not supply per-person ownership. It requests teammate machine enrollment, owner attribution and separate read/steer permissions while keeping credentials and limits local to people or machines. Its workaround copies evidence into an external store. Treat this as an architectural gap reported by the requester, not an implemented multi-user contract.

## Durable ownership across provider fallback

The request-aware handoff issue proposes transactional transfer of an unaccepted input when provider capacity is exhausted. It separates accepted side effects, retained as history, from the exact failed input to admit once on a destination. Durable source/request identity should exclude retries after transfer and reconcile repeated or restarted operations to one destination. These are proposed public contracts and locally reported prototype results, not upstream guarantees; memory-only handoff locks do not supply durable ownership.

## bb-lite is a separate multiplayer rewrite

The bb-lite README describes a smaller rewrite with shared-server multiplayer and Pi/ACP as add-ons. Its projects, threads, environments and execution machines resemble bb’s vocabulary, but the product and architecture are distinct. See [bb-lite: Smaller, Multiplayer bb Rewrite](bb-lite.md) for the source-reported code-size comparison, owner/member roles, presence and attribution. Its private machines restrict execution, not thread reading: everyone on the server can read every thread.

> **Status: Disputed**
> The open team-server request concerns get-bb/bb, whereas bb-lite explicitly claims multiplayer. This is a product-scope difference: bb-lite’s capability must not be silently attributed to the original bb server, nor should the original server’s reported limitations be used to deny bb-lite’s documented design.

## Launcher and runtime ownership

The bb-app README describes a launcher that starts the server and local host daemon and restarts a managed child independently if it fails. A healthy existing instance owning the same data directory prevents another launcher from starting duplicate children. It distinguishes stable and nightly distribution channels and notes native add-on installation requirements. Runtime ownership, published package channel and provider-session state are separate concerns when designing a collector.

## Stop and archive have separate purposes

The completed hidden-worker cleanup issue proposes extending stop to release idle as well as active runtimes while preserving thread history and future resume. Archive remains an organizational/retention action. The issue’s completed state is evidence of recorded resolution status, but its body is acceptance criteria rather than a code-level verification of every runtime state. A publisher should distinguish stopping execution from deleting or archiving evidence.
