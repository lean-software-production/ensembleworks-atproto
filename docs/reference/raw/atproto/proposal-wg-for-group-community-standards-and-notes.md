# [Proposal] WG for group/community standards and infrastructure in ATProto (source notes)

> Source: https://discourse.atmosphere.community/t/proposal-wg-for-group-community-standards-and-infrastructure-in-atproto/745
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-03 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: terms-of-service — Discourse forum user content; no open license stated. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/discourse-atmosphere-community-94a67efd/001.md.
> Work: https://discourse.atmosphere.community/t/proposal-wg-for-group-community-standards-and-infrastructure-in-atproto/745
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A Discourse thread on discourse.atmosphere.community (topic 745) titled Proposal: WG for group/community standards and infrastructure in ATProto. Opened in April 2026 by @baldemo.to; 24 posts retrieved, running through June 2026. It proposes a working group to align the many independent group and community designs in ATProto and then collects who is building what. Forum user content; these notes are a digest and attribute positions to posters.

## Key facts

- Post 1 (baldemo.to): many teams are making foundational decisions about group membership, governance and infrastructure; without coordination a de facto standard could calcify from momentum. It lists efforts including Bluesky's permissioned data spec, Blacksky, Northsky's Stratos, Roomy with its Leaf server, opensocial.community by Brittany Ellich, an implementation model by ngerakines, writing by bnewbold, Frontpage, and Composable Trust.
- Proposed work areas: community identity and discovery, membership, data and social spaces, governance and authority, app mediation and UX, topology and composability.
- Proposed phasing: phase 1 shared ontology and community archetypes; phase 2 membership and identity primitives; phase 3 governance, spaces and composability. Also proposed domain representatives, principles (enable, don't prescribe; safety and resilience as first-class constraints; assume adversarial conditions) and minimum viable standardization.
- Post 2 (bnewbold.net) is interested but short on energy for consensus-building; mentions Fediverse group work and Metagov.
- Post 8 (offline.arushibandi.com): Habitat is building community infrastructure with private data, communities keeping member-written data when members leave, a fully self-hostable stack, and eventual federation.
- Post 12 (bmann.ca): the forum can provide a Discourse group and category; suggests a scope, at least two organizers, and commitments from two app codebases to implement.
- Post 13 (holke.xyz): Hypercerts built certified-group-service, which represents groups as standard atproto repos on a normal PDS with RBAC added by a service layer.
- Post 14 (dholms.xyz): Bluesky is going to work on a community feature for the app in the coming months and wants those communities to be interoperable; suggests something like standard.site schemas for open communities.
- Post 15 (erlend.sh): Roomy extends the permissioned data spec while the other efforts, apart from contrail, are separate implementations; the stated end goal is convergence after divergence.
- Post 16 (zicklag.dev): summary of the arbiter. Permissioned spaces give a flat membership list; the arbiter is a space host that computes member lists for multiple spaces within a community boundary. It has a built-in `$admin` space, roles that are themselves spaces, Owner and Member access, and remote arbiter spaces as members for federation. Read access follows member lists, while write and other access control is left to AppViews. A Quint specification exists and a Rust server is hoped for.
- Post 19 (baldemo.to): a Tangled repo for the working group, with a project documentation template at `resources/PROJECT-TEMPLATE.md` and a list of ten projects to document, including Permissioned Data, Blacksky, Stratos, Leaf, Open Social, Habitat, lore.farm, rpg.actor, Composable Trust and Mezzanine.
- Post 20 (essentialrandom.bsky.social): interested in shared content, membership mechanisms, permissions and attestations as concrete building blocks.
- Post 22 (zicklag.dev): the arbiter now has generic group lexicons with open unions for 3 kinds of configuration and a prototype using Rego policies, preserving an 8-access-level system as one policy; policies could enable voting-based changes; community repos with policy-controlled writes are also considered.
- Post 23: a proposal to standardize attestations as the first working group output.
- Post 24 (blaine.bsky.social): Roundabout runs private full atproto stacks per community to manage private-data issues and is keen to collaborate.

## Related

- Representing groups in ATProto, Arbiter thread, permissioned data proposal feedback thread, standard.site, lexicon.community.
