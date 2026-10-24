# The Atproto Spaces Alpha is Live - AT Protocol (source notes)

> Source: https://atproto.com/blog/atproto-spaces-alpha
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-01 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: CC-BY (version unstated; footer also says all rights reserved) — Page footer: Copyright (CC-BY) Bluesky Social PBC 2026. All rights reserved. Ambiguous, so notes only. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/atproto-com-95cd0853/001.md.
> Work: https://atproto.com/blog/atproto-spaces-alpha
> Quotations: 42 characters verbatim in this file; 42 of 90 allowed for this work across the knowledge base.

## About this source

Announcement post on the AT Protocol site (atproto.com blog) saying that an alpha of atproto spaces, the permissioned-data primitive, is available for developers. Publication date is not stated in the page body. These are factual notes, not the original text.

## Key facts

- The feature was previously called private data, then permissioned data, briefly buckets, and is now called atproto spaces.
- Spaces are described as a new protocol primitive for storing and syncing non-public data while keeping portable identity, interoperable data and permissionless participation.
- Everything stored on the protocol before this is public by design (posts, follows, likes, blocks), distributed over servers and rebroadcast by a global firehose.
- The post gives example use cases for non-public data: settings, private bookmarks, forums of dozens to millions of members, and subscription-only publishing.
- A space is likened to a miniature atproto network that can be gated so that only certain people and applications can read it. It can hold a single record or scale to a billion records.
- Familiar pieces remain: users have DIDs, host data in repositories, records are JSON defined by Lexicons, and applications sync repos and build views.
- Access is controlled by a space authority, which is a DID like any other account and sometimes is the user's own account. The authority decides which DIDs may access the space.
- Records live in per-space permissioned repos on the author's PDS.
- The author stresses that spaces give access control, not confidentiality: data is readable by any user or application with access and is not encrypted.
- The smallest spaces have exactly one member (settings, drafts, bookmarks); the largest are communities of millions; a middle case is gated content for subscribers. The post says the design target is a shared social context.
- Sync is lighter than the public broadcast protocol, with facilities for real-time sync. There is no relay for space data, because rebroadcasting is often undesirable; applications sync space data directly from PDS hosts.
- A hosted alpha PDS is offered for experimenting, with an invite code obtained via a Bluesky Social account page. Data there is neither permanent nor stable, may be deleted without warning, and the whole PDS will be deleted after the alpha. Updates to the hosted PDS and SDKs are planned for Thursdays and announced on the atmosphere.community forum.
- Self-hosting: a tagged Docker image `ghcr.io/bluesky-social/atproto:pds-spaces-alpha` is maintained, compatible with the reference PDS distribution and needing no new configuration. The post warns database schemas may change without clean migrations and advises not to migrate real accounts.
- Ecosystem implementations of the proposed spec listed: ZDS (Zig PDS), atproto-crates PDS (Rust), rsky PDS (Rust, maintained by Blacksky), and HappyView (an AppView framework).
- Example app: a bulletin board app at bulletin.my, built as a space where mutuals leave sticky notes; its code is in the `bluesky-social/bulletin` repository. The TypeScript `@atproto` packages were released as alpha snapshot versions installable with the `alpha` tag.
- The protocol specification is the proposal at `0016-permissioned-data` in the bluesky-social proposals repo; the reference implementation is on a spaces branch of the atproto repo (pull request 5187), which may diverge from published packages.
- Alpha caveats listed by the authors: the code has not undergone careful security review (do not upload sensitive information, especially other people's); no backups and possibly destructive migrations; the alpha PDS goes away at the end; protocol design, SDKs and schema are not final.
- The authors aim to launch later in the year and to keep iterating through the fall.

## Quotations

- The authors say the software is "ALPHA SOFTWARE DO NOT USE IT IN PRODUCTION" (atproto.com blog, spaces alpha post).

## Related

atproto spaces / permissioned data, PDS, space authority, Lexicons, bluesky-social/proposals 0016, Bulletin sample app, Tangled, Blacksky rsky.
Relevance to session sharing: sessions shared into a space would be access-controlled but readable (not encrypted) by every member; alpha status and absence of security review matter for any design.
