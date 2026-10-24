# ATProto Repository, Records and Lexicon

> Sources: atproto.com Repository spec and Lexicon spec (Bluesky Social PBC and Contributors, CC-BY), undated; atproto.com "Data Validation" guide (notes only); all collected 2026-10-23; source inventory: Repository - AT Protocol (Bluesky Social PBC and Contributors, AT Protocol website; Unknown); Lexicon - AT Protocol (Bluesky Social PBC and Contributors, AT Protocol website; Unknown); Data Validation - AT Protocol (source notes) (attributed source notes; Unknown); Bluesky and the AT Protocol: Usable Decentralized Social Media (Martin Kleppmann, Paul Frazee, Jake Gold, Jay Graber, Daniel Holmgren, Devin Ivy, Jeromy Johnson, Bryan Newbold, Jaz Volpert; arXiv:2402.03239v2; 2024-02-05)
> Raw: [atproto Repository spec](../../raw/atproto/repository-at-protocol.md); [atproto Lexicon spec](../../raw/atproto/lexicon-at-protocol.md); [atproto Data Validation guide (notes)](../../raw/atproto/data-validation-at-protocol-notes.md); [2024-02-05-bluesky-and-the-at-protocol-usable-decentralized-social](../../raw/collaboration-research/2024-02-05-bluesky-and-the-at-protocol-usable-decentralized-social.md)
> Updated: 2026-10-24

## Overview

Each account's public data lives in one signed, content-addressed **repository**. It is a Merkle Search Tree that maps `<collection>/<record-key>` paths to CBOR records. Each mutation produces a new signed commit, and the repo exports as a CAR file. Record schemas, API endpoints and event streams are defined in **Lexicon**. Lexicon is a JSON-Schema-like language in which every NSID is controlled through DNS, published as a `com.atproto.lexicon.schema` record, and bound by strict evolution rules.

These constraints shape how a coding-agent session maps onto records:
- Paths have exactly two segments.
- TID record keys sort chronologically.
- Records have practical size ceilings.
- Once a Lexicon is published, its field types and limits are effectively frozen.
- Deletion leaves no tombstone.

Public repo data is public. Private sessions belong in [ATProto Spaces (Permissioned Data)](atproto-spaces-permissioned-data.md), which reuse records and Lexicons but use a different repo format.

## Repository structure (spec, format version 3)

- Repo contents are public and self-certifying. Record deletion is supported without leaving a trace or tombstone of previous contents.
- Paths are a valid NSID, then `/`, then a valid record key. A path has exactly two segments, uses a restricted ASCII set and is never empty. Records in the same collection sort together, and the TID key scheme was chosen so keys sort chronologically, which makes appends cheap. A session's entries written with TID keys therefore enumerate in time order.
- The spec says repositories are intended to store up to single-digit millions of records. Beyond that they become unwieldy to distribute and process.
- Commit fields are `did`, `version` (`3`), `data` (MST root CID), `rev` (TID logical clock, must increase monotonically), `prev` (virtually always `null`) and `sig`. Commits are signed with the account's current signing key, which is published in the DID document.
- Diffs are "CAR slices" containing all blocks changed since a revision. The firehose validates them by operation inversion; see [ATProto Sync and Firehose](sync-and-firehose.md).
- Security: repositories are untrusted input. Implementations should apply CBOR size, depth and memory limits, guard against mined record keys that produce pathological trees, and verify CAR imports.
- Possible future change: an optional in-repo mechanism for storing multiple versions of the same record.

## Practical limits (Data Validation guide; informal, not spec)

The guide states its limits are informal guidelines that may evolve.

| Limit | Value |
|---|---|
| `MAX_CBOR_RECORD_SIZE` | 1 MiByte (1,048,576 bytes). Keep typical records to a few dozen KBytes and use blobs for more. |
| `subscribeRepos` `#commit` block size | 2,000,000 bytes as of August 2025, so only one 1 MiByte record fits per commit |
| `MAX_JSON_RECORD_SIZE` | 2 MiByte (2,097,152 bytes) |
| `MAX_CBOR_NESTED_LEVELS` | 32 |
| `MAX_CBOR_CONTAINER_LEN` | 131,072 elements |
| Integers | 53-bit float-safe (`MAX_SAFE_INTEGER: 9007199254740991`) |

Consumers should ignore an individual invalid record and keep processing the rest of the repo. A broken commit or MST marks the repository invalid until a later valid commit.

## Lexicon essentials

- Primary types are `query` (HTTP GET), `procedure` (HTTP POST), `subscription` (WebSocket), `record` and `permission-set`. A record definition declares its `key` type, for example TID.
- `record` objects and union variants must carry `$type`.
- **Validation modes on write:** explicit validation, explicit no-validation, or optimistic validation. Optimistic is the default and "Fail-Open": if the PDS does not know the Lexicon, the record is still accepted. An unknown session Lexicon can therefore be accepted in optimistic validation mode, subject to the PDS’s other policies. It also means the PDS cannot be relied on to validate it.
- **Evolution rules:**
  - new fields must be optional;
  - required fields cannot be removed, renamed or retyped;
  - closed unions cannot change;
  - size and length limits cannot be added, removed or changed.
  - Breaking changes need a new NSID. The spec recommends flagging experimental status in the name, as in `com.corp.experimental.newRecord`.
- Unexpected fields should be ignored, which allows schema evolution. Data that fails validation should be treated as entirely invalid.
- **Publication and authority:**
  - Schemas are records of type `com.atproto.lexicon.schema`, with the NSID as record key.
  - Authority is linked by a `_lexicon` DNS TXT record per authority group, for example `app.toy.record` resolves via `_lexicon.toy.app`.
  - Resolution is not hierarchical.
  - DNS changes are not broadcast on the firehose, so resolvers should not cache them for long.

## Design implications for session records

- Model a session as a parent record plus one record per entry under TID keys, or batch entries per record. In both cases the 1 MiByte record ceiling and the one-big-record-per-commit firehose ceiling apply. Long tool outputs and attachments belong in blobs; see [ATProto Blobs and Size Limits](blobs-and-size-limits.md).
- Pi's session tree uses short entry ids and `parentId` links ([Pi Session File Format](../pi/pi-session-format.md)). Keep those as fields, and derive record keys deterministically so that re-publishing is idempotent.
- Use an explicitly experimental NSID until the schema settles, because published Lexicons cannot change limits or types.
- Unpublishing removes records with no tombstone. Copies already synced by others are a separate problem; see [Personal Data Erasure on Replicated Networks](../security-privacy/secret-leakage-in-shared-sessions.md).

## See Also

- [ATProto Sync and Firehose](sync-and-firehose.md)
- [ATProto Blobs and Size Limits](blobs-and-size-limits.md)
- [ATProto OAuth and Permissions](oauth-and-permissions.md)
- [Agent Session and Trace Formats](../agent-sessions/agent-session-trace-formats.md)

## Architecture goals versus private collaboration

Kleppmann and coauthors frame AT Protocol as infrastructure for public social media, combining interoperable service roles, provider switching, user-controlled views and approachable user experience. This architectural rationale supports separating durable identity and repository records from application indexing. It does not by itself establish private-session storage or multi-user execution authorization; those require the separate permissioned-data and application-level mechanisms.
