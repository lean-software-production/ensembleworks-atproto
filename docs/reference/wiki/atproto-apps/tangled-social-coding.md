# Tangled: Social Coding on ATProto

> Sources: Tangled team, "Introducing Tangled" (blog.tangled.org; notes only), undated; tangled.org landing page (notes only); Hacker News item 45543899 discussion (notes only); qjoly/mise-tangled README (MIT); all collected 2026-10-23; source inventory: Introducing Tangled (source notes) (attributed source notes; Unknown); Tangled · The next-generation social coding platform (source notes) (attributed source notes; Unknown); Tangled, a Git collaboration platform built on atproto (source notes) (attributed source notes; Unknown); qjoly/mise-tangled (Copyright (c) 2026 qjoly; qjoly/mise-tangled; Unknown)
> Raw: [Introducing Tangled (notes)](../../raw/atproto-apps/introducing-tangled-notes.md); [tangled.org landing page (notes)](../../raw/atproto-apps/tangled-the-next-generation-social-coding-platform-notes.md); [HN discussion of Tangled (notes)](../../raw/atproto-apps/tangled-a-git-collaboration-platform-built-on-atproto-notes.md); [qjoly/mise-tangled](../../raw/atproto-apps/qjoly-mise-tangled.md)
> Updated: 2026-10-24

## Overview

Tangled is relevant prior art for social coding over ATProto. It is a Git collaboration platform that keeps **Git data off-protocol**, on self-hostable servers called **knots**. Forge data around the code, such as repos, issues, public keys and release artifacts, lives on-protocol as Lexicon records (`sh.tangled.*`) in users' PDSes. A central **AppView** at tangled.org aggregates across knots. The split is instructive for agent sessions. Bulky or specialised data, such as git objects or very large traces, can live on purpose-built servers. The social layer (who shared what, comments, stars, follows) lives in records that any app can read. Users bring an existing ATProto (for example Bluesky) account.

## Architecture

- **Knots** are lightweight headless git hosts. They can be single- or multi-tenant, small enough for a Raspberry Pi, or large community servers. Tangled also runs managed knots. Co-founder icy (in the HN thread) says knots serve git over an XRPC API, with sqlite plus bare repos on disk. Repos are not replicated into the PDS. icy describes knots as an extension to the AT architecture for off-protocol data.
- **Spindles** run CI on your own machines. The landing page describes NixOS-powered microVMs.
- **AppView** (tangled.org): a consolidated view across knots, through which users access, clone and contribute.
- **Records** that commenters observed include `sh.tangled.repo`, `sh.tangled.repo.issue` and `sh.tangled.publicKey`. Release artifacts are `sh.tangled.repo.artifact` records in the uploader's PDS, with the binary stored as an atproto blob (mise-tangled README, MIT). mise-tangled resolves a tag to its artifact, a working example of a third-party tool consuming another app's records and blobs.
- **Features** advertised on the landing page: stacked pull requests with native Jujutsu support, a web-of-trust vouching feature, and federated contribution (PRs or bug reports to any repo on any server).

## Status and limits

- Launch was invite-only, onboarding through IRC (`#tangled` on libera.chat), and later opened to the public. The team described the platform as in its infancy and dogfooding.
- Private and enterprise repositories were not really supported, per an HN commenter linking Tangled core issue 60. icy said an airgapped non-AT version had been discussed but was not coming soon. Private Tangled repos would plausibly depend on [ATProto Spaces (Permissioned Data)](../atproto/atproto-spaces-permissioned-data.md). An HN commenter on the spaces thread expected private repos soon, but that is an expectation, not a sourced fact.
- HN concerns (opinions): moderation and spam on open PDS hosting, who pays for hosting, and whether atproto adds anything for git.

## Lessons for agent-session sharing

- Put the *social* objects (session announcements, replies, reactions, team feed items) in Lexicon records. Keep heavy payloads in blobs, or in a dedicated service the records point to.
- A purpose-built server, like a knot, could host large session archives or run sandboxed remote execution while identity and permissions stay on ATProto. That would place remote execution outside the PDS.
- The landing page's activity feed showed repositories named `tangled-for-agents` and `hermes-recall`. That points to agent-related experimentation in the Tangled ecosystem, but the page gave no details.

## See Also

- [ATProto Repository, Records and Lexicon](../atproto/repository-and-records.md)
- [ATProto Blobs and Size Limits](../atproto/blobs-and-size-limits.md)
- [ATProto Spaces (Permissioned Data)](../atproto/atproto-spaces-permissioned-data.md)

## Release artifact distribution through mise

The qjoly/mise-tangled plugin demonstrates a distribution path beyond Git hosting: it resolves Tangled releases for mise and installs matching artifacts. Its README requires annotated tags because artifacts reference tag objects, and notes that prereleases need explicit selection. It requires local git and a checksum tool and does not support Windows in the captured snapshot. These are plugin constraints, not general ATProto repository limits.

## Discussion evidence on hosting boundaries

In the Hacker News discussion, Tangled co-founder icy explains that knots serve Git repositories and keep bare repositories plus SQLite state that can be moved together. Git contents are not replicated into the PDS; forge records surround that separate storage. Other comments raise moderation, private-use and operating-cost concerns. Those comments are attributed perspectives, not measurements or guarantees that the public forge supports private collaboration.

## Launch architecture and rollout state

The Tangled team describes lightweight headless knots hosting Git repositories, managed hosting and a consolidated App View across knots. Developer data ownership and accessible participation are design goals, not measured outcomes. The launch text’s invite-only rollout is followed by an update opening public access.

> **Status: Outdated** (2026-10-24)
> Invite-only onboarding describes the initial launch. The same source explicitly updates access to public login; do not treat the launch restriction as the captured current state.

## Current landing-page claims and evidential scope

The landing page advertises native Jujutsu stacking, self-hosted knots and spindles, and NixOS microVM CI. Its web-of-trust vouching is a social signal, not proof that an artifact was human-written or secure. Agent-related repository names in the live feed do not establish their functionality. Use the page to identify advertised capabilities while keeping implementation and trust claims grounded in technical sources.

## Related compiled concepts

- [ATProto Curation and Discovery](curation-and-discovery.md)
