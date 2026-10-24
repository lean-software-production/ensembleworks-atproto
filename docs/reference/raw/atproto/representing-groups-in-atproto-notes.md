# Representing groups in ATProto (source notes)

> Source: https://brittanyellich.com/atproto-groups/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-03 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — no license statement found in archived page. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/brittanyellich-com-f3973d91/001.md.
> Work: https://brittanyellich.com/atproto-groups
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A proposal-style blog post by Brittany Ellich titled Representing groups in ATProto, dated Dec 21, 2025 on the page and about 9 minutes to read. It describes a planned design for a group-management service, opensocial.community, motivated by adding book clubs to her media-tracking app Collective. It is a design sketch from an individual developer, not a standard, and she invites feedback. License: all rights reserved (no license statement found).

## Key facts

- Motivation: ATProto has no standard way yet to handle shared group resources; the author wants a shared book-club list in Collective and runs a technical book club for Overcommitted.
- Plan: a separate service, opensocial.community, manages groups independently of any single app, so one group could be reused by several apps and could migrate between providers.
- Group handles would be subdomains, for example `overcommitted.opensocial.community`.
- Definitions used: an AppView is an app that views the ATmosphere (Bluesky and Collective are both examples); a Group is a shared resource DID that can be owned by multiple people and have members, and group resources live in its repository.
- AppView registration: the service authenticates AppViews with service authentication tokens (signed JWTs) for searching, creating groups and managing group-specific records; group creation also uses an API key. Creating a group adds the creating user as first admin and the creating AppView as first group app.
- Namespace rule: each AppView may create, update and delete only records in its own namespace, for example `app.collectivesocial.feed.list` for the group, and cannot touch another AppView's records such as `app.other.feed.post`.
- Storage: the author plans a PDS for opensocial.community to hold group metadata and AppView data, initially self-hosted, and considers letting groups migrate to self-hosted PDSs or other providers. She also wants to support managing a group created on a different PDS but has not worked that out.
- Administration: admins can list groups they administer, add other admins, update metadata (name, description, icon) and approve other AppViews requesting access to a group.
- Moderation: the author is unsure but suggests a list of labelers approved by group admins to show or hide data.
- Membership: membership records live in the user's own repo with a hard reference to the group; the group learns members through backlinks to its DID. Any user can join any group in the initial design; users sign in with OAuth.
- Example flow: creating the Overcommitted Book Club gives the group DID `did:web:overcommitted.opensocial.community`, with the author as first admin, Collective as approved AppView, and a shared list under `app.collectivesocial.feed.list` in the group repo.
- Roadmap ideas: registering existing groups from another PDS with a concept mapping, easy migration to another group-management app, and private groups or groups needing admin approval.
- The author asks specifically for feedback on the authentication model (service-to-service signed JWTs).
- Links collected: a Frontpage groups discussion, Meri's Missives summary of group work, a Bonfire Networks post on groups in the Fediverse, a Discourse thread on representing groups and shared resources in atproto, and a post by Bryan Newbold.

## Related

- Group and community work in the atproto ecosystem, permissioned spaces, service auth JWTs, Collective, opensocial.community.
