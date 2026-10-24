# ATProto Spaces (Permissioned Data)

> Sources: bluesky-social/proposals `0016-permissioned-data` README (Bluesky; notes only); proposals PR #94 and PR #115 by dholms (notes only); atproto.com "The Atproto Spaces Alpha is Live" (Bluesky; notes only); karanshukla/kodamachi#228 and ewanc26/wolfram#35 (implementer issues; notes only); Atmosphere Discourse topic 923 (notes only); Hacker News item 49379732 (notes only); socialdept/atp-spaces README (MIT); all collected 2026-10-23; source inventory: bluesky-social/proposals: 0016-permissioned-data (Atproto Spaces) (source notes) (attributed source notes; Unknown); Permissioned data (source notes) (attributed source notes; Unknown); 0016: Consistently rename to atproto spaces (source notes) (attributed source notes; Unknown); The Atproto Spaces Alpha is Live - AT Protocol (source notes) (attributed source notes; Unknown); Use permissioned data when it releases in atprotol (source notes) (attributed source notes; Unknown); feat(spaces): implement AT Protocol Spaces once upstream stabilises (source notes) (attributed source notes; Unknown); Early permissioned data proposal draft feedback (source notes) (attributed source notes; Unknown); ATProto spaces: A new extension to ATProto that enables non-public data (source notes) (attributed source notes; Unknown); socialdept/atp-spaces (Copyright (c) 2025 Social Dept, socialdept/atp-spaces; Unknown)
> Raw: [proposal 0016 (notes)](../../raw/atproto/bluesky-social-proposals-0016-permissioned-data-atproto-notes.md); [proposals PR 94 (notes)](../../raw/atproto/permissioned-data-notes.md); [proposals PR 115 (notes)](../../raw/atproto/0016-consistently-rename-to-atproto-spaces-notes.md); [spaces alpha post (notes)](../../raw/atproto/the-atproto-spaces-alpha-is-live-at-protocol-notes.md); [kodamachi#228 (notes)](../../raw/atproto-apps/use-permissioned-data-when-it-releases-in-atprotol-notes.md); [wolfram#35 (notes)](../../raw/atproto-apps/feat-spaces-implement-at-protocol-spaces-once-upstream-notes.md); [Discourse 923 (notes)](../../raw/atproto/early-permissioned-data-proposal-draft-feedback-notes.md); [HN 49379732 (notes)](../../raw/atproto/atproto-spaces-a-new-extension-to-atproto-that-enables-non-notes.md); [socialdept/atp-spaces](../../raw/atproto-apps/socialdept-atp-spaces.md)
> Updated: 2026-10-24

## Overview

**Atproto spaces** are Bluesky's extension for non-public data. Over its history the proposal has been called private data, permissioned data and briefly buckets. A space is an authorisation and sync boundary identified by an `(authority, type, skey)` triple:

- the **space authority** is a DID that decides who may read;
- each member's records live in a per-space repo on *their own* PDS;
- apps sync space data directly from PDSes with a short-lived **space credential**.

There is no relay or firehose for space data. The most important property for this project is that **spaces provide access control, not confidentiality.** Data is not end-to-end encrypted. Every authorised app, and the PDSes involved, can read it. Spaces are a natural home for team-visible coding sessions, but secrets must be scrubbed before publishing; see [Secret and Context Leakage in Shared Sessions](../security-privacy/secret-leakage-in-shared-sessions.md).

**Status at collection:** alpha.
- The proposal says it is not final and that details are likely to change.
- The hosted alpha PDS will be deleted after the alpha, and its database schemas may change without clean migrations.
- The code has not had careful security review.
- The atp-spaces README warns: "**Don't use this in production.**" (socialdept/atp-spaces, MIT).

## Timeline (from implementer issues and PRs)

- Late June 2026: proposals PR #94 (permissioned-data proposal, by dholms) opened. Discourse topic 923 collects community feedback.
- July 3, 2026: PR #94 merged as `0016-permissioned-data`, according to kodamachi#228.
- 2026-08-18: alpha packages published on the `alpha` dist-tag (`0.0.0-spaces-alpha-20260818163953`), alongside an invite-gated alpha PDS. The announcement post is dated 2026-08-20 in kodamachi#228's comments.
- 2026-09-10: an alpha update with breaking changes (see Outdated below).
- 2026-09-28: proposal renamed to atproto spaces (PR #115). 2026-09-29: new `space-ref` lexicon string format, per wolfram#35.
- The reference implementation is atproto PR 5187 on a spaces branch, still a draft when kodamachi#228 checked it.

## Model

- **Space repo**: one account's records in one space. It is auto-created on first write and disappears when its last record is deleted. The space itself persists.
- **Addressing**: `at://{spaceDid}/space/{spaceType}/{skey}/{authorDid}/{collection}/{rkey}`. A space alone is the prefix through `skey`. `skey` is at most 512 bytes, with `rkey` syntax.
- **Space type**: an NSID that is also the OAuth consent boundary. It resolves to a Lexicon definition with `"type": "space"` that lists default `collections`. Any space may still hold records of any collection.
- **Commit**: an LtHash set-hash digest instead of a Merkle Search Tree root. It is order-independent, and the syncer recomputes it locally.
- **Records**: CBOR. `getRepo` returns a STAR-lite archive, and each record value is capped at 1 MiB (1,048,576 bytes). Blobs are fetched separately with `getBlob`.
- **Sync**: incremental via `com.atproto.space.listRepoOps` with `since`, with full recovery via `getRepo`. The PDS sends best-effort `notifyWrite` to the space host. Syncers subscribe with `registerNotify` and fetch data from repo hosts directly. The writer set from `listRepos` is the authority's claim of who has written, not a reader list.
- **Deletion**: the authority stops issuing credentials and sends best-effort `notifySpaceDeleted`. Members' records remain their data but become unreadable to others.

## Access control

- Access combines a **delegation token** (which user: minted by the user's PDS, single-use, default 60 seconds) and a **client attestation** (which app: a JWT verified against the client's metadata JWKS). An authority may require either, both or neither.
- Requests are authorised with a **space credential** (`com.atproto.space.getSpaceCredential`). It is signed by the authority and usable across all repo hosts in the space.
- **OAuth scope**: `space:<spaceType>[?authority=<did>][&skey=…][&collection=…][&action=…][&manage=…]`. Actions are `read_self`, `read`, `create`, `update`, `delete`. **Read is all-or-nothing per space.** There are no per-record, collection or author read grants. `read_self` reads only your own repo, which fits personal export and backup.
- **`com.atproto.simplespace`** is a management API every PDS must support:
  - methods: `createSpace`, `putMember`, `removeMember`, `listMembers`, among others;
  - `readPolicy` / `writePolicy`: `public`, `member-list` or `managing-app`;
  - `appAccess`: `#open` or an `#allowList` of client ids.
- kodamachi#228 rejected `managing-app` for its use case because record readability would then depend on the managing app staying online. It also found that an unreachable managing app fails closed.

> **Status: Outdated** (2026-10-23)
> kodamachi#228 (checked against the August alpha) and the atp-spaces quick-start use `addMember` and a single `policy`. wolfram#35 records that the 2026-09-10 alpha update renamed `addMember` to `putMember` and split `policy` into `readPolicy` and `writePolicy`, which is what the current proposal README specifies. The early draft excerpt on Discourse 923 also used an `ats://` scheme and `#atproto_space` DID-document ids. The current README uses `at://…/space/…` and the authority's `#atproto_pds` service and `#atproto` key.

### Credential lifetime and commit authenticity

> **Status: Disputed**
> The proposal README says space credentials last 10 minutes by default and 60 minutes at most. It says commit authenticity uses an HMAC derived per request via ECDH with each account's `#atproto_kem` key, deliberately, so that leaked data carries no transferable proof of authorship. It also says credentials are bound to an app-held P-256 key through RFC 9421 HTTP Message Signatures.
> Implementer sources describe the alpha differently:
> - kodamachi#228 read the PDS branch and reports that credentials live 7200s and are not single use. It also reports that `com.atproto.space.defs#signedCommit` carries a signature by the author's atproto signing key, so an author writing directly is identifiable. Its anonymity design depends on that.
> - Discourse 923 (gui.do) also cites a 2 hours default.
> - The atp-spaces README advertises DPoP binding and commits verified against a locally computed set hash "signature and all".
>
> The sources do not establish whether the proposal text has moved ahead of the alpha code, or the reverse. Design against the deniable-MAC model only after checking the current implementation.

## Community concerns worth carrying into design

- **Privacy and erasure** (Discourse 923, gui.do):
  - aggregators holding space data become processors;
  - members cannot see who else can read;
  - expiry is not erasure, and the only purge signal is whole-space, best-effort `notifySpaceDeleted`.
- **Availability** (Discourse 923): the authority's PDS is a single point of failure for credential issuance.
- **Open design questions** (bnewbold on PR #94 and Discourse 923):
  - nothing is settled until multiple interoperating implementations exist;
  - moderation and anti-abuse are not fleshed out;
  - account-status and identity events still require the public firehose (`#account`, `#identity`);
  - notifications are best effort.
- **Client privacy** (matthieusieben on PR #94): including `client_id` in credentials could reveal which member uses which app in small groups.
- **Reception** (HN 49379732): commenters distinguish restricted access from encryption. Commenters stress again that spaces are not encrypted.
- **Rate limits** (kodamachi#228, alpha PDS): writes share a bucket keyed on the writer DID at 5000 points per hour and 35000 per day, with creates costing 3. Self-hosting removes the ceiling.

## Fit for coding-session sharing

- A session can become records of a dedicated space type, with a team's members in a `member-list` policy. Remote viewers then read with one space credential, across every member's PDS.
- Sharing all sessions in a project folder maps to one space per project, or one space per team with a project field. Read is all-or-nothing per space, so the space boundary *is* the sharing boundary.
- Large transcripts must respect the 1 MiB record cap and put bulk content in blobs; see [ATProto Blobs and Size Limits](blobs-and-size-limits.md).
- For production, wait for the stabilisation gates listed in wolfram#35:
  - out of alpha;
  - stable lexicons and credential flows;
  - a reference implementation on the normal release path;
  - migration guidance.

## See Also

- [Atmospheric Groups](atmospheric-groups.md)
- [ATProto OAuth and Permissions](oauth-and-permissions.md)
- [ATProto Repository, Records and Lexicon](repository-and-records.md)
- [Secret and Context Leakage in Shared Sessions](../security-privacy/secret-leakage-in-shared-sessions.md)

## Application contrasts

- [Germ E2EE messaging](../atproto-apps/germ-e2ee-messaging.md) separates device-held confidentiality from Spaces access control.
- [Hosted PDS practical limits](../atproto-apps/bluesky-hosted-pds-practical-limits.md) records vendor-reported host policy and the historic custom-blob experiment.
