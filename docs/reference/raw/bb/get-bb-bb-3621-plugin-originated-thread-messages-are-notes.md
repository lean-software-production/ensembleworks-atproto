# get-bb/bb#3621: Plugin-originated thread messages are indistinguishable from user input (initiator=user, senderThreadId=null) (source notes)

> Source: https://github.com/get-bb/bb/issues/3621
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-01 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-8d278711/001.md.
> Work: get-bb/bb#3621
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A GitHub issue (number 3621) on get-bb/bb, authored by jjanousek, about messages that bb plugins send to threads being recorded as if the human user typed them. Labels in metadata: threads, security, partial-repro. State open, four comments. These are factual notes, not the original text.

## Key facts

- Summary of the defect: a plugin-service message to a thread arrives with `initiator` set to user and `senderThreadId` null, the same shape as a message the human typed, so the receiving agent and the renderer cannot tell them apart.
- Cause reported: `bb thread tell` derives the sender from `BB_THREAD_ID`; a plugin service has no calling thread, so the sender is null and initiator falls back to user.
- Tested on bb 0.43.0 per the reporter; a later commenter says it still reproduces on bb 0.44.0.
- Evidence offered is a query on the local database `~/.bb/bb.db` over events of type `client/turn/requested`. The event data has fields `direction`, `source`, `initiator`, `senderThreadId` and `input`.
- Reported distribution on one real install: agent with a sender thread 1111; user with null sender 539; user with null sender and source spawn 127; system with null sender 105. The reporter says the 539 are plugin-originated.
- Why it matters, per the reporter: an agent treats its owner's words as authorization and other components' words as data, and this collapses the distinction; on that install nine messages from one plugin were put into the owner's voice before anyone noticed.
- The initiator enum already has a system value, so the enum is not the obstacle. Suggested fixes: a `senderPluginId` field alongside `senderThreadId`, or `bb thread tell --as-plugin <id>`. The reporter and a commenter argue the host should set it from the calling plugin's identity rather than trusting a supplied string.
- Workaround in use: plugins prefix messages with an automated-message line. A comment describes another plugin that fingerprints its own messages with a sha256 hash to recognise them.
- A commenter notes that attribution alone lets an agent see the difference but does not stop it acting; the renderer and the authorization path both need it. A maintainer comment cross-links authorization work in issues 1541 and 1564 and cautions that an attribution field is not proof of human approval.
- An automation bot comment classifies it as a high-priority bug, partially reproduced, and says no pull request was made because fixing it needs a public-contract and security-boundary decision.
- A fourth comment says an agent that unsets `BB_THREAD_ID` gets the same user attribution because the loopback API answers without credentials; this is tracked separately as issue 4529.

## Related

bb threads and events, plugin SDK, prompt-injection and trust boundaries, provenance of messages in session transcripts.
Relevance: shared bb transcripts may record plugin or system text as user input, so a published session record cannot assume initiator is reliable. See also the bb configuration doc, which says plugin sends carry an origin plugin id in telemetry; this is a possible partial counterpoint (observation, not stated by the issue).
