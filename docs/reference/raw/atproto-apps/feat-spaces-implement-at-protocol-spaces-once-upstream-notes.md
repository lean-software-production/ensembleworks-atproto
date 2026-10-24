# feat(spaces): implement AT Protocol Spaces once upstream stabilises (source notes)

> Source: https://github.com/ewanc26/wolfram/issues/35
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-03 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue user content. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-47a47b9a/001.md.
> Work: ewanc26/wolfram#35
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

GitHub issue ewanc26/wolfram#35, titled feat(spaces): implement AT Protocol Spaces once upstream stabilises. Opened 2026-09-16 by @ewanc26, labels enhancement and area: atproto, open at fetch time with 2 comments. Wolfram is a C23 core with C++23 wrapper atproto SDK per the issue text. GitHub user content; this is a digest.

## Key facts

- Purpose: a deferred tracking issue to support AT Protocol Spaces once upstream is stable enough to avoid experimental schema and API churn.
- Upstream status as of 2026-09-16, per the issue: Spaces is an alpha feature; the public alpha was announced on 2026-08-20; breaking changes are expected, production use is discouraged, the database schema may change destructively, and no careful security review has been done.
- Design elements listed: `com.atproto.space.*` APIs, permissioned repositories, space authorities, space credentials with DPoP, per-space sync, membership and access policies, and non-public blobs. The issue stresses this is access control, not end-to-end encryption, so authorised participants can read the data.
- A 2026-09-10 alpha update had breaking changes: splitting `simplespace.policy` into `readPolicy` and `writePolicy`, renaming `addMember` to `putMember`, separating read and write membership permissions, API changes in `@atproto/space`, CAR APIs moved into `@atproto/car`, and `atUri.spaceRef()` replaced by `SpaceRef.for()`.
- Gate conditions before real implementation include: no longer documented as alpha, proposal settled into stable lexicon semantics, reference implementation on the normal path rather than a draft PR, stable lexicons and credential flows, clear interoperability for sync, membership, permissions and blobs, and migration guidance for SDK authors.
- Allowed before the gate: research and disposable prototypes, such as testing space credentials and DPoP against the alpha PDS and validating CAR and per-space sync assumptions.
- A mismatch between the proposal and alpha API around repo-host notification registration is reported at atproto issue 5491.
- Comment 2026-09-20: still deferred. Comment 2026-09-30: the proposal was renamed from permissioned data to atproto spaces on 2026-09-28, and gained a new `space-ref` lexicon string format on 2026-09-29; simplespace write access had changed on 2026-09-10.
- Acceptance criteria are a checklist covering C23 API coverage tests, thin C++23 wrappers, predictable rejection of malformed data, access-control tests, and interoperability verification.

## Related

- Spaces alpha announcement at atproto.com, proposals 0016, atproto PR 5187, the Spaces alpha updates thread on the Atmosphere community Discourse, the downstream consumer `atperson`.
