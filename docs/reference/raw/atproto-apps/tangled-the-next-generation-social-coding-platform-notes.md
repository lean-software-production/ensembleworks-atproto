# Tangled · The next-generation social coding platform (source notes)

> Source: https://tangled.org/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-12 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — No license statement found on page. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/tangled-org-c7d1e5af/001.md.
> Work: https://tangled.org/
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

The public landing page of Tangled, a social code-hosting platform built on the AT Protocol. It is marketing and community-feed material, not technical documentation. Much of the page is a live activity feed of accounts creating, following and starring repositories, which is volatile and not summarised here.

## Key facts

- Tangled describes itself as a next-generation social coding platform, aimed at developer ownership of code and community self-governance.
- Headline features on the page: stacked pull requests, a completely self-hostable setup, and microVM-based CI.
- Stacked pull requests: large features are split into small reviewable chunks with round-based code review, and the page says stacking is supported natively using Jujutsu.
- Self-hosting: repositories are hosted on your own infrastructure with knots, and CI runs on your own machines with spindles. Hosted instances are also offered.
- CI runs in NixOS-powered microVMs; containers can be built with Docker, services such as Postgres and Redis can be set up, and inputs are cached.
- A web-of-trust feature lets users vouch for collaborators, shown as a green shield, which the page presents as a way to tell real work from LLM spam.
- Built on AT Protocol: the page says it enables federated code collaboration, so pull requests or bug reports can be submitted to any repository on any server. Users can bring an existing AT Protocol account such as a Bluesky account.
- The project is open source with a monorepo at tangled.org/core, and contributions are welcomed.
- The activity feed shows ATProto-ecosystem projects, including a repository named `tangled-for-agents` and one named `hermes-recall`, suggesting agent-related work around Tangled; the page gives no details.
- A newsletter signup is offered, and the page points to the @tangled.org Bluesky account for updates.

## Related

- AT Protocol, Bluesky, knots and spindles documentation at docs.tangled.org.
- Jujutsu version control.
