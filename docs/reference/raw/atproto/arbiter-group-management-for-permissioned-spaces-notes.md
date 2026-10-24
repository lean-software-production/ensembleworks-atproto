# Arbiter: Group management for Permissioned Spaces (source notes)

> Source: https://discourse.atmosphere.community/t/arbiter-group-management-for-permissioned-spaces/750
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-03 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: terms-of-service — Discourse forum user content; no open license stated. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/discourse-atmosphere-community-afacef81/001.md.
> Work: https://discourse.atmosphere.community/t/arbiter-group-management-for-permissioned-spaces/750
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A Discourse thread on discourse.atmosphere.community (topic 750) titled Arbiter: Group management for Permissioned Spaces, started in April 2026 by @erlend.sh and continued through early September 2026, with 11 posts retrieved. Most posts are link roundups to Leaflet posts and a simulator by @zicklag.dev (Muni Town / Roomy team), with a few longer design posts by Zicklag. Forum user content; these notes are a digest and attribute design claims to the posters.

## Key facts

- Post 1 shares a post by Meri that evaluates permissioned spaces for community contexts, after closer study of the Permissioned Data Diaries by dholms.
- Post 2 shares the first Arbiter writeup: the permissioned data proposal has a membership concept but leaves orchestration to the app, and the arbiter is intended as a general-purpose interoperable group membership service for ATProto, motivated by the next ATProto-native iteration of Roomy.
- Post 3 relays planned additions: a special `$publish` space for writing public records under the arbiter's DID, a note that sync can go either way, adopting an existing DID, and a `$labeler` role. It points to flo-bit's contrail project, whose docs describe communities as group-controlled DIDs in minted or adopted modes, and spaces as an auth-gated store identified by an `ats://` URI with one owner DID, one type and one key, where every member can read and write but delete is scoped to your own records.
- Post 4 shares Arbiter Progress Report 1 and a browser simulator that the author says runs the actual arbiter core state machine compiled to WASM.
- Post 7 (Zicklag): after talking to the Habitat and Acorn teams, Zicklag argues some apps need custom policies, such as democratic governance, and proposes an intermediate shared representation of group membership as a tree of roles, separating who is who from what you can do. Open Policy Agent is considered to guard updates to the role tree.
- Post 8 (Zicklag): draft lexicons under `town.muni.arbiter`, using open unions for arbiter, space and member configuration, with spaces able to be members of other spaces for subgroups and role trees. Arbiter servers may implement custom authentication mechanisms.
- Post 9 mentions the group-standards working group thread and says the next implementation would be an alternative to opensocial.community with advanced policy support, acting as a space host for permissioned data.
- Posts 5, 6 and 10 are scheduling chat about a public discussion session on stream.
- Post 11 (September 2026) links Arbiter Progress Report 4, about using permission sets to create virtual custom scopes for the arbiter, and ties it to another thread about sketching `com.atproto.server.createActorAuth`.

## Relevance to session sharing

- Group membership layered over permissioned spaces (roles, nested spaces, remote arbiters) is one possible design for sharing sessions with a team.

## Related

- Representing groups in ATProto by Brittany Ellich, the group-standards working group proposal thread, Habitat, Roomy, contrail, Open Policy Agent.
