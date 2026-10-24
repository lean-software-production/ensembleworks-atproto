# bluesky-social/proposals: 0016-permissioned-data (Atproto Spaces) (source notes)

> Source: https://github.com/bluesky-social/proposals/tree/main/0016-permissioned-data
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-02 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — bluesky-social/proposals: GitHub API license endpoint 404, no license found. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-166b4b35/001.md.
> Work: bluesky-social/proposals:0016-permissioned-data
> Quotations: 37 characters verbatim in this file; 37 of 90 allowed for this work across the knowledge base.

## About this source

The README of proposal 0016 ("Atproto Spaces") in the bluesky-social/proposals repository, directory `0016-permissioned-data`; the directory contains only that README (74628 bytes). It is explicitly a proposal and not a final specification: the document states that details, terminology and behaviours are likely to change. It points to the community forum for discussion, to the "permissioned data diary" blog posts, and to an implementation branch (PR 5187 in the atproto repo) holding draft lexicons, noting the implementation is still a work in progress. No license was found for the proposals repository, so this is a notes digest only.

## Key facts: purpose and model

- Spaces are an additional protocol for permissioned data (data with an access perimeter), next to the existing public broadcast repo/sync protocol. Modalities listed: personal data (bookmarks, mutes, drafts), gated content (paid newsletters, subscriber-only posts), socially shared (private posts, stories), groups (private forums, communities, group chats).
- Spaces keep DID-based authority, per-user repositories, lexicon-typed records and the crawl-PDS-to-build-views flow, but have their own repo format, sync mechanism, addressing scheme and resolution path.
- Safety statement: spaces give access control, not confidentiality. They are not end-to-end encrypted; PDSes and authorised applications can read the data they handle, needed for search, indexing, notifications, aggregation and moderation. E2EE is out of scope and may be layered on by an application.
- Comparison table with public broadcast: one space repo per (user, space) instead of one repo per user; URI authority is the space authority DID; commit is an LtHash set-hash digest rather than a Merkle Search Tree root; commit authenticity is an HMAC rather than a signature; addressing uses an `at://` URI with a `space` segment; access is gated by a space credential.
- Terminology: space (authorization and sync boundary identified by an `(authority, type, skey)` triple), space repo, repo host, space host, space authority, space credential, delegation token, client attestation, syncer. A PDS fulfils both repo host and space host roles but the roles may be filled by other services implementing the required APIs.

## Key facts: identifiers and types

- Record URI format: `at://{spaceDid}/space/{spaceType}/{skey}/{authorDid}/{collection}/{rkey}`; a space alone is the prefix through `skey`. A new `space-ref` Lexicon string format references just a space. The fixed `space` marker contains no dots, so it never collides with a public collection NSID.
- Space authority: a DID, either a user's own DID (personal data) or a dedicated DID so a shared space can transfer between users. Its `#atproto_pds` service endpoint is the space host and its `#atproto` key signs credentials.
- Space type: an NSID naming the modality; also the OAuth consent boundary. It resolves to a space type declaration, a Lexicon definition with `"type": "space"`, with fields `type`, `description`, `key`, `name`, `name:lang` and `collections` (required: `type`, `key`, `name`, `collections`). `collections` gives the default collection set for `space:` permissions, may not contain a wildcard, and any space may hold records of any collection. Declarations can be updated, and default-collection changes apply to existing OAuth sessions.
- Space key `skey`: maximum length 512 bytes, same syntax requirements as an `rkey`.

## Key facts: access control and credentials

- Access rests on two signed assertions: which user (a delegation token minted by the user's PDS) and which application (a client attestation signed by the app). An authority may require either, both or neither, and must not reject a request solely for including a valid assertion that the space does not require. Spaces requiring neither offer public access, though syncers still need a credential.
- Delegation token: minted via `com.atproto.space.getDelegationToken`, single-use, short-lived (default 60 seconds), addressed to the space authority; JWT header `typ` is `atproto-space-delegation+jwt`, no `lxm` claim, bound to the space through `sub`. Requires a `read` grant from a `space:` scope.
- Client attestation: short-lived single-use JWT, shape of a `private_key_jwt` client assertion, `typ` `atproto-client-attestation+jwt`, with `iss` and `sub` both the client_id; the authority verifies it against the JWKS in the client's client-metadata.json.
- Space credential: obtained via `com.atproto.space.getSpaceCredential` with body fields `space`, `credentialKid`, optional `delegationToken` and `clientAttestation`. JWT `typ` is `atproto-space-credential+jwt`, signed by the space authority, no `aud`, carries `cnf.kid`. Default life 10 minutes, maximum 60 minutes. Multi-use across all repo hosts for the space.
- Key binding: credential is bound to a P-256 `did:key` supplied by the app (RFC 7800 `cnf.kid`), and each request carries an HTTP Message Signature (RFC 9421, `ecdsa-p256-sha256`, 64-octet `r || s`) over the `Authorization` and `Atproto-Space-Audience` headers, so one repo host cannot replay the bearer credential elsewhere. The app should generate a new keypair per credential. Presentation scheme: `Authorization: Atproto-Space-Credential` plus a signature with tag `atproto-space-credential`; verifiers must accept both low-S and high-S signatures. Replay against the same audience is allowed until expiry.
- Revocation: short expiry is the main mechanism; optionally the authority sends `com.atproto.space.notifyCredentialRevoked` identifying credentials by `jti`; a repo host must retain a revocation for at least 60 minutes.
- An app serving several users may obtain a credential using any one user's session; if a delegation token is required and all OAuth sessions are lost, it can no longer renew and loses access.

## Key facts: space repos and sync

- A space repo is one account's records in one space, auto-created on first write; an empty and a nonexistent repo are equivalent; deleting all records deletes the repo, not the space. Records are CBOR key/value by collection NSID and rkey.
- Commit (`com.atproto.space.defs#commit`) fields: `ver` (currently 1), `repo`, `space`, `rev` (TID) and `data` (sha256 of the LtHash state, 32 bytes).
- Digest: LtHash set hash; state is a fixed 2048-byte buffer of 1024 little-endian 16-bit lanes; each record maps to the element `{collection}/{rkey}/{record_cid}`, expanded with BLAKE3 XOF; add or remove by lane addition or subtraction modulo 65536. Order-independent.
- Authenticity uses MACs, not signatures, deliberately so that leaked permissioned data carries no transferable proof of authorship. Each account publishes a P-256 `#atproto_kem` key in its DID document (a `Multikey`); the syncer does ECDH with a fresh ephemeral keypair per request, derives a 32-byte shared secret by HKDF-SHA256 following RFC 9180, sends `Atproto-Space-Want-Mac`, receives `Atproto-Space-Mac`. Commit MAC covers `space`, `repo`, `rev`, `data` using HMAC-SHA256; record MAC covers URI and CID. ECDH is not post-quantum; the KEM framing allows ML-KEM later.
- Serialisation: `getRepo` returns a STAR-lite v1 archive (profile `atproto-space-repo`), magic bytes `0x2A 0x6C 0x01 0x00`, metadata a DRISL map, records sorted strictly lexicographically by key, each value at most 1 MiB (1,048,576 bytes). Blobs are excluded and fetched with `getBlob`.
- Sync: no relays or collated firehose. The syncer calls `com.atproto.space.listRepoOps` with `since`; each entry carries `rev`, `collection`, `rkey`, `cid` and `prev`; values inlined by default, `excludeValues` for metadata only. Syncer keeps its own running set hash and compares with the commit `data`. The oplog is only a transport optimisation, may be compacted and resets on migration; fallback is full-state recovery via `getRepo`, or healing via `getLatestCommit`, `listRecords` and `getRecord`.
- Write notifications: PDS sends `notifyWrite` (rev and data, no record data) to the space host; syncers subscribe with `registerNotify` (fixed-duration registrations) and fetch data directly from the repo host. Space host sequences its own space revision; gaps are detected and `listRepos` lists repos updated since a space revision. The space host never hosts record data. The writer set from `listRepos` lists accounts that have written at least one record, not readers, and is the authority's claim rather than authoritative.
- Deletion: the authority stops issuing credentials, deletes its own records, notifies syncers with `notifySpaceDeleted`; syncers should delete every copy and derived state; a deleted space yields an explicit `SpaceDeleted` error on credential renewal. Members' repo hosts are not notified; member records remain the member's data but become unreadable to others. A space may be recreated with the same type and `skey`.

## Key facts: OAuth scopes and permission sets

- Scope syntax: `space:<spaceType>[?authority=<did>][&skey=<skey>][&collection=<nsid>...][&action=<action>...][&manage=<op>...]`. Defaults: `authority` is `self`, `skey` is `*`, `collection` defaults to the type's declared collections, `action` defaults to `read`, `create`, `update`, `delete`; `action` values `read_self`, `read`, `create`, `update`, `delete`; `manage` values `create`, `update`, `delete`, none by default.
- Read is all-or-nothing at the space boundary (no per-record, collection or author read grants). `read` also grants `getDelegationToken`; `read_self` reads only the holder's own repo and does not. Write methods accept only OAuth credentials; read and sync methods accept an OAuth scope or a space credential.
- Example scopes in the proposal include one for a personal export or backup tool using `action=read_self` (relevant to a user exporting their own session records), and a wildcard-type scope for reading every space under one authority.
- Consent screens show the declaration `name` rather than the NSID, show an authority as its bidirectionally validated handle (else the DID), and should show a prominent warning for wildcard authority plus wildcard type.
- Permission sets may bundle space permissions (`"resource": "space"`), but `spaceType` must be concrete (no wildcard) and follow namespace authority rules; `collection` may be wildcard or cross-namespace.

## Key facts: XRPC API and simplespace

- Methods under `com.atproto.space`: host (`getSpaceCredential`, `listRepos`, `registerNotify`, `unregisterNotify`), repo (`getRecord`, `listRecords`, `getBlob`, `listBlobs`, `getLatestCommit`, `getRepo`, `listRepoOps`), PDS (`getDelegationToken`, `createRecord`, `putRecord`, `deleteRecord`, `applyWrites`, `listSpaces`), and notification methods (`notifyWrite`, `notifySpaceDeleted`, `notifyCredentialRevoked`).
- `com.atproto.simplespace` is the space-management implementation every PDS MUST support: `createSpace`, `updateSpace`, `deleteSpace`, `getSpace`, `putMember`, `removeMember`, `listMembers`. Config: `readPolicy` and `writePolicy` (`public`, `member-list`, `managing-app`; default `member-list`), `appAccess` (`#open` default, or `#allowList` evaluated against the attested client_id), and `managingApp`. Read and write are independent permissions: write controls whether the authority tracks the writer and forwards notifications, and does not prevent writing to one's own space repo. With `managing-app`, the authority calls `com.atproto.simplespace.checkUserAccess` on the managing app (for example for follower-gating or paid subscriptions).

## Key facts: considerations

- Moderation: a moderation service must be admitted like any other syncer; public labels for space records would leak metadata, so labelers should publish labels as records inside the space. An authority can decline to issue credentials to cut off read access.
- Scaling: no relays, so apps sync directly from PDSes; sync load scales with the number of syncing applications not users; sync APIs are not public so abuse is easier to mitigate.
- Account lifecycle: migration requires enumerating all space repos (`listSpaces`) and blobs (`listBlobs`); the new host publishes its own `#atproto_kem` key; deletion and deactivation propagate to space data; apps syncing only spaces still need the firehose for `#account` and `#identity` events.

## Relevance to session sharing

- A coding-agent session (transcript, tool calls, attachments) could be stored as records of a dedicated space type in a collection list; membership is controlled through simplespace member lists or a managing app.
- Because spaces are not encrypted and every authorised syncer, plus the PDS, can read content, sessions containing secrets or private code must be scrubbed before sharing.
- The `read_self` grant maps to personal export and backup of own sessions; client attestation and `appAccess` allow lists let a space restrict which viewer apps may read it.
- Record values are capped at 1 MiB in the STAR archive profile; large traces would need blobs fetched separately.

## Related

- AT Protocol permissions spec, permission sets, OAuth, DRISL and DASL CIDs, STAR archive format, LtHash, RFC 9421, RFC 7800, RFC 9180, PR 5187 in atproto, permissioned data diary posts, community forum thread.
