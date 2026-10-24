# 0016 Atproto Spaces (bluesky-social/proposals) (source notes)

> Source: https://github.com/bluesky-social/proposals/blob/main/0016-permissioned-data/README.md
> Resolved: https://raw.githubusercontent.com/bluesky-social/proposals/main/0016-permissioned-data/README.md
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-11 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — bluesky-social/proposals has no LICENSE file (raw 404, root listing). Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-a4f4f779/001.md.
> Work: bluesky-social/proposals:0016-permissioned-data
> Quotations: 0 characters verbatim in this file; 37 of 90 allowed for this work across the knowledge base.

## About this source

Proposal 0016 in the bluesky-social/proposals repository, titled 0016 Atproto Spaces. It describes a draft protocol for permissioned (access-controlled) data in atproto. The document says itself that it is a proposal, not the final specification, and that details, terminology and behaviours are likely to change. It points to a community forum thread for discussion and to draft lexicons on an implementation branch (atproto PR 5187). Published date not shown in the file.

## Key facts

- Purpose: an additional protocol alongside public broadcast, for data with an access perimeter. Listed modalities: personal data (bookmarks, mutes, drafts), gated content, socially shared content, and groups (private forums, communities, group chats).
- Spaces give access control, not confidentiality. They are explicitly not end-to-end encrypted; services (PDSes and authorized apps) can read the data they handle. E2EE is out of scope.
- Comparison with public broadcast: record in a space repo instead of a repo; one space repo per (user, space); record authority stays the user DID; URI authority is the space authority DID; commit is an LtHash set-hash digest (public uses a Merkle Search Tree root); commit authenticity is an HMAC (public uses a signature); access gated by a space credential.
- Terminology: space, space repo, repo host, space host, space authority, space credential, delegation token, client attestation, syncer. A PDS fills both repo host and space host roles but these can be separate services.
- A space is identified by a triple: space authority (a DID), space type (an NSID), and space key `skey` (string, max 512 bytes, same syntax as an `rkey`).
- Record URI shape: `at://{spaceDid}/space/{spaceType}/{skey}/{authorDid}/{collection}/{rkey}`. The literal `space` segment sits where a public collection NSID would, so it is never ambiguous. A space reference uses segments up to `skey`; a new `space-ref` Lexicon string format is defined.
- Authority may be a user DID (personal data) or a dedicated DID so a shared space can move between users. Its `#atproto_pds` service endpoint is the space host and its `#atproto` key signs credentials.
- Space type declaration: a Lexicon def with type `space`, fields `description`, `key`, `name`, `name:lang`, `collections` (no wildcards). The type is also the OAuth consent boundary. Any space may hold records of any collection, not just the declared ones.
- Access control rests on two signed assertions: which user (delegation token from the user's PDS) and which app (client attestation). A space may require either, both or neither. Spaces requiring neither still need a credential for syncing.
- Delegation token: JWT with `typ` of `atproto-space-delegation+jwt`, no `lxm` claim, `sub` is the space, `aud` is the space authority's `#atproto_pds`. Single use, default lifetime 60 seconds. Requested via `com.atproto.space.getDelegationToken`, which needs a `read` grant.
- Client attestation: JWT with `typ` `atproto-client-attestation+jwt`, shaped like a `private_key_jwt` client assertion; the authority resolves the `client_id` metadata, fetches JWKS and verifies the signature.
- Space credential: JWT with `typ` `atproto-space-credential+jwt`, signed by the authority's key, no `aud`, carries `cnf.kid`. Default lifetime 10 minutes, maximum 60 minutes. Multi-use across repo hosts.
- Credential key binding: the app supplies a P-256 `did:key` as `credentialKid`; each request carries an HTTP Message Signature (RFC 9421, `ecdsa-p256-sha256`) over the `Authorization` and `Atproto-Space-Audience` headers. Verifiers must accept low-S and high-S signatures. Apps should generate a new keypair per credential.
- Presentation uses `Authorization: Atproto-Space-Credential` scheme. Signature does not bind method or URI; replay against the same audience is allowed until expiry.
- Revocation: short expiry is primary. Optional `com.atproto.space.notifyCredentialRevoked` by `jti`; repo hosts must retain a revocation for at least 60 minutes.
- Space repo commit (`com.atproto.space.defs#commit`) fields: `ver` (currently 1), `repo`, `space`, `rev` (TID), `data` (sha256 of the LtHash state, 32 bytes).
- Repos are created implicitly on first write; an empty repo equals a nonexistent one; deleting all records deletes the repo.
- LtHash state: 2048-byte buffer of 1024 little-endian 16-bit lanes; element is `{collection}/{rkey}/{record_cid}`, expanded with BLAKE3 XOF; add or subtract lanes modulo 65536. Order-independent.
- Authenticity: no signatures, to avoid provable authorship after a leak. Syncer and repo host derive an ephemeral shared secret (ECDH on P-256, HKDF-SHA256 per RFC 9180 section 4.1) using a new DID document key `#atproto_kem` (Multikey, dedicated keypair, held by repo host). MAC is HMAC-SHA256, requested with `Atproto-Space-Want-Mac` header and returned in `Atproto-Space-Mac`. Commit MAC type `atproto-space-repo`, record MAC type `atproto-space-record`.
- Repo serialization: STAR-lite v1 archive with magic bytes `0x2A 0x6C 0x01 0x00`, DRISL-encoded metadata, records sorted lexicographically, each record at most 1 MiB (1,048,576 bytes). Blobs excluded and fetched with `getBlob`.
- Sync: no relays. Space hosts aggregate repo metadata and send notifications; syncers pull from repo hosts. Incremental sync via `com.atproto.space.listRepoOps` with `since`; entries carry the fields rev (TID), collection, rkey, cid and prev. Oplog is a transport optimisation, may be compacted; fallback is full-state recovery via `getRepo`, or healing via `getLatestCommit`, `listRecords` with `excludeValues`, and `getRecord`.
- Write notifications: PDS sends `com.atproto.space.notifyWrite` (rev and data, no record content) to the space host; syncers subscribe through `registerNotify` (time-limited) and `unregisterNotify`; gaps detected through space revisions and `listRepos`.
- Writer set: `listRepos` on the authority returns accounts that have written at least one record, not mere readers or allowed writers; it is a claim, not authoritative.
- Space deletion: authority stops issuing credentials, deletes its own records, sends `notifySpaceDeleted`. Syncers should delete all copies. Member repos are not deleted; records become unreadable to others.
- OAuth scope form: `space:` followed by the type, with optional query parameters authority, skey, collection, action and manage. Actions: `read_self`, `read`, `create`, `update`, `delete`; `manage` verbs create/update/delete. Default `authority` is `self`. Read is all-or-nothing at space boundary; `read_self` does not grant `getDelegationToken`. Wildcard on both authority and type needs a prominent consent warning. Permission sets can bundle space permissions but spaceType may not be a wildcard there.
- XRPC namespace `com.atproto.space`: methods include `getSpaceCredential`, `listRepos`, `getRecord`, `listRecords`, `getBlob`, `listBlobs`, `getLatestCommit`, `getRepo`, `listRepoOps`, `getDelegationToken`, `createRecord`, `putRecord`, `deleteRecord`, `applyWrites`, `listSpaces`, `registerNotify`, `unregisterNotify`, `notifyWrite`, `notifySpaceDeleted`, `notifyCredentialRevoked`.
- Required PDS space management is `com.atproto.simplespace`: `createSpace`, `updateSpace`, `deleteSpace`, `getSpace`, `putMember`, `removeMember`, `listMembers`. Config: `readPolicy` and `writePolicy` (`public`, `member-list`, `managing-app`), `appAccess` (`#open` or `#allowList`), `managingApp`. Managing-app policies call `com.atproto.simplespace.checkUserAccess` on the app. Other space-management implementations are allowed but live on bespoke services.
- Considerations (non-normative): moderation labelers should not publish public labels for space content (metadata leak) and may publish labels inside the space; scaling relies on closed set of syncers and no relays; account migration must enumerate spaces via `listSpaces` and blobs via `listBlobs`; a new host publishes its own `#atproto_kem` key; apps syncing only spaces still need the firehose for `#account` and `#identity` events.

## Related

- AT Protocol OAuth, permission sets, service auth (atproto.com specs)
- Atproto spaces implementation branch (atproto PR 5187) and the permissioned data diary blog posts
- STAR archive format, DASL CID and DRISL, LtHash, RFC 9421, RFC 7800, RFC 9180
