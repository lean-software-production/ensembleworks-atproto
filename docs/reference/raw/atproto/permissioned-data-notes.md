# Permissioned data (source notes)

> Source: https://github.com/bluesky-social/proposals/pull/94
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-03 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub PR user content. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-8bd3b1d8/001.md.
> Work: bluesky-social/proposals#94
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

Pull request bluesky-social/proposals#94, titled Permissioned data, by @dholms. Created in late June 2026 and merged in early July 2026 per the API metadata, base main, two files changed (+634/-0): the new `0016-permissioned-data/README.md` (632 lines) and a README index change. Cached text holds the PR description, 47 reviews (mostly inline comments not captured, so most show no text) and 2 issue comments. GitHub user content; this is a digest. The proposal text itself lives in the merged file and is not in this source.

## Key facts

- The description calls it an initial proposal for permissioned data and warns that details, terminology and behaviors are all likely to change.
- It points to dholms's Leaflet posts for a friendly introduction, to the community forum thread for larger discussion, and to atproto PR 5187 as the implementation branch with draft lexicons; the implementation is described as WIP.
- Review by @matthieusieben (June 24): the `client_id` field in the space credential has two issues, that in small groups members could infer which user uses which app, and that some clients put sensitive data in query parameters such as loopback clients; the reviewer strongly recommends not sending it to the Repo Host through the credential.
- Review by @bnewbold (June 26): unclear how the space writer set is managed, for example the semantics of `listRepos`; suggests `simplespace` should address it; OAuth scope design is a lot and best reviewed by implementing; privacy, security and power dynamics need more thought; asks whether a PDS should help minimal clients call `com.atproto.space.getRecord` on remote hosts by fetching a space credential from the authority, noting added PDS complexity.
- Comment by @tunjid (June 26): asks how custom AppViews that aggregate firehose or tap data would sync spaces, since auth grants access on behalf of one user while useful data is the whole space; asks whether a wider access tier for moderators or aggregators is needed or should stay off protocol. Uses standard site recommendations and subscriptions as an example.
- Comment by @bnewbold (July 1): how space apps handle account status changes (deactivation, suspension, deletion) and identity events (migration, key updates); suggests account-state-specific error codes on space fetch endpoints; the notify mechanism is best effort rather than reliable retry delivery; asks whether apps must listen to the full firehose for `#account` and `#identity` events, presumably via an enhanced `tap` supporting space data.
- Other reviewers listed: @iameli, @ricci, @prohr, @LemmaEOF, @uniphil. @dholms posted many follow-up reviews in late June 2026.

## Related

- Early permissioned data proposal draft feedback thread on the Atmosphere community Discourse, proposals#115 rename to atproto spaces, atproto PR 5187, kodamachi#228.
