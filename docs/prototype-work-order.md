# Overnight prototype work order

Authorized by Matt on 2026-11-17. The manager coordinates implementation, integration, independent review and acceptance. Deliver a running Docker Compose spike using Bluesky's published TypeScript PDS, a CLI watching Claude JSONL logs, and a web feed displaying records fetched from that PDS.

## Acceptance

- A documented command boots the real PDS and feed; bootstrap creates local pilot accounts and a company Space where supported by the pinned reference implementation.
- A CLI watches a specified directory recursively, imports existing JSONL, and publishes newly completed entries. No silent event-type filtering: preserve all native payloads, including unknown types, tool calls/results, prompts and titles.
- A feed displays sessions, names and prompts, and allows inspecting the full native event timeline. It refreshes after a log append without reloading the service.
- Restart and repeated scans do not duplicate events. Partial final lines, malformed lines, nested subagent logs, source rewrites, and temporary PDS failure have explicit tested behavior.
- All writes/readbacks use the real PDS. Test fixtures demonstrate the complete watcher-to-PDS-to-feed path; verify persistence after restart.
- Existing privacy direction remains: company members, per-person authorship, one tenant. Investigate current Spaces implementation first; do not silently substitute public repository writes or a mock PDS. Escalate an actual compatibility blocker to manager with concrete alternatives.
- Leave a reproducible runbook, version pins, test/review evidence and a running demo with synthetic sessions. Never point the demo watcher at personal session stores by default.

## Ownership and integration

Infrastructure thread owns root package/workspace configuration, Compose, Dockerfiles, bootstrap, packages/transport, and infra documentation. Watcher thread owns packages/cli, packages/protocol, Claude fixtures and watcher tests. Feed thread owns packages/feed and browser tests. Coordinate API changes by messaging peers and manager. Shared checkout: do not overwrite another owner's files or revert existing research.

Use TypeScript on Node, npm workspaces and minimal dependencies. Infrastructure owns root dependencies and lockfile. Each owner may write its own package manifest; ask infrastructure to install workspace dependencies. Initial transport seam: createTransport(config) exposes putEvent(rkey, record) and listEvents({cursor, limit}); listing returns {records:[{uri,cid,value}],cursor?}. Infrastructure must refine this for Space/member reads and announce exact contract promptly. Protocol owner defines the event record and announces its exports promptly. Preserve original JSON via an explicitly encoded payload string if the source's values do not map losslessly to Lexicon values; support oversized payloads or fail visibly with retryable state, never silently truncate.

The user changed the earlier explicit-share-only scope: continuous filesystem watching is now required. Modeling all events is required; adapters beyond Claude are not necessary for this spike. The first feed's previous start/name-only display is expanded enough to inspect the complete imported stream.

## Review gate

After component delivery, assign a separate review and validation thread. It must inspect code, run the actual stack, check data flow and failure/restart behavior, and report defects with evidence. Implementers fix material defects; reviewer verifies fixes. The manager reports actual working endpoints and commands, checks passed, and remaining limits. No merge, public deployment or external publication is requested.

## Manager acceptance — 2026-11-17

Accepted as the requested local spike after reviewing [independent acceptance](prototype-review.md), component evidence and the final browser screenshot. Actual CLI watching, per-person private Space writes, feed polling, exact native payload readback, large-event chunks, crash recovery, PDS outage recovery and Compose persistence passed. The demo stack is left running. Root README and the infrastructure/watcher runbooks provide startup and demo commands.

The accepted bounds are Claude JSONL ingestion, one local PDS/company Space, shared feed login, 16 MiB native/20 MiB serialized limits, and source identity ambiguities documented in the watcher runbook. No claim is made for recovering runtime-only events or attachment bytes. Fresh empty-volume replay and remote BB Connect login were not independently tested. Remaining limits and dependency advisories are recorded in the runbooks and review report.

Feed: http://localhost:3100, also exposed through existing authenticated BB Connect at https://ew-lsp-001--3100.getbb.app. Local login password remains in ignored .local/feed.env; credentials are not included in handoff text. No merge or public deployment occurred.
