# Bluesky API: AT Protocol auth, facets, media and rate limits (source notes)

> Source: https://www.outstand.so/blog/bluesky-api
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-11 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — no license statement found in page (grep of archived HTML for license/copyright terms found nothing). Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/outstand-so-f67b4c56/001.md.
> Work: https://www.outstand.so/blog/bluesky-api
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A vendor blog article from Outstand (a social-media posting API product) that serves as a practical reference for the Bluesky and AT Protocol posting API: hosts, auth, records, facets, media, rate limits and failure modes. The text describes itself as the auth story as it stands in 2026. It ends with a product pitch for Outstand's own API. Treat limits as the vendor's reading of lexicons and docs; the article says each number is linked to its lexicon or spec page. No explicit publication date is shown in the visible text.

## Key facts

- The author stresses there is no single Bluesky API: AT Protocol is the open spec and Bluesky is an app on it. Calls are XRPC methods under `/xrpc/`, named for lexicons: `com.atproto.*` for protocol operations and `app.bsky.*` for the app layer. There is no separate REST API.
- Four host roles: `bsky.social` (entryway: account creation, sessions, token signing), `*.host.bsky.network` (the actual PDS), `public.api.bsky.app` (cached public AppView, no auth) and `video.bsky.app` (video upload and transcode, scoped service token).
- Two auth paths. App passwords (created at the app settings page) are exchanged through `com.atproto.server.createSession` for `accessJwt` and `refreshJwt`; the access token lasts roughly two hours and is renewed through `com.atproto.server.refreshSession`.
- OAuth profile as described: no dynamic client registration, `client_id` is an HTTPS URL serving client metadata JSON, PAR, PKCE and DPoP mandatory. The authorization server for Bluesky-hosted accounts is the entryway, not the PDS.
- Guidance: OAuth for products with end-user login; app passwords remain supported for bots, CLIs and server-side integrations on accounts you control. App passwords have no scopes. The vendor itself uses app passwords and admits it has no `transition:*` scope story.
- Video uploads require a service-auth token from `com.atproto.server.getServiceAuth` whose `aud` is the real PDS as `did:web:<pds-host>`, not `did:web:bsky.social`. The PDS endpoint is found in the DID document service entry with id `#atproto_pds` (resolved via plc.directory for did:plc).
- Posting is `com.atproto.repo.createRecord` with collection `app.bsky.feed.post`; it returns `uri` and `cid`. The AT-URI is `at://<did>/<collection>/<rkey>`; `com.atproto.repo.deleteRecord` takes repo, collection and rkey separately. Replies and quotes need both URI and CID. Public web URL form is `https://bsky.app/profile/<did>/post/<rkey>`. `createdAt` is client-supplied and not overwritten.
- Text limits on `app.bsky.feed.post`: `maxGraphemes` 300 (grapheme clusters) and `maxLength` 3000 (UTF-8 bytes). `langs` capped at 3 entries.
- Facets are not auto-detected by the protocol. Facet ranges are `byteSlice` byte offsets into UTF-8 text (start inclusive, end exclusive). Mention facets need a DID (resolve via `com.atproto.identity.resolveHandle`); ranges must not overlap; hashtag `tag` capped at 640 bytes / 64 graphemes without the leading `#`.
- Images: `com.atproto.repo.uploadBlob` with raw bytes; blob limit 2,000,000 bytes (formerly 1 MB), up to 4 images per post, `alt` required, `aspectRatio` optional in `app.bsky.embed.images`. A newer `app.bsky.embed.gallery` has a schema ceiling of 20 items, soft authoring limit of 10, and requires `aspectRatio`.
- A post carries exactly one embed (images, video, quote, external card or `recordWithMedia`).
- Video pipeline: check `app.bsky.video.getUploadLimits`, mint service token with `lxm=com.atproto.repo.uploadBlob`, POST to `app.bsky.video.uploadVideo`, poll `app.bsky.video.getJobStatus` until `JOB_STATE_COMPLETED` (other states `JOB_STATE_CREATED`, `JOB_STATE_ENCODING`, `JOB_STATE_SCANNING`, `JOB_STATE_FAILED`). Verified email required for Bluesky-hosted accounts. Re-uploading identical bytes returns 409 `already_exists` with the original job id. Video blob cap 300,000,000 bytes (formerly 100mb), `video/mp4` only, up to 20 WebVTT caption files of at most 20,000 bytes each.
- Threads: each reply has `root` (pinned to first post) and `parent` refs, each with uri and cid. Partial failure policy needs deciding in advance; blind retry double-publishes.
- Write rate limits are points per account: 5,000 per hour and 35,000 per day. CREATE costs 3 points, UPDATE 2, DELETE 1; `com.atproto.repo.applyWrites` gets no discount. HTTP limits: 3,000 per 5 minutes per IP across endpoints; `createSession` 30 per 5 minutes and 300 per day per account; `updateHandle` 10 per 5 minutes and 50 per day; blob upload size at the PDS 52,428,800 bytes (50 MB).
- Advice: create one session, persist JWTs and refresh before the two-hour expiry; use `public.api.bsky.app` for public reads. Only 409 on video and genuine 429 deserve retries.
- The vendor lists what its own product does not do (no OAuth, no gallery embed, no link cards, video cap 100 MB, no captions) and describes its own API endpoints; these are product details, not protocol facts.

## Related

- AT Protocol OAuth spec, lexicon spec, rate-limits and API host documentation at bsky.network/docs
- upload-post.com Bluesky API page (similar vendor guide)
- Relevant to agent-session sharing mainly as practical constraints for writing records to a PDS: record size and text limits, blob size, session and rate limits.
