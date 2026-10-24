# Knowledge Base Index

## agent-protocols

Compiled concepts and source-qualified findings for agent protocols.

| Article | Summary | Updated |
|---------|---------|---------|
| [Agent Client Protocol (ACP)](agent-protocols/agent-client-protocol.md) | ACP connects agent clients such as editors to coding agents. | 2026-10-24 |
| [Agent Protocol Boundaries](agent-protocols/protocol-boundaries.md) | Agent interoperability spans client-agent interaction, tool/context interfaces and agent-to-agent delegation. | 2026-10-24 |

## agent-sessions

Compiled concepts and source-qualified findings for agent sessions.

| Article | Summary | Updated |
|---------|---------|---------|
| [Agent Session and Trace Formats](agent-sessions/agent-session-trace-formats.md) | Native session logs, normalized trajectories and observability spans preserve different information. | 2026-10-24 |

## atproto

Compiled concepts and source-qualified findings for atproto.

| Article | Summary | Updated |
|---------|---------|---------|
| [Atmospheric Groups](atproto/atmospheric-groups.md) | The community opensocial.group proposal defines a group in one line: "An atmospheric group is a DID with a bunch of permissioned spaces under it." (atproto.com, CC-BY). | 2026-10-23 |
| [ATProto Spaces (Permissioned Data)](atproto/atproto-spaces-permissioned-data.md) | **Atproto spaces** are Bluesky's extension for non-public data. | 2026-10-24 |
| [ATProto Blobs and Size Limits](atproto/blobs-and-size-limits.md) | Blobs are files stored next to an account's repo and referenced from records by CID. | 2026-10-23 |
| [ATProto OAuth and Permissions](atproto/oauth-and-permissions.md) | Apps act on a user's PDS through a specific atproto *profile* of OAuth. | 2026-10-23 |
| [ATProto PDS Operation and Observability](atproto/pds-operation.md) | Operator branding, telemetry, blob policy and Spaces alpha deployment. | 2026-10-24 |
| [ATProto Repository, Records and Lexicon](atproto/repository-and-records.md) | Each account's public data lives in one signed, content-addressed **repository**. | 2026-10-24 |
| [ATProto Sync and Firehose](atproto/sync-and-firehose.md) | Public atproto data spreads in two ways. | 2026-10-23 |

## atproto-apps

Compiled concepts and source-qualified findings for atproto apps.

| Article | Summary | Updated |
|---------|---------|---------|
| [Writing to Bluesky-Hosted PDSes: Practical Limits](atproto-apps/bluesky-hosted-pds-practical-limits.md) | Teammates whose accounts live on Bluesky's hosted PDSes impose real operational ceilings on a session-sharing tool. | 2026-10-24 |
| [ATProto Curation and Discovery](atproto-apps/curation-and-discovery.md) | ATProto applications can curate links and social signals in user repositories. | 2026-10-24 |
| [Germ: End-to-End Encryption over ATProto Identities](atproto-apps/germ-e2ee-messaging.md) | ATProto Spaces (Permissioned Data) give access control but not confidentiality. | 2026-10-24 |
| [Tangled: Social Coding on ATProto](atproto-apps/tangled-social-coding.md) | Tangled is relevant prior art for social coding over ATProto. | 2026-10-24 |

## bb

Compiled concepts and source-qualified findings for bb.

| Article | Summary | Updated |
|---------|---------|---------|
| [bb Architecture and Data Model](bb/bb-architecture.md) | bb is an "agentic IDE" built from four runtime pieces: a central **server**, a **host daemon** on each execution machine, a web **app**, and the `bb` **CLI** with an SDK. | 2026-10-24 |
| [bb Pi Provider Integration](bb/bb-pi-provider-integration.md) | bb ships a built-in **Pi** provider (`pi`). | 2026-10-24 |
| [bb Plugin System](bb/bb-plugins.md) | bb plugins are on by default. | 2026-10-24 |
| [bb Project Status, Licensing and Contribution](bb/bb-project-status.md) | bb ("The agent IDE that builds itself", per the repo description) is a young, fast-moving MIT-licensed TypeScript project. | 2026-10-24 |

## collaboration-research

Compiled concepts and source-qualified findings for collaboration research.

| Article | Summary | Updated |
|---------|---------|---------|
| [Knowledge Transfer and AI Collaboration](collaboration-research/knowledge-transfer-and-ai-collaboration.md) | Studies of AI-assisted programming examine learning, scrutiny and code understanding under specific tasks. | 2026-10-24 |

## pi

Compiled concepts and source-qualified findings for pi.

| Article | Summary | Updated |
|---------|---------|---------|
| [Pi Architecture and Operations](pi/pi-architecture-and-operations.md) | Pi separates the coding-agent interface from reusable provider, agent-loop and UI components. | 2026-10-24 |
| [Pi Extensions](pi/pi-extensions.md) | Pi extensions are TypeScript modules that subscribe to lifecycle events, register tools the model can call, add commands, renderers and model providers, and persist state inside the session file. | 2026-10-24 |
| [Pi Session File Format](pi/pi-session-format.md) | Pi persists each session as one JSONL file. | 2026-10-23 |
| [Pi Session Sharing and Export](pi/pi-session-sharing-and-export.md) | Session navigation, durable tree storage and publication are separate choices. | 2026-10-24 |

## security-privacy

Compiled concepts and source-qualified findings for security privacy.

| Article | Summary | Updated |
|---------|---------|---------|
| [Message Provenance and Attribution](security-privacy/message-provenance-and-attribution.md) | A shared agent session is only trustworthy if every message says honestly who produced it: the human owner, a collaborator, another agent, a plugin or the system. | 2026-10-24 |
| [Secret and Context Leakage in Shared Sessions](security-privacy/secret-leakage-in-shared-sessions.md) | Shared sessions can expose credentials, private files and tool output. | 2026-10-24 |
