# bb-lite: Smaller, Multiplayer bb Rewrite

> Sources: get-bb/bb-lite contributors / Terragon Labs, README (MIT), undated; collected 2026-10-23, README rechecked unchanged 2026-10-24
> Raw: [get-bb/bb-lite README and repository snapshot](../../raw/bb/get-bb-bb-lite.md)
> Updated: 2026-10-24

## Overview

**bb-lite is a smaller rewrite of bb that adds multiplayer: several people share one server.** It retains live coding-agent threads, steering, queued messages and agent-managed child threads. This is a separate product, not evidence that the original get-bb/bb server supports multiple users. The following describes the repository's README claims, not an independently tested deployment.

## Smaller codebase and runtime

The README reports about **263,000 counted lines**, including **42,000** test lines, versus about **1.6 million** in get-bb/bb under the same counting rule (`pnpm count`). These are source-reported code counts, not runtime memory or speed measurements. The earlier bb-150k experiment's **150,000**-line cap was lifted to restore features as plugins.

The rewrite has a web app, Node and optional native Rust CLI, server and relay, but no desktop or native mobile app. The local runner lives inside the server process; other machines connect through `bb runner`, rather than the original's separate host-daemon architecture.

A small kernel supplies contracts, operations, hooks, slots and live values. Product features—including threads, identity and UI screens—are plugins using the same API as external plugins. Operations expose HTTP, CLI and agent-tool interfaces. Codex and Claude Code are supported, with Pi and ACP providers as add-ons. This differs from the original bb plugin SDK; compatibility should not be assumed.

## Multiplayer model and limits

- **People and roles:** owners invite members and administer users, plugins and server settings; members work in threads.
- **Shared awareness:** presence shows who is online and who has a thread open. Read/unread state, pins, tabs, prompt history and preferences are per person.
- **Attribution:** threads record their creator and messages their sender. Agent `bb` calls act as the person who last wrote in the thread; the audit log records actions.
- **Machine permissions:** machines have an owner and can be private or shared. Private machines restrict who can run threads, terminals and file commands there.
- **No private threads:** everyone can read every thread. Private execution machines do **not** imply private conversations.
- **Authentication boundary:** loopback requests on the server machine are treated as the owner without sign-in. Other access uses session cookies or the relay's GitHub sign-in mapped to server users.

## Relevance to session sharing

**Design inference:** bb-lite is a closer starting point for shared agent work than adapting the original bb's single-user model: it already documents people, message attribution, presence and machine ownership. It does not provide selective thread confidentiality or establish ATProto identity, publication or synchronization. An integration still needs explicit disclosure rules and must distinguish a message's author from the person whose authority an agent uses.

## See Also

- [bb Architecture and Data Model](bb-architecture.md)
- [bb Plugin System](bb-plugins.md)
- [Message Provenance and Attribution](../security-privacy/message-provenance-and-attribution.md)
- [Secret and Context Leakage in Shared Sessions](../security-privacy/secret-leakage-in-shared-sessions.md)
