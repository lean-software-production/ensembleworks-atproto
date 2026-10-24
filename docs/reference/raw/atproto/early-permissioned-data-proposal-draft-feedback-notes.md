# Early permissioned data proposal draft feedback (source notes)

> Source: https://discourse.atmosphere.community/t/early-permissioned-data-proposal-draft-feedback/923
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-03 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: terms-of-service — Discourse forum user content; no open license stated. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/discourse-atmosphere-community-e562ab1e/001.md.
> Work: https://discourse.atmosphere.community/t/early-permissioned-data-proposal-draft-feedback/923
> Quotations: 13 characters verbatim in this file; 13 of 90 allowed for this work across the knowledge base.

## About this source

A Discourse thread on the Atmosphere community forum (discourse.atmosphere.community, topic 923) titled Early permissioned data proposal draft feedback. It was opened by @dholms.xyz in June 2026 and has 15 posts retrieved. It collects community reaction to the draft permissioned data proposal in bluesky-social/proposals PR 94. Forum user content under the forum terms; these notes are a digest and attribute opinions to posters.

## Key facts

- Post 1 (dholms) frames the thread as feedback for the early proposal and points to PR 94 and the implementation branch, atproto PR 5187, noting the implementation is WIP.
- Post 2 (bmann.ca) pastes an excerpt of the proposal as it stood, titled 0016 Permissioned Data and described as a draft, not the final specification. Points from that excerpt: public atproto is for public broadcast; the permissioned protocol targets non-public data with an access perimeter, with listed modalities of personal data, gated content, socially shared content and groups. It is described as a distinct protocol with its own repository format, sync mechanism, addressing scheme and resolution path.
- The excerpt states the protocol provides access control, not confidentiality, and is not end-to-end encrypted; services can read data they handle, so search, indexing, notifications, aggregation and moderation remain possible. E2EE is out of scope.
- Comparison table in the excerpt: permissioned repos are one per (user, space); commit is an LtHash set-hash digest instead of a Merkle Search Tree root; signatures are deniable on rebroadcast; addressing uses `ats://` instead of `at://`; access is gated by a space credential.
- Terminology in the excerpt: space (identified by an authority, type and `skey` triple), permissioned repo, repo host, space host, space authority, space credential, delegation token, client attestation, syncer. A PDS can fill both repo host and space host roles.
- Address form: `ats://{spaceDid}/{spaceType}/{skey}/{authorDid}/{collection}/{rkey}`; the first three components alone reference a space.
- The authority DID document must expose a verification method with id `#atproto_space` and a service entry with id `#atproto_space_host`. The space type is an NSID and is also the OAuth consent boundary.
- Post 3 (tamme.schichler.de) praises the design as user-safe and not leaking attestations, values the `simplespace` requirement for PDSs, and spots a typo ("unlike" for "usually") that dholms confirms in post 4. Dholms also confirms `listMembers` is private to the space authority, unless members are expressed as records in the space.
- Post 6 (baldemo.to) argues the word space misnames a permissioning boundary and suggests Permission Space as canonical, with shorthand Space; erlend.sh opened a sidebar topic on terminology; holobrine.bsky.social agrees that naming matters. (The proposal was later renamed to atproto spaces, per other sources.)
- Post 9 and 10 (holobrine.bsky.social): access control is stateful and data driven; the space owner's PDS is a single point of failure because it must keep delivering tokens or credentials expire. Post 11 (zicklag.dev) replies that redundancy can be built with ordinary web techniques and that checks can be stateless, for example gating on a call to a third-party API like GitHub.
- Post 13 (dholms): lexicons work the same for public and permissioned data; expects 3 layers for communities, namely the protocol, a cross-app community governance and structure standard, and application lexicons.
- Post 14 (bnewbold.net) lists high-level review notes: mixed feelings about the design process; nothing is set until multiple interoperating implementations and a real app exist; app services holding multiple space credentials from multiple accounts feels weird; centralizing forces differ from public data; needs a careful security and privacy review; moderation and anti-abuse is not fleshed out (possible space blob pre-scanning at the PDS, labeler relationships, moderator access, rate limits and quotas).
- Same post lists design goals: scales to millions of readers; personal data across devices and apps; authority rooted in the DID rather than PDS hostname; newly authorized services can backfill an entire space, seen as critical for credible exit; multiple concurrent client apps with the authority able to limit them; migration of spaces between hosts; bulk export and PDS migration of an account's permissioned data; leaked data is refutable rather than strongly authenticated at rest.
- Post 15 (j12t.org) asks what happens when a user leaves a space and what the app view must do.
- Post 16 (gui.do, who builds Sifa) raises GDPR-oriented gaps: aggregators that read via a space credential hold copies and become processors; no fetch-on-demand reader mode (`read_self` is own-repo only); members cannot see who else can read; expiry is not erasure (credentials are short-lived with a default of 2 hours) and the only affirmative purge signal is whole-space `notifySpaceDeleted`, delivered best effort; per-record or per-member eviction with delivery confirmation is requested; network-wide labelers and sybil detection cannot see signals that move into spaces. The poster notes they are not a lawyer.

## Relevance to session sharing

- Access control rather than confidentiality, plus app-held copies and weak erasure, are the main privacy caveats for putting private coding-session transcripts in spaces.

## Related

- bluesky-social/proposals#94, atproto PR 5187, Permissioned Data Diaries Leaflet posts, Arbiter and group-standards threads on the same forum.
