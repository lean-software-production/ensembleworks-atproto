# Tangled, a Git collaboration platform built on atproto (source notes)

> Source: https://news.ycombinator.com/item?id=45543899
> Resolved: https://hn.algolia.com/api/v1/items/45543899
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-08 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: terms-of-service — Hacker News; user comments under site terms. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/news-ycombinator-com-fd9dbb91/001.md.
> Work: news.ycombinator.com/item?id=45543899
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A Hacker News discussion thread (submitted by the user mjbellantoni, 332 points) about the blog post titled Tangled, a Git collaboration platform built on atproto at blog.tangled.org/intro. Only the discussion is captured here, not the linked post. The thread is user commentary, mostly from 2025-10-11, and the claims in it are individual opinions. Several comments are from Tangled's co-founder using the handle icy, who is the most authoritative voice in the thread.

## Key facts

- Tangled is described in the thread as a code forge built on the AT Protocol, with data outside git stored as app-defined records.
- Commenters point to `sh.tangled.repo`, `sh.tangled.repo.issue` and `sh.tangled.publicKey` collections visible in the ufos.microcosm.blue lexicon browser as evidence of what lives in a user's PDS. One commenter's rough summary is that code lives in git while the surrounding forge data is lexicon records, and that some things are not yet in lexicons.
- danabramov explains lexicons as schemas for app-defined data types, comparable to table or collection names; there are lexicons for a Tangled repo, a Bluesky post and a Leaflet publication, defined and evolved by each application's developers.
- icy states that knots serve git repositories over an XRPC API; the state on disk is a sqlite database plus bare git repositories that can be tarballed and moved. Git repos are not replicated into the PDS; knots are described as an extension to the AT architecture for off-protocol data, namely git.
- Tangled components named by commenters: knot (git host), spindle (CI runner), appview. One commenter claims the appview runs on a single machine with about 4 cores and a few gigabytes of RAM; another says Tangled's appview is stateful and synchronises via NATS. These are commenter claims.
- Tangled has a CI pipeline feature; one commenter complains it looks like GitHub Actions in shape and wants DAG-style dependencies instead.
- Tangled supports stacked pull requests and Jujutsu (blog post on stacking cited), praised by several commenters.
- Private or enterprise use: a commenter links Tangled core issue 60 and says there is not really support; icy says an airgapped non-AT version has been discussed but is not soon.
- Mirroring: icy suggests running a knot on top of a local git server, or adding a push-only remote with `git remote set-url --add --push`; a spindle pipeline could push back to GitHub on merge.
- Moderation concerns raised: spam, illegal content and arbitrary PDS hosting; replies note atproto labelers and curation via subscription to the firehose. One commenter says the jury is out on how well labelers scale.
- Cost debate: commenters argue over who pays for decentralised hosting; one cites a blog post about consuming the firehose for less than $2.50/mo, and another says a PDS is a small Node app with sqlite.
- icy (co-founder) says a recent OAuth library switch caused a regression preventing new users being added to the default knot and spindle, fixed by logging out and in.
- icy argues atproto fits data around code such as issues and pulls, and says Gitea is stuck on GitHub because 30k+ issues and PRs cannot migrate due to API rate limits.
- Skeptics: one commenter calls atproto pointless for git; another compares to the radicle project, which a commenter says uses around 40G of storage for 5k repos.
- A commenter says most Bluesky users do not run a personal PDS and expects Tangled to trend the same way.

## Related

- Tangled (tangled.org), AT Protocol lexicons, PDS, ufos.microcosm.blue, Jujutsu, radicle, git-bug.
