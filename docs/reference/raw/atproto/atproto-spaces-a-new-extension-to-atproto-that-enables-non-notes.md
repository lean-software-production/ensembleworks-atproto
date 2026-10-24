# ATProto spaces: A new extension to ATProto that enables non-public data (source notes)

> Source: https://news.ycombinator.com/item?id=49379732
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-02 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: terms-of-service — Hacker News comments; site terms. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/news-ycombinator-com-1230c30c/001.md.
> Work: news.ycombinator.com/item?id=49379732
> Quotations: 27 characters verbatim in this file; 27 of 90 allowed for this work across the knowledge base.

## About this source

A Hacker News discussion thread about the ATProto spaces alpha announcement (a new extension for non-public data), submitted by grappler, linking to https://atproto.com/blog/atproto-spaces-alpha. The API metadata shows a creation date in August 2026 and a score of 178 points. Comments are from the Hacker News community, not from the protocol authors, and are opinion.

## Key facts

- Naming debate: ChrisArchitect argues the word "Spaces" collides with Twitter Spaces (live audio) and suggests another name; oofdere replies that "space" is an ordinary English word; embedding-shape argues common words clash; tolerance guesses the overlap might be deliberate to distance atproto from Bluesky and X.
- Architecture questions: pocksuppet asks whether this is merely a server; tancop answers that data stays on the user's PDS and that, for a space, a requester must present a token signed by the space authority to read records from someone else's PDS. oddevan suggests thinking "protected" rather than "private" (subscriber perks, paywalled content). inigyou worries about relays caching private data and whether every relay would check auth.
- jodosha quotes the blog post: spaces give access control, not confidentiality, and data in a space is readable by any user or app with access and is not encrypted. irickt replies that encryption with multiple access is a specialised need that could be built on the primitive, citing the next sentence of the post saying the primitive is flexible with a deliberately broad range of uses.
- arikrahman remarks that tangled.sh is about to gain private repositories (an expectation, not a fact from the article).
- isodev criticises the lexicon sprawl and notes the absence of references to the IDSA (International Data Spaces Association), preferring reuse of existing ontologies such as schema.org.
- jazzyjackson and evbogue discuss atproto generally: signed Merkle trees and portable identity are praised; evbogue says content hashes are not advertised so data cannot be distributed by the software.
- The thread contains a short sub-discussion on whether atproto runs on top of HTTP and how it compares to REST and ActivityPub; no authoritative answers from the authors.

## Relevance to session sharing

- Community reception shows the main safety misunderstanding to document: spaces are access-controlled, not encrypted, so shared coding-agent sessions in a space are readable by every member and by the hosting PDS and any app granted access. Do not treat this thread as a spec.

## Related

- The atproto spaces alpha blog post, permissioned data proposal, Tangled.
