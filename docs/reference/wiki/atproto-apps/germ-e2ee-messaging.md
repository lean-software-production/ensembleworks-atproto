# Germ: End-to-End Encryption over ATProto Identities

> Sources: Mark Xue (Germ Network), "Integrating Germ with AT Protocol" (page shows "Jul 28" without year; notes only), collected 2026-10-23; source inventory: Integrating Germ with AT Protocol (source notes) (attributed source notes; Unknown)
> Raw: [Integrating Germ with AT Protocol (notes)](../../raw/atproto-apps/integrating-germ-with-at-protocol-notes.md)
> Updated: 2026-10-24

## Overview

[ATProto Spaces (Permissioned Data)](../atproto/atproto-spaces-permissioned-data.md) give access control but not confidentiality. Germ shows the main pattern available for actual confidentiality: end-to-end encrypted conversations between ATProto **DIDs**, keyed to *device-bound* keys rather than the PDS-held signing key. The core argument is that PDS-delegated signing keys are fine for public posting, where misuse is quickly noticed, but not for private messaging, where misuse cannot be detected. A possible session-sharing design could adopt a similar device-held key hierarchy. Inference: servers lacking plaintext would need a separate design for content search, indexing and moderation.

## Design (beta-era, per the post)

- **Anchor key.** A public signing key bound to a DID for E2EE. It is currently published in the user's **profile bio text** so it shows up in every AppView. A custom PDS record was considered and rejected because users would not see it elsewhere. Moving out of the bio depends on a future standard way to publish E2EE keys.
- **Bidirectional binding.** The recipient fetches a `com.germnetwork.keypackage` record from the sender's PDS. The record holds an AnchorHello signed by the Anchor key over the DID.
- **Agents.** The Anchor key delegates to task-specific keys called Agents that map 1:1 to MLS clients. A Hello agent receives handshakes.
- **TwoMLS / distributed MLS.** Each participant has its own MLS send group, and key material is mixed across groups for post-compromise security. The post references `draft-xue-distributed-mls` and says TwoMLS shipped in app version 2.2.0.
- **Rotation.** A new anchor key can carry a proof of succession. Without one, the app should warn the user.
- **Transport metadata.** Mailbox addresses rotate with each exchange. Germ servers learn only anchor keys, never DIDs.
- **Policy.** New-connection policy (for example, only accounts the recipient follows) is published in the AnchorHello and enforced on-device. The author suggests a PDS could enforce it and vend single-use key packages, which would need an authenticated XRPC interface.

## Relevance

- Germ demonstrates application-layer encrypted messaging over ATProto identities. Applying that pattern to session sharing is a design proposal; spaces do not supply this encryption.
- The bio-publishing workaround shows the ecosystem still lacks a standard for publishing E2EE keys.
- Name clash: Germ's ACP means the Autonomous Communicator Protocol. It is unrelated to the Agent Client Protocol ([Agent Client Protocol (ACP)](../agent-protocols/agent-client-protocol.md)).

## See Also

- [ATProto Spaces (Permissioned Data)](../atproto/atproto-spaces-permissioned-data.md)
- [Secret and Context Leakage in Shared Sessions](../security-privacy/secret-leakage-in-shared-sessions.md)

## Device-bound messaging identity and transport

Mark Xue’s engineering account separates DID identity, device-held encryption identities and message transport. In the described beta architecture an Anchor key is visible in the profile bio, while a signed key package in a PDS record completes bidirectional identity binding. A custom hidden binding record was rejected because other AppViews would not make unauthorized changes visible. Delegated keys and MLS-based sessions protect messages; PDS signing keys alone do not provide that endpoint trust. The proposed move out of bios requires visible, user-removable standard key publication and is future work. Germ’s Autonomous Communicator Protocol abbreviation is unrelated to Agent Client Protocol.
