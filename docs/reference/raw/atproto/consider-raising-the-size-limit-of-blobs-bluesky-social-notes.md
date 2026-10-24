# Consider raising the size limit of blobs · bluesky-social/atproto · Discussion #1740 (source notes)

> Source: https://github.com/bluesky-social/atproto/discussions/1740
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-02 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub discussion; user content. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-63e83827/001.md.
> Work: bluesky-social/atproto#1740
> Quotations: 77 characters verbatim in this file; 77 of 90 allowed for this work across the knowledge base.

## About this source

A GitHub discussion in the atproto repository, in the "Bluesky Lexicons" category, started by davidcelis on Oct 12, 2023. It collects 9 comments and 11 replies running to Aug 9, 2026. Maintainers bnewbold and pfrazee answer.

## Key facts

- The opening post complains of an undocumented blob size limit of 976.56 kilobytes for images, and compares it with Mastodon v4.2.0, which allowed images up to 16 megabytes. The author is not asking for 16 MB specifically, just a limit above 1 MB.
- bnewbold (Oct 12, 2023) points out the limit, one million bytes, is declared in the lexicon `lexicons/app/bsky/embed/images.json`. He explains the Lexicon "social contract": values like this cannot be changed in place; a new record version or a new embed type would be needed (the post `embed` field is an open union). He says they were still in a maturity window where a small breaking change might be considered.
- pfrazee (Oct 13, 2023) says the size was chosen so images propagate efficiently through the network without bad load times.
- Why bsky.app can post bigger images (Mar 2024 onward): bnewbold and others say the web app resizes images in JavaScript before upload; the limit bites API users.
- Allowed formats (bnewbold, May 14, 2024): the lexicon constraint is `image/*`; in practice he believes JPEG, PNG, WEBP and GIF are allowed. Files are stored as-is on the PDS but usually resized and stored on a CDN, possibly converted to JPEG.
- bnewbold (Jul 20, 2024): not changed yet; the team is considering both a specific app limit and making Lexicon more flexible about blob sizes. He distinguishes opinionated constraints that define the medium (the 300 char post limit) from cost/performance choices such as upload size that will evolve. Video support was in the works and image limits might change alongside it.
- snarfed (Oct 23, 2024, and again Feb 9, 2025) asks whether the limit is actually enforced anywhere, noting the AppView apparently does not enforce it and other PDSes, relay and AppView may differ.
- Later commenters point to social-app PRs on binary-search image compression, and the final comment (laem, Aug 9, 2026) links a commit titled "Increase max image upload size to 2mb from 1mb".

## Relevance to session sharing

- Illustrates how Lexicon maxSize blob limits are treated as de facto schema contracts, and that enforcement varies by service. Any lexicon for session transcripts or attachments must pick blob limits knowing they are hard to evolve.

## Related

- Discussion on raising the image limit in 2026, issue on blobstore consumption, the image-embed lexicon, Lexicon evolution rules.
