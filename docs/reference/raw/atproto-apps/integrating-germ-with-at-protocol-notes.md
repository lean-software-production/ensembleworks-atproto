# Integrating Germ with AT Protocol (source notes)

> Source: https://www.germnetwork.com/blog/integrating-germ-atproto
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-10 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — no license statement in page. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/germnetwork-com-74e45a84/001.md.
> Work: https://www.germnetwork.com/blog/integrating-germ-atproto
> Quotations: 6 characters verbatim in this file; 6 of 90 allowed for this work across the knowledge base.

## About this source

Technical engineering blog post by Mark Xue (Germ Network) describing how Germ's end-to-end encrypted DMs are integrated with AT Protocol identities. The page shows only "Jul 28" with no year, so the publication date is treated as unknown. It is a beta-era architecture description and the author flags several parts as future directions.

## Key facts

- Goal: E2EE conversations between AT Protocol DIDs, so changing a handle does not interrupt a conversation.
- Three steps are required: agree on messaging cryptographic identities, set up encryption sessions that end at those identities, and transport the encrypted messages.
- The author calls the identities device-bound: only the user's devices can use them, in contrast to AT Protocol signing keys, which are commonly delegated to a server (the PDS).
- The author argues PDS-delegated publishing keys suit public posting, where misuse is quickly noticed, but not private messaging, where misuse cannot be detected.
- Trust principle cited: a key from a weakly trusted intermediary is acceptable if the key owner would quickly notice lying. Key transparency logs are named as the stronger approach.
- Anchor key: a public signing key bound to a DID for E2EE messaging (shown as the pairing key in the app UI), or nil if the account cannot receive E2EE messages. The binding can change over time.
- Current implementation: the Anchor key is published in the AT Protocol profile bio text. The Germ app monitors the user's own bio and others' bios for changes.
- A custom PDS record for the binding was considered and rejected, because users would not see it on other AppViews.
- Verification: the recipient fetches the `com.germnetwork.keypackage` record from the sender's PDS. It holds an AnchorHello package with data to start an encryption session and a signature by the Anchor key over the DID, completing a bidirectional binding.
- Future direction: move the key out of the bio if PDSes had a standard way to publish an E2EE key and AppViews showed it to users with a way to remove unexpected values.
- Application-layer rule: a valid message goes from a delegate of the sender's current Anchor key to a delegate of the recipient's current Anchor key.
- Anchor key delegates to task-specific signing keys called Agents; the Anchor is analogous to an Identity Key in the Autonomous Communicator Protocol (ACP).
- A Hello agent is delegated in the AnchorHello to receive handshakes. The initiator's first messages carry a Reply object with the newly delegated agent and signatures proving DID to Anchor to Agent delegation.
- Agents map 1:1 to MLS Clients, using the Agent public key as the MLS basic credential.
- Distributed MLS: each participant uses an MLS group as their Send Group; fresh key material is mixed across groups using MLS key import and export for post-compromise security. An Internet-Draft `draft-xue-distributed-mls` is referenced.
- The 1:1 implementation, called TwoMLS, shipped in app version 2.2.0 according to the post; a detailed writeup is promised.
- TwoMLS handshake: the initiator adds the recipient's Hello agent to a new MLS group (their send group) and staples the MLS welcome to first-round messages. The recipient exports a key from that group to build their own send group, so only members of the first can join the second.
- Multiple valid sessions between a pair of DIDs must be tolerated; clients converge on the most recently used session and may purge stale ones.
- Key rotation: a new anchor key can come with a proof of succession signed by predecessor and successor. Without it the app should warn the user, since a security boundary may have been crossed.
- Transport: TwoMLS encrypts MLS private messages with a symmetric header key derived per epoch. ACP transport uses ephemeral and rendezvous mailboxes whose addresses change with each exchange; Germ implements these over HTTPS.
- Initial Reply messages are authenticated to the sender's Anchor key and addressed to the recipient's Anchor key. Germ servers learn only anchor keys and never learn the DID.
- New-connection policy (for example, only accounts the recipient follows) is public in the AnchorHello and enforced on the recipient's device. The author suggests a PDS could enforce it and vend single-use keyPackages, which would need an authenticated xRPC interface (a gist by another developer is linked).

## Related

- Companion announcement post on Germ DM beta, and the Autonomous Communicator Protocol blog post (both on germnetwork.com)
- MLS Architecture (RFC 9750)
- `com.germnetwork.keypackage` lexicon record
