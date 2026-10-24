# Data Validation - AT Protocol (source notes)

> Source: https://atproto.com/guides/data-validation
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-04 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — Footer: "Copyright (CC-BY) Bluesky Social PBC 2026. All rights reserved." - unversioned CC-BY, ambiguous, treated conservatively. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/atproto-com-39b44f38/001.md.
> Work: https://atproto.com/guides/data-validation
> Quotations: 15 characters verbatim in this file; 15 of 90 allowed for this work across the knowledge base.

## About this source

The atproto.com guide "Data Validation", from the AT Protocol project site (Bluesky Social PBC). No explicit publication date in the content; it mentions August 2025 as a reference point. The guide itself states its limits are informal guidelines, not part of the atproto specification, and likely to evolve.

## Key facts

- Audience: client apps and bots can usually assume API data is valid and rely on the PDS to check schemas on record creation; software consuming the firehose (feed generators, AppViews, moderation services) should be more careful.
- Failure handling: an invalid individual record should be ignored while other records from the same repository are processed. A problem with commit data or the MST marks the repository invalid, without purging old content; a later valid commit restores it to valid.
- Recommended limits (informal), with the constant names given:
  - `MAX_CBOR_RECORD_SIZE`: 1 MiByte, 1,048,576 bytes; keep typical records to a few dozen KBytes and use blobs for more data.
  - As of August 2025 the `subscribeRepos` Lexicon limits `#commit` block size to 2,000,000 bytes, so only one 1 MiByte record fits per commit.
  - Firehose frames can hold multiple records; CBOR parsing limits of 4-5 MBytes are suggested.
  - `MAX_JSON_RECORD_SIZE`: 2 MiByte, 2,097,152 bytes.
  - String length: measured in UTF-8 bytes, tens of KBytes at most; `MAX_RECORD_STRING_LEN` can rely on the record size limit. Some early implementations had an 8 KByte, 8192-byte limit.
  - `MAX_RECORD_BYTES_LEN` follows the same approach for binary data.
  - `MAX_CID_BYTES`: 100 bytes.
  - `MAX_CBOR_NESTED_LEVELS`: 32 levels.
  - `MAX_CBOR_CONTAINER_LEN`: 128 x 1024 = 131,072 elements.
  - `MAX_CBOR_OBJECT_KEY_LEN`: 8 KByte (8192).
  - Integers should be 64-bit float safe (53 bits): `MAX_SAFE_INTEGER: 9007199254740991`, `MIN_SAFE_INTEGER: -9007199254740991`.
- Validation without a schema, by type: strings must be valid UTF-8 with no required normalization; `bytes` may be empty; `cid-link` must be CIDv1 with multicodec `dag-cbor` (`0x71`) or `raw` (`0x55`), SHA-256 encouraged; arrays may be heterogeneous; object keys must be non-empty strings and keys starting with `$` are reserved (for example `$bytes`, `$type`).
- Blob rules: `ref` must be a valid `cid-link` with `raw` multicodec; `size` not negative; `mimeType` not empty; the legacy blob format should be readable but new records must use the regular blob format.
- Relevance: large session transcripts as records would hit the per-record limits; the guide recommends blobs for bulk data, and consumers should tolerate invalid records.

## Related

- atproto data model and Lexicon specs, `subscribeRepos` firehose.
