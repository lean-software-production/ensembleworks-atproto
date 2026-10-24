# ATProto Blobs and Size Limits

> Sources: atproto.com Blob spec (Bluesky Social PBC and Contributors, CC-BY), undated; atproto.com "Make the PDS your own: customization and metrics" (notes only); bluesky-social/atproto issue #3392 and discussions #1740 and #4832 (notes only); all collected 2026-10-23; source inventory: Blobs - AT Protocol (Bluesky Social PBC and Contributors, AT Protocol website; Unknown); Make the PDS Your Own: Customization and Metrics - AT Protocol (source notes) (attributed source notes; Unknown); bluesky-social/atproto#3392: Add restrictions on blobstore consumption (source notes) (attributed source notes; Unknown); Consider raising the size limit of blobs · bluesky-social/atproto · Discussion #1740 (source notes) (attributed source notes; Unknown); Increasing Bluesky Post Image Size Limit · bluesky-social/atproto · Discussion #4832 (source notes) (attributed source notes; Unknown)
> Raw: [atproto Blob spec](../../raw/atproto/blobs-at-protocol.md); [PDS customization and metrics post (notes)](../../raw/atproto/make-the-pds-your-own-customization-and-metrics-at-protocol-notes.md); [atproto#3392 blobstore quotas (notes)](../../raw/atproto/bluesky-social-atproto-3392-add-restrictions-on-blobstore-notes.md); [discussion 1740 blob size (notes)](../../raw/atproto/consider-raising-the-size-limit-of-blobs-bluesky-social-notes.md); [discussion 4832 image limit increase (notes)](../../raw/atproto/increasing-bluesky-post-image-size-limit-bluesky-social-notes.md)
> Updated: 2026-10-23

## Overview

Blobs are files stored next to an account's repo and referenced from records by CID. Their size limits come from three independent layers:

1. **Per-PDS server policy.** The reference PDS's default upload maximum is now 300M (`PDS_BLOB_UPLOAD_LIMIT=314572800`).
2. **Per-Lexicon `maxSize`.** Bluesky image embeds had a 1 MByte limit, being raised to 2 MByte.
3. **App and CDN processing.**

Lexicon size limits are effectively frozen once published, so the 2026 image-limit increase was a breaking change made knowingly. Account-wide storage quotas are not standardised. Session transcripts and attachments that exceed the ~1 MiB record ceiling ([ATProto Repository, Records and Lexicon](repository-and-records.md)) go into blobs. A session Lexicon should therefore choose blob `maxSize` carefully, and clients should read the PDS's advertised `blobUploadLimit`.

## Blob lifecycle (spec)

- Upload with `com.atproto.repo.uploadBlob` *before* creating the referencing record. The PDS can only apply generic limits at upload, because it does not yet know the Lexicon. Lexicon limits are enforced when the record is created.
- Uploaded blobs sit in temporary storage until a record references them. The spec recommends allowing several hours of grace before garbage collection, with one hour as a firm lower bound.
- A blob is deleted when no remaining record in the repo references it. Account deletion deletes all blobs. Deactivated or suspended accounts' blobs should not be publicly accessible.
- The blessed CID is CIDv1, `raw` codec, sha-256. Fetch with `com.atproto.sync.getBlob`. Serving blobs directly to browsers is not a recommended pattern, and if a PDS does serve them, a strict CSP (`default-src 'none'; sandbox`) is effectively mandatory.
- Security: the spec warns about EXIF-style metadata leakage and about parsing media without sandboxing. It recommends rate limits, size limits and quotas against resource exhaustion.

## Limits in practice

- **Reference PDS.**
  - The default maximum blob size was raised to 300M, mainly for longer videos.
  - Existing installs must set `PDS_BLOB_UPLOAD_LIMIT=314572800` themselves.
  - `com.atproto.server.describeServer` now advertises `blobUploadLimit`, so clients can split or reject uploads.
- **No account-wide quota** (atproto#3392, open). The reference PDS caps individual blob size but has no cap on the total storage an account consumes. The issue proposes windowed caps for cost control.
- **Lexicon `maxSize` as a social contract** (discussion 1740, from Oct 12, 2023):
  - The image embed limit of one million bytes is declared in `lexicons/app/bsky/embed/images.json`.
  - bnewbold explained that such values cannot be changed in place.
  - snarfed questioned whether any service actually enforces it.
- **The 2026 increase** (discussion 4832, Apr 7, 2026):
  - bnewbold announced raising `app.bsky.embed.images` from 1 MByte to 2 MByte, and accepting dimensions up to 4000 by 4000 pixels.
  - He acknowledged the change technically breaks Lexicon evolution rules, called it a bad precedent, and floated a schema flag marking `maxSize` as soft or hard.
  - He reaffirmed the 300 character post limit as a medium-defining constraint.
  - The last comment on discussion 1740 (Aug 9, 2026) links the commit raising the limit to 2mb.

> **Status: Outdated** (2026-10-23)
> The 1 MByte `app.bsky.embed.images` limit discussed from 2023 onward in discussion 1740 was being raised to 2 MByte, as announced in discussion 4832 (April 2026) and confirmed by the commit linked in 1740's final comment. Lexicon `maxSize` values are not as permanent in practice as the evolution rules state.

## Design implications for session data

- Large tool outputs, diffs and logs should be blobs referenced from entry records. Compressed transcript chunks are another option.
- Check `blobUploadLimit` before uploading, and split content across multiple blobs where needed.
- Decide early whether the session Lexicon's blob `maxSize` is a hard contract. The 2026 discussion shows that loosening it later is contentious.
- Expect self-hosted PDS operators to care about per-account storage, since no protocol quota exists.
- Remember blobs are public on a public repo. Space blobs are fetched with credentials ([ATProto Spaces (Permissioned Data)](atproto-spaces-permissioned-data.md)).

## See Also

- [ATProto Repository, Records and Lexicon](repository-and-records.md)
- [ATProto Spaces (Permissioned Data)](atproto-spaces-permissioned-data.md)
- [ATProto PDS Operation and Observability](pds-operation.md)
