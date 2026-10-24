# Social Coding for the AI Age: Pre-Build Research Report (docs/research/)

**Bottom line: you can build this, but not the way the vision assumes. As of 2026-10-24, ATProto cannot give a team private sharing that is production-grade. Spaces is an alpha, Atmospheric Groups was announced two days ago, and Spaces provides access control but no encryption. Agent transcripts are among the most secret-dense artefacts a developer produces. So the MVP should be read-only sharing on a private, team-controlled PDS, with the lexicon designed so the same records move into Spaces when Spaces reaches GA. Nothing should ever go to a public repo by default.**

## TL;DR

- **Privacy is the existential risk, not integration.** Bluesky's own launch post calls Spaces "truly an alpha". It says the code "has not undergone careful security review", that the hosted alpha PDS "goes away at the end of the alpha", and that "spaces give you access control not confidentiality". Bluesky's stated "goal of launching later this year" is a target, not a commitment.\[1\] Anything written to a normal public repo goes to the firehose and cannot be reliably erased.
- **pi and bb are both very hookable TypeScript/MIT codebases, and you probably don't need a bb fork.** pi stores sessions as a documented JSONL tree (v3, `id`/`parentId`).\[2\] Its extensions can observe events, block tool calls, and inject `steer`/`followUp` messages.\[3\]\[4\] bb is a TypeScript monorepo with a SQLite-backed server, a host daemon and full-trust in-process plugins.\[5\]\[6\] It already runs pi in RPC mode, with sessions under `~/.bb/pi-bridge-sessions/`.\[7\]\[8\] The real gaps are small upstream asks, such as letting a plugin identify itself as a message sender.\[9\] Both projects are moving fast, and bb now auto-closes outside PRs from authors who are not on an allow list.\[10\]
- **No agent-transcript interchange standard has real adoption for interactive sessions.** Agent Trace (Cursor; spec header "Version: 0.1.0 Status: RFC Date: January 2026", with partners including Amp, Cloudflare, Cognition, git-ai, Jules, OpenCode and Vercel) covers code attribution, not transcripts. ATIF (Harbor) is used in evaluation and RL pipelines. You will have to define your own lexicon. Make ATIF an export target and Agent Trace's `conversation.url` a link target. Treat secret redaction as a safety net, not a guarantee: in Basak et al.'s 2023 NC State study of nine tools on SecretBench, the best precision was GitHub Secret Scanner's 75% and the best recall was Gitleaks' 88%, and the authors conclude "no current tool has the coveted high precision and high recall scores."

---

## Method, labels and limits

- **Execution constraint.** We could not clone or run anything, so no claim in this report is **verified** in the sense of "executed". Where we read a primary file (a spec, a repo doc, or a source path quoted with a commit SHA in an upstream issue), we label it **documented**. Third-party articles, issues by non-maintainers, DeepWiki summaries and search snippets are **reported**.
- **Access date.** All URLs were accessed 2026-10-24 unless a commit SHA is given. Most GitHub "blob/main" reads have no SHA we could capture, so treat line numbers as drifting.
- **Coverage gaps (stated openly).** We did not research these in depth:
  - legal/ToS
  - ensemble-programming literature
  - Amp, Cursor and Claude Code share features
  - Germ/MLS E2EE
  - PDS rate limits
  - Ozone

  They appear under Unknowns with spike plans instead of invented facts.

---

## Section 7 "Known gaps": resolved first

| Gap | Answer | Label / source |
|---|---|---|
| bb language/runtime | TypeScript pnpm/turbo monorepo on Node. It uses native add-ons `better-sqlite3`, `node-pty` and `@parcel/watcher`, plus an Electron desktop shell.\[11\] | documented: github.com/get-bb/bb README |
| bb licence | MIT ("bb is MIT-licensed end to end"; the repo shows an MIT license file)\[11\]\[12\] | documented: getbb.app, github.com/get-bb/bb |
| bb thread storage | A server "stores all state in a SQLite database". A thread "produces an append-only stream of events (messages, tool calls, file changes, etc.)". Events sit in an `events` table in `~/.bb/bb.db`.\[6\]\[9\] | documented: docs/system-overview.md; `events` table reported via issue get-bb/bb#3621 |
| bb plugin runtime | "Plugins are full-trust code running inside the bb server process." Separate "host workers" and "provider bridges" ship code to each machine.\[5\]\[13\] | documented: docs/configuration.md (snippet), getbb.app/plugin-guide |
| pi language | TypeScript (extensions are TS modules; SDK `createAgentSession`; packages `pi-ai`, `pi-agent-core`, `pi-coding-agent`)\[14\]\[15\] | documented: pi docs; packages reported |
| pi on-disk format | JSONL. The first line is a `session` header (version 3). Every other line is an entry with `type`, `id` (usually 8-char hex), `parentId`, `timestamp`.\[16\]\[17\] Path: `~/.pi/agent/sessions/--<path>--/<timestamp>_<session-id>.jsonl`\[2\] | documented: packages/coding-agent/docs/session-format.md |
| Which PDSes support Spaces | Reference image `ghcr.io/bluesky-social/atproto:pds-spaces-alpha`, plus the community implementations ZDS (Zig), the atproto-crates PDS (Rust), rsky PDS (Rust, Blacksky) and the HappyView AppView framework. All are alpha or partial.\[1\] | documented: atproto.com/blog/atproto-spaces-alpha (2026-08-20) |
| Reference PDS roadmap | The alpha image is "compatible with the reference PDS distribution". Bluesky's goal is "launching later this year". There is no committed GA date and no migration guarantee: "Do not expect that you'll even be able to cleanly upgrade between versions."\[1\] | documented: same post |
| Transcript standard adoption | None for interactive session sharing. Agent Trace is an attribution RFC; ATIF is used for eval/RL. | see WS3 |

---

# findings/ws1-atproto-foundations.md

**Records and size limits (documented, atproto.com/guides/data-validation)**
- The guide says: "try to keep individual records to a few dozen KBytes… A reasonable maximum record size limit (MAX_CBOR_RECORD_SIZE) is 1 MiByte."\[18\]
- The `subscribeRepos` `#commit` block is limited to 2,000,000 bytes, "so only a single 1 MiByte record can be created or updated per commit."\[18\]
- The JSON-encoding guidance is 2 MiB.\[18\]
- Implication: a session cannot be one record. Tool outputs must be split out.

**Blobs (documented)**
- The reference PDS raised its default maximum blob size to 300 MB for *new* installs (`PDS_BLOB_UPLOAD_LIMIT=314572800`). Existing installs keep their old value.\[19\]
- The limit is advertised through `describeServer.blobUploadLimit` (atproto.com/blog/pds-customization-and-metrics).\[19\]
- Lexicons can set their own blob caps. Tangled's artifact lexicon caps at 50 MB (reported, github.com/qjoly/mise-tangled).\[20\]
- Per-PDS limits vary, so read `describeServer` at runtime.
- The total-storage quota is unlimited in the reference PDS (reported, bluesky-social/atproto#3392).\[21\]

**Deletion and the firehose**
- Public repo writes are rebroadcast by relays ("a global firehose anyone can tap into"; documented, Spaces alpha post).\[1\]
- A delete is just a new commit. Copies already taken by relays, AppViews, archivers and mirrors are outside your control.
- Our conclusion: GDPR-style erasure cannot be promised for anything written publicly.
- This is the main reason the MVP must not use public repos for transcripts.

**Lexicon, NSID authority and resolution (documented)**
- NSID authority comes from DNS.
- Lexicon resolution goes from the `_lexicon` TXT record, to a DID, to a `com.atproto.lexicon.schema` record. This is described in the permission spec and in cocoon's Go implementation (pkg.go.dev/github.com/haileyok/cocoon/oauth/scopes).\[22\]
- Lexicon evolution is strict. Bluesky staff describe the "social contract" that published constraints cannot be tightened (reported, bluesky-social/atproto discussions #1740, #4832).\[23\]\[24\]
- Implication: publish v1 schemas conservatively, with open unions everywhere.

**Auth (documented, atproto.com/specs/permission, guides/permission-sets)**
- Granular OAuth scopes exist: `repo:<nsid>`, `rpc:<lxm>?aud=`, `blob:`, `account:`, `identity:`, and `include:<permission-set>`.\[22\]\[25\]
- Permission sets are lexicons, resolved and cached by the authorization server.\[26\]
- Spaces adds a `space:` OAuth scope (documented, proposal 0016 snippet).\[27\]
- Recommended use:
  - CLI and pi extension: OAuth via a loopback client (public client, DPoP).
  - bb plugin: the same, run in the plugin server.
  - Headless runners: app passwords are expedient but over-privileged. Avoid them for anything touching Spaces.
- Unknown: how mature `@atproto/oauth-client-node` is for long-lived CLI refresh, specifically with Spaces credentials. This is spike-worthy.

**Sync and AppView**
- For public data: relays, firehose, Jetstream.
- For Spaces: "there is no concept of a relay for data stored in a space… Applications will sync space data directly from PDS hosts" (documented, alpha post).\[1\] An HN commenter confirms the sync protocol is "pull from PDS" (reported).\[28\]
- So a team AppView for Spaces is a *per-writer puller*, not a firehose consumer. That actually fits the shape of a small-team product better.
- Not researched: `@atproto/tap` and the Sync v1.1 details. The search budget ran out, so these are listed as unknown.

**Feeds**
- Bluesky feed generators return skeletons of `app.bsky` post URIs.
- Our assessment (reported/inference, not verified): a non-Bluesky app with its own record types gains little from reusing them. Build a small team-feed endpoint in your own AppView.

**Moderation**
- Proposal 0016: "A moderation service should not publish public labels for records in permissioned spaces, as this leaks metadata" (documented snippet).\[27\]
- So labelers/Ozone are not a secret-leak control for private sessions. Their role is limited to public sessions.

**Open questions**
- PDS write rate limits for bursts of thousands of records. Not researched.
- Tap/backfill maturity.
- Whether Spaces blobs (`com.atproto.space.getBlob`) honour the same size limits.

---

# findings/ws2-spaces-groups.md (highest risk)

**What Spaces is (documented: alpha post 2026-08-20; proposal 0016; Holmgren's "Reintroducing Spaces")**
- A space is identified by space type (NSID), space key and a space authority (DID).\[29\]
- Records live in per-space permissioned repos on each *author's* PDS.\[1\]
- Readers present a credential, a JWT with `typ: atproto-space-credential+jwt`, issued by the authority.\[27\]
- Apps get a short-lived delegation token from the user's PDS. The `typ` is `atproto-space-delegation+jwt`. A Laravel SDK describes it as "a 60-second single-use delegation token" (reported, github.com/socialdept/atp-spaces).\[30\]
- Blobs are fetched with `com.atproto.space.getBlob`.\[27\]\[31\]
- Encryption: "E2EE is a separate concern that may be layered on top by an application and is out of scope" (documented, 0016 draft as quoted on discourse.atmosphere.community).\[32\]
- Leaked data: the draft says leaked data "is refutable (not strongly authenticated at rest)".\[32\]

**History and status**
- Proposal PR #94 (dholms) merged 2026-07-03 (reported, via kodamachi#228).\[33\]
- Renamed from "permissioned data" to "atproto spaces" in PR #115, 2026-09-25 (documented).\[34\]
- The reference implementation is in bluesky-social/atproto PR #5187 on a branch that "may temporarily diverge from the packages and PDS that are published".\[1\]
- Issue #5491 documents a mismatch between the proposal and the alpha API (reported via ewanc26/wolfram#35).\[35\]
- Alpha builds ship on Thursdays.\[1\]

**Rough edges third parties found (reported, socialdept/atp-spaces)**
- "`listSpaces` is a hint, not a roster."\[30\]
- "A member's per-space repo survives the space being deleted, as an empty shell no method removes."\[30\]
- "getDelegationToken also succeeds for spaces that never existed."\[30\]

**Atmospheric Groups (documented, atproto.com/blog/atmospheric-groups-intro, 2026-10-22)**
- "An atmospheric group is a DID with a bunch of permissioned spaces under it."\[29\]
- There is a `meta` space and a members space, `fyi.opensocial.members`.\[29\]
- Membership is two-way: the group writes `membership`, the member writes `acceptance`.\[29\]
- Permissions are "flat role-based access control"; "Each space has an `access` record listing which roles can read".\[29\]
- Write rules are left to app lexicons.\[29\]
- The group host acts as "an OAuth authorization server for the group DID".\[29\]
- Grain's records used `opensocial.fyi`, "an early revision of opensocial.group".\[29\] The NSIDs are already in flux.
- Usable "today if you're [on] a spaces-enabled PDS".\[29\]
- Competing or adjacent community designs: Brittany Ellich's opensocial.community, and Zicklag and Meri's "Arbiter" (reported, discourse.atmosphere.community).\[36\]\[37\]\[38\]

**Mapping our needs**
- One group DID per team or company.
- One space per *project*, with space type `works.ensemble.project` and space key = project slug.
- "Share all sessions in a folder" = write into the project space.
- "Share a single session" = a one-off space, with key = session TID, and a member list containing the invitees.
- Per-session ACLs inside a project space are not expressible, because access is per space. You must create a separate space for each exception.

**Revocation (inference from documented design)**
- Removing a member stops *new* credential issuance.
- Anything the ex-member's client or any AppView already pulled stays readable to them.
- The ex-member's *own* authored records remain in *their* PDS.
- So "someone leaves the team" means they keep whatever they synced and they keep their own contributions. There is no protocol-level remote wipe.

**Fallbacks if Spaces slips**

| Option | Security | UX/ops cost | Verdict |
|---|---|---|---|
| Private stock PDS on a team network (VPN/Tailscale), never `requestCrawl`'d, plus a private AppView | Network perimeter only; standard ATProto signing; no relay exposure | One PDS per team; accounts on it are "team identities" separate from personal Bluesky identities | **Least-bad interim.** |
| E2EE blobs in public repos | Ciphertext is permanently in the firehose (harvest-now-decrypt-later); metadata such as record existence, timing and size leaks; past data cannot be revoked | Key management (MLS/Germ) not researched; heavy | Reject for MVP. |
| Off-protocol store (S3, etc.) plus on-protocol pointer records | Pointers leak metadata if public | Simple, but not "protocol-native" | Acceptable for large artefacts only. |
| Spaces alpha on a self-hosted `pds-spaces-alpha` | No security review; breaking schema changes\[1\] | Re-provision on upgrades | Dogfood only, with synthetic or non-sensitive sessions. |

**People to follow (documented authorship)**
- Daniel Holmgren (dholms), author of the Spaces proposal and blog.\[1\]\[39\]
- Bryan Newbold (bnewbold), reviewer and the auth-scopes work.\[39\]
- Brittany Ellich (opensocial.community).
- Zicklag and Meri (Arbiter).
- The Grain team.

---

# findings/ws3-session-formats.md

**pi (documented, session-format.md)**
- Header: `{"type":"session","version":3,"id","timestamp","cwd","parentSession?"}`.\[2\]
- Entry types: `message`, `model_change`, `thinking_level_change`, `usage`, `compaction` (with `firstKeptEntryId`, `summary`, `tokensBefore`, optional `systemMessage`), `context_edit`, `branch_summary` (`fromId`), `custom` (not in context), `custom_message` (in context), `label`, `session_info`.\[2\]
- System messages persist "every prompt section and tool declaration" on the first request, then patches after that.\[2\]
- Implication: the *system prompt and tool schemas are inside the transcript*. That includes `cwd`, skill contents, and possibly internal tooling descriptions.
- Multiple roots are possible (`resetLeaf()`).\[2\]
- Message timestamps are Unix ms; entry timestamps are ISO.\[2\]
- Versions: v1 linear, v2 tree, v3 renamed `hookMessage`→`custom`. Migration happens automatically on load.\[2\]

**bb**
- Normalised thread events are stored in SQLite.\[40\]
- When bb runs pi, the pi JSONL lives at `~/.bb/pi-bridge-sessions/pi_<uuid>.jsonl`. It is "format-identical to a native Pi session", and there is no `~/.pi/agent/sessions` dir for bb workspaces (reported, regutierrez/traicr#37; jgarrow-springhealth/bb-plugin-pi-usage).\[8\]\[41\]\[42\]
- **Consequence:** a file-watcher on `~/.pi/agent/sessions` silently misses every pi session run inside bb.

**Others (Claude Code JSONL under `~/.claude/projects`, Codex rollouts, opencode, Cursor, Aider, Amp, Gemini CLI, Goose, Zed, Cline/Roo)**
- Not individually researched in this pass. Listed as unknown.
- ATIF tooling claims producers exist for Claude Code, Codex, Gemini CLI and OpenHands via Harbor adapters (reported, Arize Phoenix docs).\[43\]

**Standards**
- **Agent Trace**
  - Cursor, RFC v0.1.0, January 2026. A JSON "trace record" links code ranges to conversations, with contributor type human/ai/mixed/unknown and a `conversation.url` (documented, github.com/cursor/agent-trace).\[44\]\[45\]
  - Cognition's 30 Jan 2026 blog post names the supporters: "Cursor, Cloudflare, Vercel, git-ai, Google Jules, Amp, OpenCode and others".
  - Thoughtworks Technology Radar Vol. 34 (April 2026) places it in Assess and notes "early signals of adoption, with support from tools such as Cline and OpenCode as well as implementations like Git AI."
  - It does not carry transcripts.
- **ATIF (Agent Trajectory Interchange Format)**
  - Harbor's current version is ATIF-v1.7, and Harbor accepts v1.0–v1.7 (documented, docs.harborframework.com).\[46\]
  - Conflict: one importer claims v1.0–v1.8 (reported, ChristopherDavenport/agentimport#11).\[47\]
  - It is a flat `steps` list plus `subagent_trajectories`, and has *no tree/branching*.\[43\]\[46\]
  - Consumers: Phoenix, Opik, agentpile.\[43\]\[48\]\[49\]
  - An OTel GenAI semconv issue (#338) tracks ATIF↔OTel mapping gaps.\[50\]
- **ACP**: pi-acp adapters bridge ACP to `pi --mode rpc` (reported, github.com/svkozak/pi-acp).\[51\]\[52\] bb exposes ACP exports in its provider-bridge API (reported).\[53\]
- Verdict: adopt none as the canonical model. Export ATIF (lossy: it flattens branches) and emit Agent Trace records that link back to your session AT-URIs.

**Common-denominator model (feeds lexicon-sketch)**
- Session: harness, version, model(s), cwd fingerprint, git context.
- Entry tree: id, parentId, kind.
- Kinds: message (role, content blocks: text/image/thinking), toolCall (name, args), toolResult (isError, content or blob), fileEdit (path, diff), shell (cmd, exit, stdout/stderr blob), modelChange, compaction (summary, firstKept), branchSummary, label, usage (tokens, cost), and harness-specific `custom` as an open union.

**Session sizes**
- We found no published measurement of real pi or bb session sizes. See Spike 2.

---

# findings/ws4-harness-integration.md

**pi extension capabilities (documented: pi.dev/docs/latest/extensions; examples README)**
- (a) **Observe live.** The lifecycle runs `session_start → input → before_agent_start → agent_start → turn_start → context → before/after_provider_request → tool_execution_start → tool_call → tool_result → turn_end → agent_end → agent_settled`.\[54\] `provider_stream_event` fires per parsed stream event.\[55\]
- (b) **Read/write the tree.**
  - `pi.appendEntry()` persists custom entries.\[55\]
  - `setLabel` and `setSessionName` exist.\[56\]
  - The `SessionManager` API is in `packages/coding-agent/src/core/session-manager.ts`.\[2\]
  - DeepWiki cites lines 144–153 for `SessionEntry` and 575–602 for `getTree()`.\[57\] This is reported, the commit is unknown, and the numbers will drift.
- (c) **Inject remote messages.**
  - `pi.sendUserMessage(content, {deliverAs: "steer"|"followUp"})`.\[4\]
  - `pi.sendMessage({customType, content, display}, {deliverAs, triggerTurn})`.\[3\]
  - The `input` event exposes `event.source` = `"interactive" | "rpc" | "extension"`.\[3\]
- (d) **Gate tools.** `tool_call` can mutate input or return `{block:true, reason}`. Errors in `tool_call` handlers fail closed ("tool_call errors block the tool (fail-safe)"). There is a permission-gate.ts example.\[4\]\[55\]

**Share prior art (documented, pi.dev/docs/latest/usage & sessions)**
- `/share` uploads to a "Radius artifact" visible to "your Radius organization" when Radius auth is configured, and otherwise to a private (secret) GitHub gist.\[58\]\[59\]
- A `sessionShareDestination` setting forces either one.\[59\]
- We did not research what Radius is. It is a direct competitor or partner to evaluate: the pi maintainers already ship org-scoped sharing.
- The HTML exporter is not publicly exported to extensions; pi-share-slice works around this through `getPackageDir()` (reported, gpxl-dev/pi-share-slice).\[60\]
- Conflict: a third-party guide claims `/share` content "is sanitized for credentials" (reported, piagent.fyi). The official docs only say "Review the session first because it can contain… credentials".\[58\]\[61\] Assume no sanitisation.

**pi headless modes**
- RPC mode uses "strict LF-delimited JSONL framing".\[62\]
- Child processes see `PI_SESSION_ID` and `PI_SESSION_FILE` (documented, npm README).\[62\]
- Both are viable for a "remote participant runner".

**bb (documented unless noted)**
- Server/host-daemon/app/CLI split. Contracts live in `@bb/server-contract` and `@bb/host-daemon-contract`.\[6\]\[40\]
- **Plugin surfaces:**
  - lifecycle events
  - dispatch hook
  - provider bridges
  - host workers
  - per-thread private JSON metadata
  - plugin storage
  - HTTP/WebSocket/RPC/realtime
  - thread side-panel tabs, message actions, in-thread forms
  - "The bb SDK"\[13\]
- **Dispatch hook.**
  - `bb.experimental_hooks.on("message.dispatch", handler)` can "proceed, wait, or reject" (changelog 0.41.0).\[63\]
  - Since 0.43.3 the payload uses `queuedMessages`, `initiator`, `senderThreadId`.\[63\]
  - It is *experimental*. bb's own time budget is unknown. The community Hooks plugin self-imposes 8 s (reported, get-bb/marketplace#410).\[64\]
- **Event history.**
  - `bb thread log --all` reads full history (changelog 0.40.0).\[63\]
  - The plugin-authoring skill references "event history" in the backend SDK (reported).\[53\]
  - A plugin author confirms threads can be watched from a plugin but "a thread's events can only be read on its owner's server" (reported, get-bb/bb#4214, read at a60b895).\[65\]
- **Injecting into threads.**
  - `bb thread tell <id>` works from a plugin service.\[9\]
  - **But** it arrives with `initiator:"user"`, `senderThreadId:null`, and "There is no way for a plugin to name itself as the sender" (reported, get-bb/bb#3621).\[9\]
  - For remote participation this is a provenance hole: remote input is indistinguishable from the owner typing.
- **How pi runs in bb.**
  - Plugin `plugins/provider-pi/`. bb launches pi in RPC mode with a bundled extension,\[7\] at `plugins/provider-pi/src/bridge/rpc-session.ts#L196-L223` @ `9a47d42` (reported via get-bb/bb#5254, which links source).\[66\]
  - Known fragility:
    - `thread/resume` hit a 30 s JSON-RPC default on large pi sessions (get-bb/bb#5080, bb 0.45.0).\[67\]
    - A stale extensionPath failed on resume (#5350).\[68\]
    - Earlier, the bridge did not pass Pi's `ExtensionUIContext` (#1668).\[69\]
  - Implication: pi extensions that rely on `ctx.ui.confirm()` (such as permission gates) may not behave the same inside bb. Current status unknown.
- **Security note.** bb's own README warns that `pnpm dev:remote` exposes a server API that "is unauthenticated and permits command execution and file reads".\[11\]
- **Contribution policy.**
  - PR #5522, merged 2026-10-14 (c01608d), changed the policy. Outside contributors open the PR with "Allow edits by maintainers" on, "expect the gate to close it", then request approval on Discord to join `.github/APPROVED_CONTRIBUTORS`.\[10\]
  - Issues-first is expected for UI and contract changes (reported via issues #4809, #5552).\[70\]\[71\]
- **Scale and velocity.** Roughly 7,040 commits, 4.5k stars, 680 forks, 556 open issues at access time (documented, repo page).\[11\] A long-lived fork would rot quickly.

**Generic harness support, ranked by fidelity × coverage**
1. **Native adapters** (pi extension, bb plugin): highest fidelity, including the tree, and live.
2. **File watchers on known session dirs**: works for any harness with on-disk logs, but must know bb's relocation of pi sessions and every harness's format. Not live for steering.
3. **ACP proxy/tap**: harness-neutral for ACP agents, but sees only the ACP view (no compaction internals, no branches).
4. **OTel exporter**: spans lose content unless configured, and there is no tree.

**Language.**
- TypeScript is right for the core: pi extensions are TS, bb plugins are TS, and `@atproto/*` plus the alpha Spaces SDK are TS-first ("alpha snapshot versions… installed with the alpha tag").\[1\]
- A Rust/Go single binary only wins for the file-watcher daemon. Defer it.

---

# findings/ws5-participation-safety.md

**Participation spectrum and our recommended gate:**
1. Comment/annotate. Pure records, no execution. **MVP.**
2. Suggest a prompt. A record the owner sees; the owner clicks "send". **v1.**
3. Queue a steer. Delivered via `sendUserMessage` only after per-message owner approval. **v2, behind an explicit opt-in.**
4. Co-drive. Execution on the owner's machine. **Not recommended** without a sandboxed environment.
5. Fork-and-run. Participant replays the session into their own sandbox. **Recommended alternative to 4.**

**Why 3–4 are dangerous**
- A remote reply injected as a user message is, by construction, a prompt-injection channel with the owner's full tool permissions.
- A coding agent with the owner's filesystem, network and secrets satisfies all three legs of Simon Willison's "lethal trifecta" (simonwillison.net, 16 June 2025): private data, untrusted content and external communication, a combination where "an attacker can easily trick it into accessing your private data and sending it to that attacker."
- bb's provenance gap (#3621) means even the *UI* would not show that a remote party sent it.

**Mitigations**
- **Fail-closed gating.** Use pi `tool_call` blocking or the bb dispatch hook.
- **Distinct custom message type.** Inject remote text as `sendMessage({customType:"ensemble.remote", display:true})` and wrap it in an explicit "untrusted remote input from @handle" envelope, rather than as a raw user message.
- **Per-reply capability scoping.** Use `pi.setActiveTools(["read"])` for the turn.
- **Sandboxing for fork-and-run.** Containers, gVisor, Firecracker, Seatbelt/Landlock, or hosted E2B/Daytona/Modal. These are not evaluated here.
- **Signed provenance.** ATProto record signatures plus an AT-URI on every injected message.

**Redaction (published measurements)**
- Basak et al., "A Comparative Study of Software Secrets Reporting by Secret Detection Tools" (arXiv 2307.00714), on SecretBench (documented):\[72\]
  - Precision: GitHub Secret Scanner 75%, Gitleaks 46%.\[72\]
  - Recall: Gitleaks 88%, SpectralOps 67%, TruffleHog 52%.\[72\]
  - TruffleHog's precision was 6% before `--only-verified`.\[72\]
- In the same study, TruffleHog's `--only-verified` mode raised its precision from 6% to 90% but reported only 611 secrets. Verification itself still showed 10% false positives, and "TruffleHog does not report an active secret if the API endpoint is unreachable."
- No study measures transcripts specifically. Transcripts mix env dumps, stack traces, `.env` reads and base64 tool output, so expect worse.
- Policy:
  - Run redaction client-side, before upload, as a union of detectors plus entropy.
  - Show an interactive diff.
  - Default to excluding raw tool-result bodies for `read` and `bash` of files matching `.env*`, `*.pem`, `id_*`, and similar.

---

# findings/ws6-feeds-social-ux.md

**Feed events**
- `session.started`, `session.shared`, `milestone` (owner-labelled; maps to pi `label` entries), `help.requested`, `pr.opened` (git context), `reply.posted`, `suggestion.accepted`.
- Rank chronologically within a team. Notify only on `help.requested` and on replies to your own sessions.

**Viewer essentials**
- Collapse tool output by default.
- Render diffs.
- Branch navigator (pi's tree is the differentiator).
- Jump to labels and compactions.
- Show the system-prompt/tools checkpoint as a collapsible "context" panel.
- Base it on pi's HTML export look, which already handles tree, thinking and tool rendering (documented, pi docs; reported, pi-share-slice).

**Social dynamics**
- The pi npm README explicitly asks OSS users to "share your coding agent sessions" because "Public OSS session data helps improve models, prompts, tools, and evaluations" (documented).\[62\]
- So a norm of public sharing exists, and it is entangled with model training. Teams will need a visible "not for training" stance.
- Not researched: mob/ensemble programming literature, Amp/Cursor/Claude Code share UX, SpecStory. These are open items.
- Risk to flag: performative sharing ("curated" sessions) undermines the documentation value. Default to sharing whole sessions with redactions, not edited highlights.

---

# findings/ws7-landscape-prior-art.md

**Tangled**
- Git on ATProto.
- Social records live under `sh.tangled.*` in users' PDSes. Git data lives on self-hostable "knots", which are "essentially our extension to the AT architecture… off-protocol data".\[73\]
- Its AppView is stateful and synchronises via NATS (reported, HN 45543899).\[73\]
- Lesson: large or binary payloads go off-protocol to a user-hostable sidecar. This is directly analogous to session blobs.

**Grain**
- The first production Groups user, on spaces-enabled PDSes only.\[29\]

**Session-sharing products**
- pi `/share` (gist or Radius), and community viewers (pi-sessions-viewer, pi-share-slice).
- Agent Trace partners link to conversations by URL.\[45\]
- Not researched: pricing and fate of SpecStory, Amp threads and the like.

**Legal**
- Not researched. Open items: transcript ownership, provider ToS on sharing outputs, GDPR erasure versus content-addressed and replicated data, and company DLP policies.
- The firehose deletion problem means any EU deployment must keep personal data in Spaces or on a private PDS, not in public repos.

---

# landscape.md

| Name | Link | What | Licence | Maturity | Relevance | Reuse |
|---|---|---|---|---|---|---|
| pi coding agent | github.com/earendil-works/pi | Harness; JSONL tree sessions; extensions; RPC/SDK | MIT | Active, stable | High | Extension + format |
| bb | github.com/get-bb/bb | Agent IDE; SQLite threads; plugins; runs pi via RPC\[7\]\[11\] | MIT | Active, "core architecture is stable"\[11\] | High | Plugin |
| bb-lite | github.com/get-bb/bb-lite | Single-process bb variant, separate data dir\[74\] | Unknown | Early | Low | Watch |
| ATProto Spaces (0016) | github.com/bluesky-social/proposals | Permissioned repos | Spec | Alpha | High | Target store |
| pds-spaces-alpha image | ghcr.io/bluesky-social/atproto:pds-spaces-alpha | Spaces-capable reference PDS | MIT/Apache (not re-checked) | Alpha | High | Dogfood |
| opensocial.group | tangled.org/opensocial.group/proposal | Group model on Spaces | Unknown | Proposal, in flux | High | Adopt for teams |
| rsky / atproto-crates / ZDS | see alpha post | Alt PDSes with Spaces work | Various | Alpha | Med | Interop tests |
| HappyView | happyview.dev | AppView framework with experimental Spaces | Unknown | Experimental | Med | Possible AppView base |
| cocoon | github.com/haileyok/cocoon | Go PDS with OAuth scopes | Unknown | Active | Low | Reference |
| Tangled | tangled.org | Git on ATProto, knots | Unknown | Production | High (pattern) | Knot pattern |
| Grain | grain.social | Photo app using Groups | Unknown | Production | Med | Reference |
| Agent Trace | github.com/cursor/agent-trace | Code-attribution records | Open spec | RFC v0.1.0 | Med | Emit links |
| ATIF | docs.harborframework.com | Trajectory JSON for eval | Unknown | v1.7 | Med | Export |
| pi-acp | github.com/svkozak/pi-acp | ACP↔pi RPC adapter | Unknown | Community | Med | ACP path |
| bb-plugin-hooks | github.com/MacHatter1/bb-plugin-hooks | Dispatch-gate plugin example | Unknown | Community | Med | Template |
| pi-share-slice | github.com/gpxl-dev/pi-share-slice | Partial session share via pi HTML | Unknown | Community | Med | Viewer reuse |
| Gitleaks / TruffleHog / detect-secrets | — | Secret scanners | MIT / AGPL / Apache (not re-checked) | Mature | High | Redaction layer |
| Basak et al. 2023 | arxiv.org/abs/2307.00714 | Scanner precision/recall | — | Paper | High | Evidence |
| Kleppmann et al. 2024 | arXiv 2402.03239 | ATProto design paper | — | Paper | Med | Background (not re-read) |

---

# lexicon-sketch.md

The namespace `works.ensemble.*` is a **placeholder**. You must control the matching DNS domain, because NSID authority is DNS-based. All `kind`/`content` fields are **open unions** so harness-specific entries survive.

```json
{ "lexicon": 1, "id": "works.ensemble.session",
  "defs": { "main": { "type": "record", "key": "tid", "record": { "type": "object",
    "required": ["harness","createdAt"],
    "properties": {
      "harness": { "type": "object", "properties": {
        "name": {"type":"string"}, "version": {"type":"string"},
        "sourceFormat": {"type":"string"} }},
      "title": {"type":"string","maxLength":300},
      "project": {"type":"string","description":"project slug; never raw cwd"},
      "git": { "type":"object", "properties": {
        "repo":{"type":"string"},"branch":{"type":"string"},
        "commit":{"type":"string"},"dirty":{"type":"boolean"} }},
      "models": {"type":"array","items":{"type":"string"}},
      "rawArchive": {"type":"blob","accept":["application/jsonl","application/zstd"]},
      "redaction": {"type":"ref","ref":"#redactionReport"},
      "createdAt": {"type":"string","format":"datetime"} } } } } }
```

```json
{ "lexicon": 1, "id": "works.ensemble.session.chunk",
  "defs": { "main": { "type":"record","key":"any","record":{"type":"object",
    "required":["session","seq","entries"],
    "properties":{
      "session":{"type":"ref","ref":"com.atproto.repo.strongRef"},
      "seq":{"type":"integer"},
      "entries":{"type":"array","maxLength":500,"items":{"type":"ref","ref":"#entry"}} }}},
    "entry": { "type":"object","required":["id","kind","ts"],
      "properties":{
        "id":{"type":"string"},"parentId":{"type":"string"},
        "ts":{"type":"string","format":"datetime"},
        "kind":{"type":"union","refs":["#message","#toolCall","#toolResult",
          "#fileEdit","#compaction","#branchSummary","#label","#modelChange","#usage"]},
        "payloadBlob":{"type":"blob","description":"outputs > 16 KB"} } } } }
```

**Other records**
- `works.ensemble.share`: subject (session strongRef or project), audience (space ref / DIDs), and mode (`read` | `comment` | `suggest`).
- `works.ensemble.feed.event`: type (open string), subject, summary.
- `works.ensemble.reply`: subject = session strongRef + `entryId`; `intent` = `comment` | `suggestPrompt` | `steerRequest`; text.
- `works.ensemble.approval`: owner-written; references a reply; `decision`; resulting `entryId`. This makes "who caused this turn" auditable from both repos.

**Design alternatives**
- **Per-entry records**: perfect granularity and live streaming, but thousands of commits per session and rate-limit exposure (unknown limits).
- **Chunked records** (recommended): batches of ≤ 500 entries kept under ~200 KB, plus large payloads as blobs and a raw JSONL archive blob for lossless round-trip.
- **Single snapshot blob plus index record**: simplest, but no partial reads or live view.
- Keep `cwd` out of records: pi system messages embed `cwd`, so redact them.

---

# architecture-options.md

**A. Private team PDS + private AppView (recommended MVP)**
```
[pi ext]/[bb plugin]/[CLI] --redact--> OAuth --> Team PDS (stock, VPN-only, no requestCrawl)
                                                   |  pull (listRecords/getRepo)
                                         Team AppView (TS, SQLite/Postgres) --> Web viewer + feed
```
- Build: lexicons, capture adapters, redaction, AppView, viewer.
- Reuse: stock PDS, `@atproto/*`.
- Risks: the network perimeter is the only ACL; the identity is a team-PDS identity.
- Effort: about 8–10 engineer-weeks (estimate).

**B. Spaces-native (target state)**
```
author PDS (spaces) --space repo--> group DID host (credentials, writer set)
       AppView pulls each writer's space repo with space credential --> viewer/feed
```
- Same lexicons; the swap is in the storage adapter.
- Risks: alpha churn, no security review, revocation semantics.
- Effort: +4–6 weeks on top of A once Spaces is GA (estimate).

**C. Public-only (OSS sessions)**
- The same records in a public repo, firehose and Jetstream.
- Only for explicitly public OSS sessions, after a mandatory redaction review.
- Effort: small on top of A.

**D. E2EE blobs in public repos (rejected)**
- Permanent ciphertext, metadata leak, no revocation of past data, and unresearched key management.

---

# integration-pi.md

**Hook points (documented docs; line refs reported)**
- `session_start`: read `ctx`/session file, register share state.
- `turn_end` / `agent_settled`: flush new entries to chunks, debounced.
- `tool_call`: gate for remote-originated turns.
- `input` with `source:"extension"`: tag remote input.
- `registerCommand("ensemble-share")`.
- `registerEntryRenderer("ensemble.remote")`.
- `appendEntry("ensemble", {...})`: record the AT-URIs of published chunks for idempotent resumption.

**Source**
- `packages/coding-agent/src/core/session-manager.ts` (SessionManager).
- `packages/coding-agent/src/core/extensions/types.ts` (tool_call ~L250–255 per DeepWiki, commit unknown).\[75\]

**PoC**
1. An extension that, on `agent_settled`, reads `PI_SESSION_FILE`, diffs against the last published entry id, and writes chunk records to a local PDS.
2. Verify round-trip by regenerating the JSONL from records and byte-comparing entries.
3. Run inside bb to confirm the extension loads under provider-pi. Unknown: whether bb loads user pi extensions at all.

---

# integration-bb.md

**Hook points**
- **Lifecycle events**: thread start/finish triggers feed events.
- **SDK event history** and `bb thread log --all`: export bb-native threads, covering non-pi providers.
- **`message.dispatch` hook**: hold remote-originated messages until owner approval.
- **Thread side-panel tab**: a "Shared / Replies" panel.
- **Per-thread metadata**: share state.
- **For pi threads**: read `~/.bb/pi-bridge-sessions/pi_<uuid>.jsonl` for full-fidelity tree data.

**Source refs (reported via issues)**
- `plugins/provider-pi/src/bridge/rpc-session.ts` (@9a47d42 L196–223).
- `packages/provider-bridge-protocol/src/thread-delta.ts`.
- `packages/provider-bridge-protocol/src/bridge-kit/runtime-json-rpc.ts`.

**What a plugin cannot do today (reported)**
- (1) Name itself as message sender (#3621).\[9\]
- (2) Read threads on another bb server (#4214).\[65\]
- (3) Possibly surface pi extension UI prompts (#1668, status unknown).\[69\]

**Fork assessment**
- **No fork for read-only sharing.** For participation, upstream a `senderPluginId`/`--as-plugin` change.
- Cost of a fork: rebasing against roughly 7k-commit, multi-release-per-week velocity. High.
- Upstreaming path: open an issue first, then a PR with maintainer edits on, then Discord approval.\[10\]

---

# threat-model.md

| Asset | Actor | Attack path | Mitigation |
|---|---|---|---|
| Secrets in transcripts | Any reader, AppView operator, ex-member | Publish → sync → cached copies | Client-side redaction plus review; private PDS/Spaces only; raw archive blob opt-in |
| Owner's machine | Remote participant / injected content | Reply → steer → tool call | No execution in MVP; approval records; fail-closed tool gating; custom untrusted envelope; fork-and-run in sandbox |
| Provenance | Impersonator | Plugin `tell` appears as the user\[9\] | Signed reply records + approval record; upstream sender field |
| Team membership | Departed member | Retained synced data | Accept as residual; short credential TTL; rotate exposed secrets on departure |
| Metadata | Public observers | Public pointers/labels | No public records for private sessions; no public labels (0016 guidance) |
| Supply chain | Malicious shared extension/skill | Shared session recommends an install | Never auto-install from sessions; display only |
| bb server | LAN attacker | `dev:remote` unauthenticated API\[11\] | Never expose bb's server for participation; use our own authenticated channel |

---

# risks-and-unknowns.md (ranked)

1. **Spaces not production-ready within 12 months, or semantics change.** Evidence: alpha, breaking changes, divergent branch, Groups NSIDs already renamed. *Spike 1.*
2. **Secrets leak despite redaction.** Evidence: in Basak et al.'s 2023 study, the best precision (GitHub Secret Scanner, 75%) and the best recall (Gitleaks, 88%) come from different tools, and "no current tool has the coveted high precision and high recall scores"; transcripts are untested. *Spike 2.*
3. **Upstream churn breaks adapters.** Evidence: pi format v1→v3; bb dispatch hook "experimental" and renamed fields in 0.43.3;\[2\]\[63\] bb pi-bridge bugs #5080 and #5350. *Spike 3 plus contract tests.*
4. **Pi `/share` with Radius makes us redundant for pi-only teams.** Unresearched.
5. **Session sizes exceed practical PDS limits/rate limits.** No data. *Spike 2.*
6. **Legal/ToS/GDPR.** Not researched.

---

# recommendation.md

**MVP scope**
- Read-only sharing of whole sessions and project folders to a team.
- Comments and "suggested prompts" that the owner manually sends.
- A team activity feed.
- No remote execution.

**Stack**
- TypeScript throughout.
- Stock PDS on a private network (Architecture A).
- Storage-adapter boundary so Spaces (B) is a swap.
- pi extension first, then a bb plugin, then a file-watcher.

**Spikes**
1. **Spaces round trip.**
   - On a self-hosted `pds-spaces-alpha` with 3 accounts and a group DID: write chunk + blob, read as a member, remove the member, attempt a read, and enumerate what the ex-member still holds.
   - Settles it: whether revocation and blob access behave as documented.
2. **Corpus measurement plus redaction.**
   - Script over `~/.pi/agent/sessions`, `~/.bb/pi-bridge-sessions`, and `~/.claude/projects` on ≥ 5 volunteers.
   - Measure: bytes, entries, max entry size, and the share of bytes in tool results.
   - Seed 50 canary secrets, then run gitleaks, TruffleHog and detect-secrets, and record precision and recall.
   - Settles it: chunk sizing, and whether redaction can be default-on.
3. **Dual capture.** A pi extension and a bb plugin publish the same session to a local PDS; the viewer renders both identically.
   - Settles it: adapter fidelity, and whether bb loads user pi extensions.

**Recorded disagreement**
- One position: build directly on Spaces now, because GA is targeted for "later this year"\[1\] and the product is 12+ months out.
- The majority position: don't let the alpha carry secret-bearing data. Ship A, and design lexicons so B is a migration, not a rewrite.
- Both sides agree that public-by-default is unacceptable.

## Sources

1. [The Atproto Spaces Alpha is Live - AT Protocol](https://atproto.com/blog/atproto-spaces-alpha)
2. [pi/packages/coding-agent/docs/session-format.md at main · earendil-works/pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/session-format.md)
3. [Extensions](https://pi.ubitools.com/extensions/)
4. [Extensions - pi](https://hochej.github.io/pi-mono/coding-agent/extensions/)
5. [bb/docs/configuration.md at main · get-bb/bb · GitHub](https://github.com/get-bb/bb/blob/main/docs/configuration.md)
6. [bb/docs/system-overview.md at main · get-bb/bb · GitHub](https://github.com/get-bb/bb/blob/main/docs/system-overview.md)
7. [GitHub - Diffuzmetall/bb-plugin-pi-command-sync: Native command sync addon for the existing BB Pi provider; requires the documented BB 0.45 compatibility adapter. · GitHub](https://github.com/Diffuzmetall/bb-plugin-pi-command-sync)
8. [Collect Pi traces from bb bridge sessions (\~/.bb/pi-bridge-sessions) · Issue #37 · regutierrez/traicr · GitHub](https://github.com/regutierrez/traicr/issues/37)
9. [Plugin-originated thread messages are indistinguishable from user input (initiator=user, senderThreadId=null) · Issue #3621 · get-bb/bb · GitHub](https://github.com/get-bb/bb/issues/3621)
10. [Ask contributors to open the PR first, with maintainer edits on by ymichael · Pull Request #5522 · get-bb/bb](https://github.com/get-bb/bb/pull/5522)
11. [GitHub - get-bb/bb: The agent IDE that builds itself](https://github.com/get-bb/bb)
12. [bb: agentic IDE · The IDE that builds itself](https://getbb.app/)
13. [Plugin Guide — bb](https://getbb.app/plugin-guide)
14. [pi Deep Dive: The Minimal Architecture Behind 95,000 GitHub Stars](https://www.developersdigest.tech/blog/pi-deep-dive-agent-toolkit-architecture)
15. [Pi Agent in Practice: Setup, Custom Extensions & 5 Best Practices - HoangYell](https://hoangyell.com/pi-agent-setup-best-practices/)
16. [pi-dev/packages/coding-agent/docs/sessions.md at main · auryan898/pi-dev · GitHub](https://github.com/auryan898/pi-dev/blob/main/packages/coding-agent/docs/sessions.md)
17. [pi.dev.details.md · GitHub](https://gist.github.com/rajeshpv/eccc1dc8d70e8cdcf948de3312ca111f)
18. [Data Validation - AT Protocol](https://atproto.com/guides/data-validation)
19. [Make the PDS Your Own: Customization and Metrics - AT Protocol](https://atproto.com/blog/pds-customization-and-metrics)
20. [GitHub - qjoly/mise-tangled: mise backend plugin: install binaries attached to tangled.org tags · GitHub](https://github.com/qjoly/mise-tangled)
21. [Add restrictions on blobstore consumption · Issue #3392 · bluesky-social/atproto · GitHub](https://github.com/bluesky-social/atproto/issues/3392)
22. [scopes package - github.com/haileyok/cocoon/oauth/scopes - Go Packages](https://pkg.go.dev/github.com/haileyok/cocoon/oauth/scopes)
23. [Consider raising the size limit of blobs · bluesky-social/atproto · Discussion #1740 · GitHub](https://github.com/bluesky-social/atproto/discussions/1740)
24. [Increasing Bluesky Post Image Size Limit · bluesky-social/atproto · Discussion #4832 · GitHub](https://github.com/bluesky-social/atproto/discussions/4832)
25. [feat(atproto): granular OAuth permissions, and trusted apps by karlitschek · Pull Request #2542 · AlohaSocial/social · GitHub](https://github.com/AlohaSocial/social/pull/2542)
26. [Permissions - AT Protocol](https://atproto.com/specs/permission)
27. [proposals/0016-permissioned-data at main · bluesky-social/proposals · GitHub](https://github.com/bluesky-social/proposals/tree/main/0016-permissioned-data)
28. [ATProto spaces: A new extension to ATProto that enables non-public data](https://news.ycombinator.com/item?id=49379732)
29. [An Intro to Atmospheric Groups - AT Protocol](https://atproto.com/blog/atmospheric-groups-intro)
30. [GitHub - socialdept/atp-spaces: Read and write permissioned AT Protocol data with Spaces in Laravel · GitHub](https://github.com/socialdept/atp-spaces)
31. [This Website is Hosted on Bluesky · Daniel Mangum](https://danielmangum.com/posts/this-website-is-hosted-on-bluesky/)
32. [Early permissioned data proposal draft feedback - WG Private Data - Atmosphere Community](https://discourse.atmosphere.community/t/early-permissioned-data-proposal-draft-feedback/923)
33. [Use permissioned data when it releases in atprotol · Issue #228 · karanshukla/kodamachi · GitHub](https://github.com/karanshukla/kodamachi/issues/228)
34. [0016: Consistently rename to atproto spaces by dholms · Pull Request #115 · bluesky-social/proposals · GitHub](https://github.com/bluesky-social/proposals/pull/115)
35. [feat(spaces): implement AT Protocol Spaces once upstream stabilises · Issue #35 · ewanc26/wolfram · GitHub](https://github.com/ewanc26/wolfram/issues/35)
36. [Representing groups in ATProto](https://brittanyellich.com/atproto-groups/)
37. [\[Proposal\] WG for group/community standards and infrastructure in ATProto - Discussion - Atmosphere Community](https://discourse.atmosphere.community/t/proposal-wg-for-group-community-standards-and-infrastructure-in-atproto/745)
38. [Arbiter: Group management for Permissioned Spaces - WG Private Data - Atmosphere Community](https://discourse.atmosphere.community/t/arbiter-group-management-for-permissioned-spaces/750)
39. [Permissioned data by dholms · Pull Request #94 · bluesky-social/proposals · GitHub](https://github.com/bluesky-social/proposals/pull/94)
40. [How bb, the programmable IDE for coding agents, is built](https://flaviocopes.com/bb-agentic-ide/)
41. [GitHub - VladimirGVP/bb-plugin-provider-pi-durable · GitHub](https://github.com/VladimirGVP/bb-plugin-provider-pi-durable)
42. [GitHub - jgarrow-springhealth/bb-plugin-pi-usage: See where Pi tokens and estimated costs go across providers, models, days, and BB or terminal sessions. · GitHub](https://github.com/jgarrow-springhealth/bb-plugin-pi-usage)
43. [Import ATIF Trajectories - Phoenix](https://arize.com/docs/phoenix/tracing/how-to-tracing/importing-and-exporting-traces/importing-atif-trajectories)
44. [Agent Trace: Cursor Proposes an Open Specification for AI Code Attribution - InfoQ](https://www.infoq.com/news/2026/02/agent-trace-cursor/)
45. [agent-trace/README.md at main · cursor/agent-trace · GitHub](https://github.com/cursor/agent-trace/blob/main/README.md)
46. [ATIF - Harbor documentation](https://docs.harborframework.com/core-concepts/agents/atif)
47. [Import ATIF trajectories by ChristopherDavenport · Pull Request #11 · ChristopherDavenport/agentimport · GitHub](https://github.com/ChristopherDavenport/agentimport/pull/11)
48. [GitHub - yzhao062/agentpile: Load public agent-trajectory datasets and agent traces into one ATIF-based run record · GitHub](https://github.com/yzhao062/agentpile)
49. [Evaluate LLM Agents with Harbor - Opik](https://www.comet.com/docs/opik/integrations/harbor)
50. [ATIF trajectory format used by Harbor · Issue #338 · open-telemetry/semantic-conventions-genai · GitHub](https://github.com/open-telemetry/semantic-conventions-genai/issues/338)
51. [GitHub - 0xSero/pi-acp · GitHub](https://github.com/0xSero/pi-acp)
52. [GitHub - svkozak/pi-acp: ACP adapter for pi coding agent · GitHub](https://github.com/svkozak/pi-acp)
53. [Bb Plugin Authoring (Grade A) - Claude Skill](https://www.skillsdirectory.com/skills/get-bb-bb-plugin-authoring)
54. [Extensions 101 — Guides](https://piagent.fyi/guides/extensions-101/)
55. [Extensions · Documentation · Pi](https://pi.dev/docs/latest/extensions)
56. [pi-extension-dev](https://lobehub.com/skills/kanatti-pipi-pi-extension-dev)
57. [Session Management and Compaction](https://deepwiki.com/earendil-works/pi/2.3-session-management-and-compaction)
58. [Use Pi in the terminal · Documentation · Pi](https://pi.dev/docs/latest/usage)
59. [Sessions and Context · Documentation · Pi](https://pi.dev/docs/latest/sessions)
60. [GitHub - gpxl-dev/pi-share-slice · GitHub](https://github.com/gpxl-dev/pi-share-slice)
61. [Sessions and History — Guides](https://piagent.fyi/guides/sessions-and-history/)
62. [earendil-works/pi-coding-agent](https://npmx.dev/package/@earendil-works/pi-coding-agent/v/%3E=0.74.0)
63. [Changelog — bb](https://getbb.app/changelog)
64. [Add plugin entry: hooks by MacHatter1 · Pull Request #410 · get-bb/marketplace · GitHub](https://github.com/get-bb/marketplace/pull/410)
65. [Let one bb server be shared by a team (multiple users, per-user threads and machines)](https://github.com/get-bb/bb/issues/4214)
66. [provider-pi: add background shell tasks with task cards and automatic completion delivery · Issue #5254 · get-bb/bb · GitHub](https://github.com/get-bb/bb/issues/5254)
67. [thread/resume inherits the 30s JSON-RPC default and fails large pi sessions · Issue #5080 · get-bb/bb · GitHub](https://github.com/get-bb/bb/issues/5080)
68. [provider-pi bridge: resumed session can use a stale extensionPath from a dead bridge worker's temp dir (ENOENT on pi-tools-\*.json at extension load) · Issue #5350 · get-bb/bb · GitHub](https://github.com/get-bb/bb/issues/5350)
69. [Pi SDK bridge does not expose standard extension UI requests to BB · Issue #1668 · get-bb/bb · GitHub](https://github.com/get-bb/bb/issues/1668)
70. [Public request-aware handoff ownership for safe provider fallback · Issue #5552 · get-bb/bb · GitHub](https://github.com/get-bb/bb/issues/5552)
71. [Thread list: date group headings (Today, Yesterday, …) in the Custom organization's Threads section · Issue #4809 · get-bb/bb · GitHub](https://github.com/get-bb/bb/issues/4809)
72. [\[2307.00714\] A Comparative Study of Software Secrets Reporting by Secret Detection Tools](https://ar5iv.labs.arxiv.org/html/2307.00714)
73. [Tangled, a Git collaboration platform built on atproto](https://news.ycombinator.com/item?id=45543899)
74. [GitHub - get-bb/bb-lite · GitHub](https://github.com/get-bb/bb-lite)
75. [Extension API and Lifecycle Events](https://deepwiki.com/earendil-works/pi/6.1-extension-api-and-lifecycle-events)
