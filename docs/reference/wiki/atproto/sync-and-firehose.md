# ATProto Sync and Firehose

> Sources: atproto.com Data Synchronization spec (Bluesky Social PBC and Contributors, CC-BY), undated, collected 2026-10-23; source inventory: Sync - AT Protocol (Bluesky Social PBC and Contributors, AT Protocol website; Unknown)
> Raw: [atproto Sync spec](../../raw/atproto/sync-at-protocol.md)
> Updated: 2026-10-23

## Overview

Public atproto data spreads in two ways. One is **batch export**: the unauthenticated `com.atproto.sync.getRepo` returns a whole repo as a CAR file. The other is a real-time **repository event stream**, the "firehose" (`com.atproto.sync.subscribeRepos` over WebSocket with CBOR). PDSes stream their own accounts, and relays aggregate many PDSes into one stream. Repo data on the firehose is self-certifying. Identity and account events are not, so consumers must resolve DIDs and handles themselves.

For a team activity feed, an AppView can consume the firehose filtered to the session Lexicon's collections, using the record-level sync pattern below. This covers *public* sessions only. Private sessions in spaces have no relay or firehose and are synced per space instead (see [ATProto Spaces (Permissioned Data)](atproto-spaces-permissioned-data.md)), although space apps still need the public firehose's `#account` and `#identity` events.

## Event types

- **`#commit`**: a new commit. Fields:
  - `repo` and `rev`, plus `since` (the preceding rev).
  - `blocks`: a CAR slice holding the diff.
  - `ops`: record-level creates, updates and deletes.
  - `prevData`: the previous MST root, effectively required for inversion.
  - `tooBig` and `blobs`: deprecated, but still technically required.
- **`#sync`**: asserts or resets the repo's current state. It carries the commit block only, so consumers must refetch the full CAR.
- **`#identity`** and **`#account`**: DID/handle changes and hosting status.

## Reliable synchronization

- Revisions are TIDs used as a per-repo logical clock. They must always increase, even across migrations. Updates with future timestamps should be ignored. Services can report sync status with the `Atproto-Repo-Rev` response header.
- Consumers verify each `#commit` against the previous state using **operation inversion**: apply the ops in reverse to the partial tree in the diff and check that the result matches the prior `data` root. Only the rev and root per repo need to be stored. If `since`/`prevData` do not match, or after a `#sync`, the repo is re-synchronized from its full CAR. Fetch it from the direct upstream (often a relay) first, to avoid a thundering herd on the PDS.
- **Record-level sync pattern** for indexers:
  - Track per-repo status (`desynchronized`, `in-progress`, `synchronized`) and a sorted table of (DID, path, CID).
  - Drop events for desynchronized repos and queue events for in-progress ones.
  - Resync workers walk the CAR and diff it against the table.
  - Validate *every* commit for in-scope accounts, even ones with no in-scope records, to keep the chain intact.
  - Backfill previously active accounts with `com.atproto.sync.listReposByCollection`.
- Process events in order per account and concurrently across accounts. Persist the cursor (sequence number) so the stream can resume.

## Mirrors and deletion

The spec says mirrors of repo CARs must honour deletions and account status changes within seconds or minutes. It also says static repo snapshots generally should not be redistributed in bulk, such as archives or torrents. This is the protocol's own position on erasure for public data. A shared-session archive service would need to follow it. See [Personal Data Erasure on Replicated Networks](../security-privacy/secret-leakage-in-shared-sessions.md).

## See Also

- [ATProto Repository, Records and Lexicon](repository-and-records.md)
- [ATProto Spaces (Permissioned Data)](atproto-spaces-permissioned-data.md)
- [ATProto Blobs and Size Limits](blobs-and-size-limits.md)
