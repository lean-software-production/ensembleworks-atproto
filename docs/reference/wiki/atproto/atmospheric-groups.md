# Atmospheric Groups

> Sources: atproto.com "An Intro to Atmospheric Groups" (Bluesky Social PBC and Contributors, CC-BY), undated; Brittany Ellich, "Representing groups in ATProto" (page dated Dec 21, 2025; notes only); Atmosphere Discourse topics 745 (group standards WG) and 750 (Arbiter) (notes only); all collected 2026-10-23; source inventory: An Intro to Atmospheric Groups - AT Protocol (Bluesky Social PBC and Contributors, AT Protocol website; Unknown); Representing groups in ATProto (source notes) (attributed source notes; Unknown); [Proposal] WG for group/community standards and infrastructure in ATProto (source notes) (attributed source notes; Unknown); Arbiter: Group management for Permissioned Spaces (source notes) (attributed source notes; Unknown)
> Raw: [atproto.com groups intro](../../raw/atproto/an-intro-to-atmospheric-groups-at-protocol.md); [Brittany Ellich on groups (notes)](../../raw/atproto/representing-groups-in-atproto-notes.md); [Discourse 745 group standards WG (notes)](../../raw/atproto/proposal-wg-for-group-community-standards-and-notes.md); [Discourse 750 Arbiter (notes)](../../raw/atproto/arbiter-group-management-for-permissioned-spaces-notes.md)
> Updated: 2026-10-23

## Overview

The community opensocial.group proposal defines a group in one line: "An atmospheric group is a DID with a bunch of permissioned spaces under it." (atproto.com, CC-BY). The group has its own DID, so no member's account owns it, and it can migrate between hosts like any account. It can also be reused across applications, which means a team created in one app is the same team in another. Groups sit on top of [ATProto Spaces](atproto-spaces-permissioned-data.md), so they inherit that layer's alpha status and its access-control-not-encryption property. For this project, a group is the natural unit for a team: a team activity feed and per-team sharing of coding sessions can hang off one group DID with its members and roles.

## Structure (opensocial.group, as described by atproto.com)

- **Spaces under the group DID**
  - A `meta` space holds the group's profile and rules. Many groups will make it publicly readable.
  - A `members` space holds the member list, roles and an index of the group's other spaces. Grain's example writes it as `fyi.opensocial.members`, an early revision of opensocial.group.
  - Every app or modality adds its own space under the same DID. Grain uses `social.grain.group`. An events app, or a coding-session app, could add another and reuse the same members and roles.
- **Two-way membership**: the group writes a `membership` record granting roles, and the member writes an `acceptance` record in the same space.
- **Permissions are flat RBAC**. Each space has an `access` record listing which roles can read, and the group host enforces it when issuing space credentials. Write rules are left to each app's own Lexicons, which can refer to the group's roles.
- **Acting as the group**: the group host is an OAuth authorization server for the group DID. An admin signs in with their own account and gets a credential scoped to their roles, so nobody shares the group account's password. This matters for records that must come from the group itself, such as a pinned post.
- **Writer set**: a space's writers are the accounts whose repos hold data in it. Apps ask the group host which repos exist and sync each one directly from its PDS. The post's example is that a group with a thousand active members is a thousand space repos across members' PDSes. The host tracks repos and routes notifications but does not hold members' records.
- **Availability**: the post's demo needs a spaces-enabled PDS account. Grain is the featured app, and pdsls can browse space records after an OAuth grant that includes Spaces permissions.

## Other group designs in the ecosystem

- **opensocial.community** is Brittany Ellich's earlier design sketch, dated Dec 21, 2025. It describes a separate group-management service whose groups are DIDs such as `did:web:overcommitted.opensocial.community`. AppViews authenticate with service-auth JWTs and may write only records in their own namespace. Membership records live in the user's repo and are discovered through backlinks. Any user could join any group in the initial design. Private groups were a roadmap item.
- **Arbiter** (Zicklag, Muni Town / Roomy; Discourse 750 and 745) is a space host that computes member lists for many spaces within a community boundary. It has a built-in `$admin` space, roles that are themselves spaces (nesting for subgroups), remote arbiters as members for federation, and policy experiments with Rego / Open Policy Agent for custom governance. Draft lexicons live under `town.muni.arbiter`. Read access follows member lists, and write rules are left to AppViews.
- The **working-group proposal** (Discourse 745) catalogues parallel efforts and proposes phased standardisation, starting with a shared ontology and membership primitives. The efforts include Bluesky's spec, Blacksky, Northsky's Stratos, Roomy/Leaf, opensocial.community, Hypercerts' certified-group-service, Habitat and Roundabout. dholms (post 14) said Bluesky would work on a community feature for its app and wants those communities to be interoperable.

> **Status: Disputed**
> These designs disagree on where group membership lives. opensocial.group keeps membership/acceptance records in a `members` space under the group DID, with the group host enforcing read roles. Brittany Ellich's sketch keeps membership records in the user's own public repo and discovers them via backlinks. Arbiter computes member lists centrally in the space host, using a role tree. No single standard had won at collection time, and Discourse 745's stated goal is convergence after divergence.

## Implications for team session sharing

- Model a team as a group DID. The session-sharing app adds its own space type under it, for example a sessions space, and reuses the group's roles for read access.
- Because write rules belong to app Lexicons, the app must define who may append replies to a session.
- Prefer the opensocial.group structure while it remains the one featured by atproto.com. Keep the membership layer swappable until the standards settle.

## See Also

- [ATProto Spaces (Permissioned Data)](atproto-spaces-permissioned-data.md)
- [ATProto OAuth and Permissions](oauth-and-permissions.md)
