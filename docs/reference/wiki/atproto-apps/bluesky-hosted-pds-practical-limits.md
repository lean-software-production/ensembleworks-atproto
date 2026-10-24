# Writing to Bluesky-Hosted PDSes: Practical Limits

> Sources: Outstand, "Bluesky API: AT Protocol auth, facets, media and rate limits" (vendor blog; notes only); Upload-Post, "Bluesky API Guide 2026" (vendor guide; notes only); karanshukla/kodamachi#228 (notes only); all collected 2026-10-23; source inventory: Bluesky API: AT Protocol auth, facets, media and rate limits (source notes) (attributed source notes; Unknown); Bluesky API Guide 2026: Posting with the AT Protocol (source notes) (attributed source notes; Unknown); Use permissioned data when it releases in atprotol (source notes) (attributed source notes; Unknown); This Website is Hosted on Bluesky (source notes) (attributed source notes; Unknown)
> Raw: [Outstand Bluesky API guide (notes)](../../raw/atproto-apps/bluesky-api-at-protocol-auth-facets-media-and-rate-limits-notes.md); [Upload-Post Bluesky API guide (notes)](../../raw/atproto-apps/bluesky-api-guide-2026-posting-with-the-at-protocol-notes.md); [kodamachi#228 (notes)](../../raw/atproto-apps/use-permissioned-data-when-it-releases-in-atprotol-notes.md); [this-website-is-hosted-on-bluesky-notes](../../raw/atproto-apps/this-website-is-hosted-on-bluesky-notes.md)
> Updated: 2026-10-24

## Overview

Teammates whose accounts live on Bluesky's hosted PDSes impose real operational ceilings on a session-sharing tool. A proposed exporter that writes every session entry as a record would consume their write budget. Two vendor guides from 2026 (third-party readings of the docs, not official specs) agree that **write limits are per-account points: 5,000 per hour and 35,000 per day, with a create costing 3 points**. That allows roughly 1,666 new records an hour. A chatty agent session published entry-by-entry could hit this ceiling, so entries should be batched into fewer records. kodamachi#228 found the same 5000/35000 bucket on the spaces alpha PDS and noted that self-hosting removes the ceiling.

## Hosts and auth

- XRPC methods under `/xrpc/`: `com.atproto.*` for protocol operations and `app.bsky.*` for the app layer.
- Host roles (Outstand):
  - `bsky.social` is the entryway, handling sessions and token signing. It is the OAuth authorization server for Bluesky-hosted accounts.
  - `*.host.bsky.network` is the actual PDS.
  - `public.api.bsky.app` is the cached, unauthenticated AppView.
  - `video.bsky.app` handles video.
- App passwords via `com.atproto.server.createSession` return `accessJwt`/`refreshJwt`. App passwords have no scopes. `createSession` is limited to 30 per 5 minutes and 300 per day per account. OAuth (PAR, PKCE, DPoP) is the route for products with end-user login. See [ATProto OAuth and Permissions](../atproto/oauth-and-permissions.md).

> **Status: Disputed**
> Session access-token lifetime: Outstand says the `accessJwt` lasts roughly two hours and should be refreshed before the two-hour expiry. Upload-Post says it expires after a few minutes. Neither cites the server code. Treat it as server-defined and refresh on `ExpiredToken`.

## Limits (as reported by both guides)

| Limit | Value |
|---|---|
| Record writes | 5,000 points/hour, 35,000/day; create 3, update 2, delete 1. `applyWrites` gets no discount (Outstand). |
| HTTP requests | 3,000 per 5 minutes per IP |
| Blob upload at a Bluesky PDS | 52,428,800 bytes (50 MB). Other PDS hosts may set their own limits. |
| Post text | 300 graphemes, 3000 bytes (`app.bsky.feed.post`) |
| Images | up to 4 per post, 2,000,000 bytes each (formerly 1 MB) |

Notes:

- Over-limit responses are HTTP `429`. Both guides advise retrying only genuine 429s, and video 409s. Blind retries of `createRecord` double-publish.
- `createdAt` is client-supplied and not overwritten. Scheduling is not native.
- Facets (links, mentions, tags) are byte-offset annotations that the client must compute. The protocol does not auto-detect them. This is relevant if session summaries are cross-posted as Bluesky posts.

## Implications

- Batch session entries, for example one record per turn or per N entries, instead of one record per JSONL line.
- Use idempotent record keys so that retries do not duplicate entries.
- Consider recommending that teams self-host a PDS, or use a dedicated sharing PDS, for heavy agent usage. See [ATProto PDS Operation and Observability](../atproto/pds-operation.md).

## See Also

- [ATProto Blobs and Size Limits](../atproto/blobs-and-size-limits.md)
- [ATProto Repository, Records and Lexicon](../atproto/repository-and-records.md)

## Historical arbitrary-blob hosting experiment

Daniel Mangum demonstrates HTML stored as a blob and made retrievable by a custom record referencing it. Upload alone did not make the temporary blob available; the record reference changed its retention and availability. His experiment also uses an open embed union to attach a custom type ignored by the Bluesky app. This is an acknowledged unintended hosting use, not an availability promise. Public blob retrieval is unauthenticated, and browser-serving protections constrain direct HTML execution; private session storage cannot rely on obscuring a blob URL.

## Snapshot scope of upload ceilings

The vendor-reported hosted upload ceiling here differs from the reference PDS default in [ATProto Blobs and Size Limits](../atproto/blobs-and-size-limits.md). These are different host-policy and source snapshots, not one universal protocol constant. The older Mangum experiment below is historical evidence of behavior, not a current hosting promise. Query the target server’s advertised policy before relying on a limit.
