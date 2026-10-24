# Message Provenance and Attribution

> Sources: get-bb/bb issue #3621 by jjanousek and commenters (notes only); get-bb/bb `docs/configuration.md` (MIT); pi Extensions docs via community mirror (notes only); all collected 2026-10-23; source inventory: get-bb/bb#3621: Plugin-originated thread messages are indistinguishable from user input (initiator=user, senderThreadId=null) (source notes) (attributed source notes; Unknown); get-bb/bb: docs/configuration.md (Copyright (c) 2026 Michael Yong, get-bb/bb; Unknown); Extensions (source notes) (attributed source notes; Unknown); Agent Trace: Cursor Proposes an Open Specification for AI Code Attribution (source notes) (attributed source notes; Unknown); earendil-works/pi: packages/coding-agent/examples/extensions/send-user-message.ts (Copyright (c) 2025 Mario Zechner, pi; Unknown); On Automated and Explainable Provenance of AI-Generated Code (source notes) (attributed source notes; 2026-08-03)
> Raw: [get-bb/bb#3621 (notes)](../../raw/bb/get-bb-bb-3621-plugin-originated-thread-messages-are-notes.md); [bb configuration.md](../../raw/bb/get-bb-bb-docs-configuration-md.md); [pi extensions docs, ubitools mirror (notes)](../../raw/pi/extensions-notes.md); [agent-trace-cursor-proposes-an-open-specification-for-ai-notes](../../raw/agent-sessions/agent-trace-cursor-proposes-an-open-specification-for-ai-notes.md); [earendil-works-pi-packages-coding-agent-examples-extensions](../../raw/pi/earendil-works-pi-packages-coding-agent-examples-extensions.md); [2026-08-03-on-automated-and-explainable-provenance-of-ai-generated-code-notes](../../raw/collaboration-research/2026-08-03-on-automated-and-explainable-provenance-of-ai-generated-code-notes.md)
> Updated: 2026-10-24

## Overview

A shared agent session is only trustworthy if every message says honestly who produced it: the human owner, a collaborator, another agent, a plugin or the system. Agents treat their owner's words as authorisation and other text as data. A transcript that misattributes plugin or remote text to the user therefore collapses that boundary. This matters twice for this project. Published session records must not overstate who said what, and *remote participation* must never be laundered into owner-voice input.

## Evidence from bb

bb issue #3621 (open, labelled threads / security / partial-repro) reports the following:

- A message a plugin service sends into a thread is stored with `initiator` set to user and `senderThreadId` null. That is the same shape as a message the human typed, so neither the receiving agent nor the renderer can tell them apart.
- **Cause.** `bb thread tell` derives the sender from `BB_THREAD_ID`. A plugin service has no calling thread, so attribution falls back to user.
- **Versions.** Reported on bb 0.43.0, and still reproducible on bb 0.44.0 according to a commenter.
- **Scale on one real install** (from `client/turn/requested` events in `~/.bb/bb.db`):
  - 1111 agent messages with a sender thread
  - 539 user-attributed messages with null sender, which the reporter says are plugin-originated
  - 127 user messages with source spawn
  - 105 system messages
  - On that install, nine messages from one plugin were put in the owner's voice before anyone noticed.
- **Proposed fixes.** A `senderPluginId` field, or `bb thread tell --as-plugin <id>`. Participants argue the host should set it from the calling plugin's identity, not trust a supplied string.
- **Caveats.** Commenters note that attribution lets an agent *see* the difference but does not stop it acting, so the renderer and the authorisation path both need it. A maintainer warns that an attribution field is not proof of human approval. A further comment says that unsetting `BB_THREAD_ID` yields user attribution because the loopback API answers without credentials. That is tracked as issue 4529.
- **Status.** An automation comment classifies it as a high-priority bug. No PR was opened, because the fix needs a public-contract and security-boundary decision.

> **Status: Disputed**
> bb's current `docs/configuration.md` (collected 2026-10-23) says telemetry `initiator` values include `plugin` and `automation`. It also says sends from a plugin carry its ID because the plugin SDK adds `originPluginId`. Issue #3621 was still open at collection and reports that stored `client/turn/requested` events from plugin services using `bb thread tell` on 0.43.0/0.44.0 are attributed to `user`. The sources do not establish whether the SDK path fixes stored attribution, affects only telemetry, or differs from the CLI path. Verify against current code before relying on either.

## Evidence from pi

Pi distinguishes two extension paths. `pi.sendMessage` injects a *custom* message (steer, followUp or nextTurn). `pi.sendUserMessage` sends a message that appears as if typed by the user. Input events do carry a source label (interactive, rpc or extension), so pi records provenance at the input layer even when the content is user-shaped. See [Pi Extensions](../pi/pi-extensions.md).

## Design implications

- **Record provenance explicitly in the lexicon.** Every published message needs an author DID and a role (owner, collaborator, agent, plugin, system), plus the harness's own source label where one exists. The harness's `initiator` field is unreliable as-is (bb#3621).
- **Remote replies should enter as attributed, non-owner input.** In pi, prefer a `custom_message` with `display` over `sendUserMessage`. Show collaborator input to the agent as data, unless the owner explicitly approves it.
- **An attribution field is not an authorisation.** Remote participation needs a separate approval gate. See [Prompt Injection and the Lethal Trifecta](secret-leakage-in-shared-sessions.md).

## See Also

- [bb Plugin System](../bb/bb-plugins.md)
- [bb Architecture and Data Model](../bb/bb-architecture.md)
- [Pi Extensions](../pi/pi-extensions.md)

## Code attribution versus session interchange

InfoQ’s account of Cursor’s Agent Trace RFC describes records linking code ranges to conversations and contributor categories. The format is storage-independent and can attach model identity or content hashes. It does not define ownership, judge code quality or establish training-data provenance. For a session-sharing design it supplies links from code to conversation evidence, rather than replacing a complete trajectory. Merge and rebase handling remain open questions in this RFC account.

## Upstream example confirms user-role injection

Pi’s send-user-message example intentionally inserts actual user messages from an extension and demonstrates both steering and follow-up delivery while busy. When idle, submission triggers a turn. A transcript’s user role alone therefore does not establish a human typed that content. A sharing layer should preserve origin separately from the model-facing role and identify extension-generated requests.

## Explainable code provenance is a research agenda

Velasco and colleagues distinguish prompt-to-output, instance-to-output, factor-to-output and model-component-to-output traceability. They propose attribution techniques and practitioner research while identifying inaccessible training data, missing ground truth and causal confounds as open challenges. This is a research vision, not an evaluated provenance system. Recording the generating session can support prompt-level provenance, but it cannot establish training-instance influence or legal ownership.

## Related compiled concepts

- [Knowledge Transfer and AI Collaboration](../collaboration-research/knowledge-transfer-and-ai-collaboration.md)
