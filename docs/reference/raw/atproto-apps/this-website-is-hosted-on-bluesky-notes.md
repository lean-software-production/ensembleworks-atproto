# This Website is Hosted on Bluesky (source notes)

> Source: https://danielmangum.com/posts/this-website-is-hosted-on-bluesky/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-03 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — no license statement found in archived page. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/danielmangum-com-8c71a1e5/001.md.
> Work: https://danielmangum.com/posts/this-website-is-hosted-on-bluesky
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A blog post by Daniel Mangum, dated November 24, 2024 on the page, with a 14-minute read time. It demonstrates that an HTML file can be hosted on Bluesky infrastructure by uploading it as an AT Protocol blob and referencing it from a custom record. The author says he told the Bluesky team before publishing and that the behavior is known and not intended use. These notes are a digest; the original is under all rights reserved (no license statement found).

## Key facts

- Core claim: hosting a website this way depends on AT Protocol-level APIs implemented by a PDS, not on anything specific to Bluesky the app. The author's account sits on a PDS at `porcini.us-east.host.bsky.network`, reached through the `bsky.social` entryway.
- Two primary content types in atproto apps: records (structured entities users create) and blobs (larger unstructured data such as media), where blobs are exposed via a record that references them.
- Per the blob spec as quoted by the author, blobs are uploaded separately from records and held in temporary storage until a record references them; unreferenced temporary blobs should be garbage collected and are excluded from `listBlobs` output.
- The PDS cannot know the intended Lexicon at upload time, so it applies only generic limits then and enforces Lexicon-defined limits when the record is created.
- Session flow shown: `com.atproto.server.createSession` returns an `accessJWT`; `com.atproto.repo.uploadBlob` uploads the file (POST with the HTML content type); the response is a blob object with `$type` of `blob`, a `ref` with `$link` (a CID), `mimeType` `text/html` and `size` 268.
- Before referencing, `getBlob` for the new CID returned an InternalServerError rather than the blob, and the `listBlobs` count stayed at 391.
- Bluesky's own `app.bsky.embed.images` embed rejects a non-image blob with error `InvalidMimeType`; the PDS also checks that the MIME type in the reference matches the stored blob.
- A record of the author's own collection `com.danielmangum.hack.website` containing the blob reference was accepted by the PDS with `validationStatus` of `unknown`, because the PDS does not know that Lexicon. After that the `listBlobs` count rose to 392 and the blob became publicly fetchable.
- `getBlob` needs no access token, since unauthenticated parties must be able to fetch blobs. On `bsky.social` it answers with a redirect to the user's PDS host.
- The PDS finds blob refs in a record with a recursive `findBlobRefs` function that walks arrays and objects up to a depth of 32 layers and looks for blob-typed values; this works without a Lexicon schema.
- Security: the blob spec says serving arbitrary uploads directly to browsers raises XSS-style issues, requires a Content Security Policy on `getBlob`, and says apps must proxy blobs through an independent CDN or service. The Bluesky PDS sets `x-content-type-options` to nosniff and a CSP of `default-src 'none'; sandbox`.
- Default blob upload limit in the PDS config is 5 MB (`5 * 1024 * 1024`).
- Images in the Bluesky app are served from `cdn.bsky.app` (feed_thumbnail and feed_fullsize variants) via an `ImageUriBuilder`; the post record holds only the CID.
- The author argues this amounts to free but unreliable arbitrary file hosting, and points to a GitHub issue (atproto issue 523) that explains why `getBlob` is unauthenticated: image labeling, user content export and future uses.
- Open unions: per the Lexicon spec unions are open by default unless marked `closed`. The `app.bsky.feed.post` embed union is not closed, so a post with a custom embed `$type` of `com.danielmangum.hack.sites` was accepted with `validationStatus` of `valid`; the Bluesky app silently ignores it, but another app could render it.
- The author sees these micro-extensions as one of the most interesting features of Lexicons and imagines small code snippets run in a WebAssembly sandbox.

## Relevance to session sharing

- Shows that arbitrary blobs plus custom-NSID records are accepted by a Bluesky-hosted PDS without schema validation, so session transcripts could be stored as blobs referenced from custom records; also shows that public blob access is unauthenticated, which matters for private sessions.

## Related

- AT Protocol blob specification, Lexicon specification, PDS entryway, `com.atproto.repo.uploadBlob`, `com.atproto.sync.getBlob`, `com.atproto.sync.listBlobs`.
