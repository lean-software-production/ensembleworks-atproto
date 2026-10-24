# Research Brief: Social Coding for the AI Age ("Bluesky for code")

## 0. How to read this brief

You are a research team being sent out ahead of a build. Your job is to map the ground well enough that the engineers who come after you won't be surprised by anything important. Depth matters more than speed. Read primary sources: specs, source code, RFCs, issue trackers, commit history, and conference talks. Run things locally when that's the only way to learn how they actually behave. Wherever you can, separate what the docs **claim** from what the code **does**.

Every factual claim in your output needs a source (URL plus commit SHA or access date). Label each one **verified** (you read the code or ran it), **documented** (official docs say so), or **reported** (third-party or hearsay). Unknowns are fine and expected. List them openly rather than papering over them.

## 1. The vision (verbatim intent, paraphrased)

From `docs/vision.md`:

> Social coding for the AI age. Bluesky for code.

- Build an **ATProto Lexicon and PDS** for sharing **coding-agent sessions** between people.
- A user can share **a specific session** or **all sessions in a project folder** with collaborators on the network. At minimum, collaborators can **read** them.
- Ideally collaborators can also **participate** in a session, the way you reply in a Bluesky thread, *within safety bounds of remote execution*.
- A **feed of all activity on a team**.
- **Privacy** for teams and companies via ATProto **Groups** (<https://atproto.com/blog/atmospheric-groups-intro>).
- **Harness-agnostic**, with first-class support for **pi** (<https://pi.dev>) via an extension and **bb** (<https://getbb.app>) via a plugin. bb may also need a fork, at least temporarily.
- Implementation is likely **TypeScript**, for compatibility with pi and bb. Alternatives: a Rust or Go CLI, and/or a Docker-packaged PDS.

## 2. What we already know (pre-research reconnaissance, 2026-10-23)

These notes come from a quick read of the project homepages. Treat them as leads to verify, not conclusions.

### pi (pi.dev)
- Minimal, adaptable agent harness from Earendil Inc. MIT licensed. Source: `github.com/earendil-works/pi` (`packages/coding-agent`). npm: `@earendil-works/pi-coding-agent`.
- Modes: interactive TUI, print/JSON event stream (`pi -p`, `--mode json`), **RPC over stdin/stdout**, and an embeddable **SDK**.
- **Extensions** are TypeScript modules with access to tools, commands, keybindings, events, and the TUI. They're distributed as "pi packages" through npm or git (`pi install npm:…` / `git:…`). The repo includes 50+ example extensions, among them permission gates, path protection, SSH execution, and sandboxing.
- **Sessions are stored as trees in a single file**, with branching via `/tree`, labels, and filtering by message type. The on-disk format is **not documented on the homepage**.
- Built-in sharing exists today: `/export` produces HTML, and `/share` uploads to a **GitHub gist** with a rendered viewer URL (example: pi.dev/session). This is the closest prior art to our read-only sharing.
- Supports steering messages to a running agent and queued follow-ups. These are a likely hook point for remote participation.

### bb (getbb.app)
- An "agentic IDE" that "builds itself." Repo: `github.com/get-bb/bb`. Install via `npx bb-app@latest`. Mature on macOS (Apple Silicon); Linux and Windows are alpha; remote machines are supported.
- Hosts many agents, including Claude, OpenAI, Cursor, **Pi**, opencode, Grok Build, oh-my-pi, Hermes Agent, and more. Recent releases mention **ACP** (Agent Client Protocol) support.
- The work model is **threads** and **automations**, with diff review and commit.
- The plugin guide (getbb.app/plugin-guide) lists a very broad surface. Relevant parts: **lifecycle events for thread state changes**, a **dispatch hook that runs before messages reach an agent**, **provider bridges** (which run agent sessions through a bridge shipped to each machine), per-thread private JSON records, plugin server storage, HTTP/WebSocket/RPC/realtime messaging, timeline entries, message embeds, and thread header controls.
- **Not documented on the pages we read:** implementation language/runtime, license, thread/session persistence format, and how sessions could be synced externally. Finding these out is a top priority.

### ATProto Groups / Spaces
- An "atmospheric group" is **a DID with permissioned Spaces under it**. Spec: the community proposal at `tangled.org/opensocial.group/proposal/`. The underlying protocol is **Bluesky proposal 0016 (permissioned data / Spaces)**: `github.com/bluesky-social/proposals/tree/main/0016-permissioned-data`.
- Membership is a two-way handshake: the group writes a `membership` record with roles, and the member writes an `acceptance` record. These live in the `fyi.opensocial.members` space, which also has an `access` record and a `meta` space.
- Access is **flat RBAC** per space, enforced by the group host when it issues space credentials. Write rules are app-specific and defined in each app's lexicons. The group host also acts as an **OAuth authorization server** for the group DID.
- **Member records stay in members' own repos on their own PDS.** The group host tracks each space's writer set and routes notifications. Apps sync each writer's repo directly.
- Status: a **community proposal**, in production use by Grain, but **only on spaces-enabled PDSes**. Maturity, implementation availability, and timeline are critical unknowns.

## 3. Core research questions

Organise your work around these questions. Each workstream below breaks them down further.

1. **Representation:** What is the right data model (Lexicon) for a coding-agent session? The model has to capture tree-shaped branching, tool calls, diffs, large outputs, and harness-specific metadata, and stay harness-agnostic.
2. **Placement:** Where does session data live? Options include the author's PDS, a dedicated PDS, a Space, blobs, or off-protocol storage. What does that mean for size, privacy, deletion, and portability?
3. **Privacy:** Can permissioned Spaces/Groups deliver team- and company-private sharing **today**? If not, what is the least-bad interim path?
4. **Participation:** What does "replying" into someone else's agent session mean, both technically and socially? How do we make it safe, given that a reply may cause code execution on someone else's machine?
5. **Distribution:** How do team activity feeds work? Which AppView/indexer architecture fits, and what do we have to run ourselves?
6. **Integration:** Exactly how do we hook into pi and bb? What can extensions and plugins do, and where would we need to fork?
7. **Landscape:** Who has already tried this, in session sharing, social coding on ATProto, or agent transcript standards? What can we reuse, and what should we avoid?

## 4. Workstreams

### WS1: ATProto foundations (deep)
- Protocol fundamentals as they relate to our design: repos, MST, CIDs, DIDs (plc/web), handles, records versus blobs, **record and blob size limits**, rate limits, deletion semantics, and what "deletion" really means once the data has hit the firehose and relays.
- **Lexicon design**: the spec, NSID namespace ownership and authority (DNS), versioning/evolution rules, `union`/`ref`/open unions, `$type` extensibility, and the Lexicon resolution and publication work under way in 2025–26. Study well-designed third-party lexicons as models.
- **PDS options**: the reference `bluesky-social/pds` (Docker), `@atproto/pds`, and alternative implementations (e.g. Rust or Go PDSes such as rsky and cocoon; verify the current landscape). Can a stock PDS store arbitrary lexicons? What changes when we need Spaces? What does self-hosting cost operationally?
- **Sync/infra**: the firehose (`com.atproto.sync.subscribeRepos`), **Jetstream**, relays and their current non-archival design, Sync v1.1, `@atproto/tap` or equivalent backfill tools, and the costs and patterns of building an **AppView**.
- **Auth**: ATProto OAuth (DPoP, PAR, scopes and the newer granular permission scopes), app passwords, and service auth (`getServiceAuth`, inter-service JWTs). Which ones would a CLI, a pi extension, and a bb plugin each use?
- **Feeds**: feed generators, custom feed skeletons, and whether a non-Bluesky app can reuse them or must build its own feed infrastructure.
- **Moderation and labels**: labelers and Ozone. Are they relevant to secret leakage or abuse in shared sessions?
- **SDKs**: `@atproto/api`, `@atproto/lex-cli` codegen, `@atproto/oauth-client-node`/`-browser`, and community SDKs (Rust `atrium`, Go `indigo`, Python, and others). Assess how mature each is for our use.

### WS2: Permissioned data, Spaces & Groups (deepest dive; highest risk)
- Read proposal 0016 in full, including its history, discussion threads, and any follow-on proposals. Explain precisely how it differs from public repos: encryption (or lack of it), credential issuance, sync, and how leaks are handled.
- Read the opensocial.group proposal and the Grain implementation. Identify which PDS implementations support Spaces today, and whether the reference PDS does or will.
- Map our needs onto Groups: one group per team or company? Per-project spaces? A per-session ACL? How are sharing "a single session" and "all sessions in a folder" expressed?
- Revocation: when someone leaves a team, what can they still see? What cached copies exist in AppViews?
- **If Spaces are not ready**, evaluate the fallbacks: E2EE blobs in public repos (key management via MLS? Germ? other ATProto E2EE work), a private self-hosted PDS plus a private AppView, off-protocol storage with on-protocol pointers, and others. Give the security and UX cost of each.
- Find the people involved (Bluesky team, opensocial.group authors, Grain developers) and their public statements on roadmap and timing.

### WS3: Coding-agent session formats & standards
- Document the session/transcript formats of: **pi** (tree-in-a-file; find the real schema in source), **bb** threads, Claude Code (JSONL under `~/.claude/projects`), OpenAI Codex CLI (rollout files), opencode, Cursor, Aider, Amp, Gemini CLI, Goose, Zed agent, Cline/Roo, and others you find.
- Standards and protocols: **ACP (Agent Client Protocol)** from Zed, **MCP**, A2A, and any emerging **agent-trace or transcript interchange specs** (verify; several were proposed in 2025–26). Also look at OpenTelemetry GenAI semantic conventions, and at how LangSmith, Langfuse, and Braintrust model traces.
- Propose a **common denominator model**: messages, roles, tool calls and results, file edits/diffs, shell commands and outputs, model/provider metadata, token/cost usage, branching (tree) structure, compaction/summaries, attachments, and the git context (repo, commit, branch, dirty state).
- How do large outputs, binary artifacts, and images map onto records versus blobs? Should sessions stream as many small records or snapshot as a few big ones? Measure real session sizes from a sample of genuine sessions.

### WS4: Harness integration (pi and bb)
- **pi**: read the extension API source and examples end to end. Can an extension (a) observe every session event live, (b) read and write the session tree, (c) inject messages or steering from a remote source, (d) gate tool execution? Study the existing `/share` gist implementation as a template. Assess the RPC and SDK modes for a headless "remote participant" runner.
- **bb**: clone `get-bb/bb`. Determine its language/runtime, license, build, plugin loading, the thread/session storage format, how provider bridges work, how the dispatch hook and lifecycle events behave, and how pi runs *inside* bb. Identify exactly what a plugin **cannot** do that would force a fork. Estimate what it would cost to maintain that fork, and whether the changes could be upstreamed. Find the maintainers' contribution policy.
- What would generic harness support look like? Options: an ACP proxy or tap, file watchers on known session directories, and an OTel exporter. Rank them by fidelity and coverage.
- Is TypeScript the right core language? Compare it with a Rust/Go CLI plus thin TS adapters, taking into account distribution (npm vs. single binary), and look at what pi and bb themselves ship.

### WS5: Remote participation & execution safety
- Define a spectrum of participation: comment/annotate → suggest a prompt for the owner to approve → queue a steering message → co-drive with execution on the owner's machine → fork the session and run it on the participant's own machine or sandbox.
- Threat model: **prompt injection via remote replies**, tool-call abuse, data exfiltration, secrets in transcripts, supply-chain risk from shared skills/extensions, impersonation, and replay. Use frameworks such as the "lethal trifecta" (Simon Willison), OWASP's LLM Top 10, and published agent-security research and incidents.
- Mitigations: permission gates (pi already has examples), capability-scoped execution, sandboxing (containers, microVMs like Firecracker, gVisor, macOS Seatbelt, Landlock, devcontainers, and hosted sandboxes such as E2B, Daytona, and Modal), human-in-the-loop approval UX, and signed provenance of who said what (ATProto record signatures).
- **Secret and PII redaction** before publishing: tools such as gitleaks, trufflehog, and detect-secrets, plus entropy heuristics. Should redaction run client-side before anything leaves the machine? Test false-positive and false-negative rates on real transcripts.

### WS6: Feeds, social UX & product
- Team activity feed: what events (session started, milestone, PR opened, help requested), how to rank or filter them, and how to notify.
- Learn from the UX of Bluesky threads, GitHub activity, Slack, Linear, and Amp's public threads and team features. Also look at opencode `/share`, Cursor and Claude Code share features, SpecStory, and transcript viewers (e.g. claude-code-log and similar).
- Viewer: what makes an agent session readable? Collapsing tool output, diff rendering, branch navigation, jump-to-decision. Review existing viewers and pi's HTML export.
- Social dynamics: norms around sharing AI sessions, how mob/ensemble programming translates to agent sessions (this project lives in an "ensembleworks" repo, so ensemble/mob programming literature is relevant), and the risk of performative sharing.

### WS7: Landscape & prior art
- Social coding on ATProto: **Tangled** (git collaboration on ATProto, which also hosts the Groups proposal), plus any other dev-tool ATProto apps (code snippets, PR reviews, CI). Study their lexicons, architecture, and lessons learned.
- Other ATProto apps with relevant patterns: Grain (groups), WhiteWind/Leaflet (long-form records), Frontpage, Smoke Signal, Roomy (group chat on ATProto), and Germ (E2EE).
- Session-sharing products and startups (2024–26): who exists, what they charge, what happened to them.
- Academic and industry literature: collaborative programming with LLMs, pair programming with AI, provenance of AI-generated code, transcript-as-documentation, knowledge sharing in software teams, and decentralised social protocols (ATProto papers, e.g. Kleppmann et al., "Bluesky and the AT Protocol: Usable Decentralized Social Media", 2024). Include ActivityPub/ForgeFed as a comparison point.
- Legal and compliance: ownership of transcripts, model provider ToS on sharing outputs, GDPR erasure versus content-addressed public data, and company data-loss-prevention policies.

## 5. Deliverables

Produce these under `docs/research/`:

1. **`findings/<workstream>.md`**: one per workstream, with sourced findings, verified/documented/reported labels, and open questions.
2. **`landscape.md`**: a table of every relevant tool, library, product, spec, and paper. Columns: name, link, what it is, licence, maturity, relevance (high/med/low), reuse potential.
3. **`lexicon-sketch.md`**: a first-draft Lexicon set (NSIDs, record types, JSON schemas) for sessions, session entries, shares, team feed events, and participation/replies. Include design alternatives and their trade-offs.
4. **`architecture-options.md`**: two to four end-to-end architectures (e.g. "stock PDS + public-only MVP", "Spaces-native", "self-hosted private PDS + AppView", "E2EE blobs"). Each needs a diagram, components, what we build versus reuse, risks, and a rough effort estimate.
5. **`integration-pi.md` and `integration-bb.md`**: concrete hook points with file/line references into source, a proof-of-concept plan, and the fork assessment for bb.
6. **`threat-model.md`**: assets, actors, attack paths, and mitigations for both read-only sharing and participation.
7. **`risks-and-unknowns.md`**: a ranked list of existential risks (e.g. "Spaces not shippable within 12 months"), each with the evidence and a suggested spike to retire it.
8. **`recommendation.md`**: your team's opinionated recommendation for the MVP scope, the stack, and the first three spikes. Disagreement within the team is welcome. Record it.

Small proofs of concept are encouraged where they settle a question cheaply. Examples: write a custom-lexicon record to a local PDS, capture a pi session via an extension, or render a session from records. Put the code in `docs/research/spikes/<name>/` with a README.

## 6. Constraints & principles

- **Harness-agnostic first.** pi and bb are the initial targets, not the boundary.
- **Privacy by default.** Nothing leaves a developer's machine unless they shared it explicitly. Assume transcripts contain secrets.
- **Protocol-native where possible.** Prefer standard ATProto mechanisms over bespoke servers. Where we must deviate, say why.
- **Safety over capability** for remote participation. Read-only sharing must be excellent before participation ships.
- **Respect upstreams.** Prefer contributions to pi, bb, and ATProto over long-lived forks.

## 7. Known gaps from the reconnaissance (resolve these first)

- bb: implementation language, licence, session/thread storage format, and plugin runtime. None of these were stated on getbb.app or the plugin guide. Only the first ~100k characters of the getbb.app homepage were reviewed.
- pi: the on-disk session tree format and the core implementation language.
- Spaces: which PDS implementations support them, and the reference PDS roadmap.
- Whether any agent-transcript interchange standard has real adoption.

Spare no expense. Go deep, cite everything, and tell us what we don't want to hear.
