# Increasing Bluesky Post Image Size Limit · bluesky-social/atproto · Discussion #4832 (source notes)

> Source: https://github.com/bluesky-social/atproto/discussions/4832
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-02 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub discussion; user content. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-e8add5ad/001.md.
> Work: bluesky-social/atproto#4832
> Quotations: 71 characters verbatim in this file; 71 of 90 allowed for this work across the knowledge base.

## About this source

A "Dev Announcements" discussion in the atproto repository, posted by maintainer bnewbold on Apr 7, 2026, titled "Increasing Bluesky Post Image Size Limit". It has 4 comments and 4 replies with discussion up to Apr 23, 2026.

## Key facts

- The announcement says the `app.bsky.embed.images` lexicon limits image blobs to 1 MByte (one million bytes), and that estrattonbailey plans to raise this to 2 MByte (two million bytes) by publishing an updated lexicon and TypeScript SDK, then enabling it in the Bluesky app.
- Outside the lexicon, the bsky client and CDN will also accept image dimensions up to 4000 by 4000 pixels, up from 2000 by 2000.
- Further changes to image embeds are expected, for example a "gallery" embed with more than four images.
- Ecosystem impact as stated: validation strictness in TypeScript lexicon SDKs is configurable; PDS operators will see marginally more blob storage and bandwidth; bsky video size limits are already 100 MByte or more; independent appviews and clients may need to update lexicon validation, though it has not always covered blob size; Bluesky's image CDN users need no change. A tracking PR is referenced.
- Lexicon evolution: the change technically breaks the evolution rules, since new valid records look invalid to older software. Similar breaking changes were made before when video embed sizes rose. The author calls this a bad precedent but also says strict media blob size limits feel constraining in practice.
- Other lexicons mentioned as having 1 MByte image limits: `pub.leaflet.blocks.image` and `social.grain.photo`.
- Ideas floated by the author: a flag on the schema `blob` type marking `maxSize` as soft or hard (permanent); alternatives not chosen were an `imagesV2` embed type and an optional `fullImage` field. He asks whether other limits could be soft (images per embed, currently max 4; alt text size; moderation report size) and says the team is firmly committed to the 300 character `app.bsky.feed.post` limit.
- Comment thread: Bossett proposes expressing limits as "accepts" values; bnewbold worries flexibility invites boundary pushing and wants consistent acceptance across PDSes, appviews and clients. OneDeuxTriSeiGo argues for lifting blob limits in the image lexicon and having PDS or appviews transform blobs; bnewbold replies PDS should stay simple and that specialised record types with flexible limits suit other uses. jeffb4 (Apr 23, 2026) says the non-conformant lexicon change indirectly caused a service problem for the Northsky PDS provider and that an `imagesV2` with client fallback might have avoided it.
- bnewbold also considers removing `goat` lints that recommend limits on string and blob definitions.

## Relevance to session sharing

- Directly relevant to designing lexicons for session records and attached blobs: shows the maintainers' current view on schema evolution, hard versus soft constraints, and why PDS hosts avoid per-lexicon blob policy.

## Related

- Discussion on raising blob size limits, blob consumption issue, `app.bsky.embed.images`, Grain and Leaflet lexicons, `goat`.
