# bluesky-social/atproto#3392: Add restrictions on blobstore consumption (source notes)

> Source: https://github.com/bluesky-social/atproto/issues/3392
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-02 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue; user content. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-f4b2a54b/001.md.
> Work: bluesky-social/atproto#3392
> Quotations: 14 characters verbatim in this file; 14 of 90 allowed for this work across the knowledge base.

## About this source

A GitHub feature-request issue in the atproto repository, opened by @yamarten and still open at collection time. The API metadata gives created and updated timestamps in January 2025, and the issue has 1 comment.

## Key facts

- The issue says the reference PDS implementation has a per-blob size cap, `PDS_BLOB_UPLOAD_LIMIT`, but no cap on the total blob storage an account can consume.
- Concern raised: a few accounts could over-consume storage and raise costs for PDS administrators.
- Proposal: an upper limit on total blob bytes uploaded within a time window, so administrators can control cost.
- Alternative noted by the author: the existing rate limit on uploadBlob does not reflect cost, since blob sizes vary. A window-less total cap is also mentioned, with a warning that without garbage collection or deletion it would disadvantage long-term users.
- Trends the author lists as accelerating blob use: larger individual blob limits for Bluesky video, the ATFile tool that uses a PDS as file storage, a video-streaming experiment using blobs by GrayHaze, and interest in image-posting services.
- A commenter (@Invertex) supports limits, suggests paid higher quotas, and suggests a "limit rollover" so overage is deducted from the next period (capped at 2x the allowance, with a strong warning). They argue periods should not be as long as a year.

## Relevance to session sharing

- Session transcripts and traces stored as blobs would count against any such per-account storage quota; large agent logs are a plausible driver of blob consumption.

## Related

- `PDS_BLOB_UPLOAD_LIMIT`, uploadBlob, ATFile, GrayHaze and related blob-size-limit discussions in the same repo.
