# Bluesky API Guide 2026: Posting with the AT Protocol (source notes)

> Source: https://www.upload-post.com/bluesky-api/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-11 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — Page footer states All rights reserved (c) 2026 Upload-Post.com. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/upload-post-com-a5821d3a/001.md.
> Work: https://www.upload-post.com/bluesky-api/
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A vendor guide page from Upload-Post (a multi-network posting API product) titled Bluesky API Guide 2026: Posting with the AT Protocol. It explains how to post to Bluesky over XRPC, with curl and Python examples, and ends by promoting the vendor's own API. The footer reads that Upload-Post.com holds all rights. Its source citations are marked as read on 29 September 2026; no explicit publication date is shown.

## Key facts

- Bluesky has no developer programme, no app review and no paid tier. Posts are records of type `app.bsky.feed.post` in the account's repo on its PDS; likes, follows and reposts are records too.
- Endpoints are XRPC methods such as `com.atproto.repo.createRecord`, called at `https://<pds-host>/xrpc/<method>`; for Bluesky-hosted accounts `https://bsky.social` works as the entry point. `https://public.api.bsky.app` serves cached public reads without authentication.
- The page notes developer docs moved from docs.bsky.app to bsky.network/docs.
- Auth comparison: app password (via `com.atproto.server.createSession`, for bots, scripts and CLIs acting as your own account, minutes of effort) versus atproto OAuth (PAR, PKCE and DPoP-bound tokens, needs published client metadata, an SDK is strongly recommended, a real integration project). Never use the main account password.
- Session: `accessJwt` and `refreshJwt` returned; refresh with `com.atproto.server.refreshSession`. This page says the access token expires after a few minutes, whereas the Outstand article says roughly two hours (see contradictions in the staging file).
- `createSession` limit: 30 per 5 minutes and 300 per day per account.
- `createRecord` needs `text` and `createdAt`; `langs` up to three codes; `tags` up to eight extra hashtags not in the text. Response gives an `at://` URI and a CID; keep both for replies and quotes.
- Post text: 300 graphemes and 3,000 bytes. Longer text should be split into a reply thread.
- Facets: Bluesky does no markup and no URL detection. Three feature types: `#link` (`uri`), `#mention` (`did`) and `#tag` (`tag`). Indexes are UTF-8 byte offsets, start inclusive, end exclusive. Mentions need handle resolution (for example `com.atproto.identity.resolveHandle`). Facets must not overlap.
- Images: `com.atproto.repo.uploadBlob`, then `app.bsky.embed.images`; up to four images, each up to 2 MB, each with alt text; send `aspectRatio`. The newer `app.bsky.embed.gallery` has a ceiling of 20, clients asked to stay at 10.
- Link cards use `app.bsky.embed.external`; the client fetches title, description and thumbnail and uploads the thumb as a blob.
- Replies: `reply` with `root` and `parent`, each uri and cid. In a self-written thread, post 1 is root for all replies.
- Video: verified email required on Bluesky-hosted accounts (check with `com.atproto.server.getSession`). Simple path uploads with `uploadBlob` and embeds `app.bsky.embed.video` but processing starts only after the post exists. Recommended path: `com.atproto.server.getServiceAuth` (audience `did:web:<your PDS host>`, method `com.atproto.repo.uploadBlob`, about 30 minutes validity), upload to `https://video.bsky.app/xrpc/app.bsky.video.uploadVideo`, poll `app.bsky.video.getJobStatus`. Limits per the page: 10 minutes and 300 MB since August 2026; daily cap 25 videos or 10 GB per account; up to 20 WebVTT captions.
- Limits table: record writes 5,000 points per hour and 35,000 per day (create 3, update 2, delete 1; at most 1,666 new records an hour and 11,666 a day); 3,000 requests per 5 minutes per IP; blob upload 52,428,800 bytes (50 MB) on a Bluesky PDS. The page notes other PDS hosts may set their own limits. Over a limit: HTTP `429`.
- Python `atproto` package wraps sessions, facets (`TextBuilder`), uploads and replies; it suggests exporting and restoring the session string to avoid repeated logins.
- Scheduling is not native to the API: `createRecord` publishes immediately and `createdAt` is only a client-declared timestamp.
- Vendor product details (not protocol facts): free plan 10 uploads a month and 2 profiles; paid plans from $24 a month ($16 billed annually); scheduling up to 365 days ahead; an MCP server is offered.

## Related

- outstand-so-f67b4c56 (Outstand Bluesky API article) covers the same ground with more depth
- bsky.network/docs: rate limits, OAuth client, video guide, rich text guide
