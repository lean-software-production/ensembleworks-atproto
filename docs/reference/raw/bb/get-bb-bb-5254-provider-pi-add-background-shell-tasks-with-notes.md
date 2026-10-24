# get-bb/bb#5254: provider-pi: add background shell tasks with task cards and automatic completion delivery (source notes)

> Source: https://github.com/get-bb/bb/issues/5254
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-07 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue: user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-165ac9a9/001.md.
> Work: get-bb/bb#5254
> Quotations: 89 characters verbatim in this file; 89 of 90 allowed for this work across the knowledge base.

## About this source

Feature-request issue get-bb/bb#5254, titled "provider-pi: add background shell tasks with task cards and automatic completion delivery". Opened by ariofrio on 2026-10-09 (updated the same day), open, labels providers and provider-pi. The body says it was written by Codex and is marked agent generated.

## Key facts

- Reproduction environment reported: BB 0.45.0, Pi 1.1.0, macOS 26.5.1, model `openrouter/moonshotai/kimi-k2.6`. In that test, a `background_task` tool was not available to the agent.
- A detached shell fallback worked: the launcher returned in 22 ms, the turn finished at 15:30:37.492, and the background command wrote its output marker at 15:30:55.458. No `backgroundTask` item or automatic follow-up arrived during the next 87 seconds; the thread stayed idle.
- Finding: detached shell commands do not wake the bb thread on completion unless the agent adds an explicit callback, for example `bb thread tell`.
- A separate user observation (unverified): through the GUI the agent seemed to block on a command it claimed to background; the test did not reproduce that.
- Repro uses `bb thread spawn` with `--provider pi` and `--prompt-file`, then inspects the log with `bb thread log <id> --all --json`.
- Proposed tools: `background_task(command, description, cwd?, timeout_sec?)` and `background_task_cancel(taskId)`; launch returns a task ID and output-file path promptly.
- Acceptance criteria summarized: a task card appears within one second and updates through running, success, failure, timeout, cancellation; completion is delivered to an active agent between steps, or starts one follow-up turn if idle, recorded as provider input without duplicates; full stdout/stderr kept in a file with bounded summaries; stop/release/discard terminates owned process trees; restart may terminate verified owned orphans, not adopt them; shared workspaces, forks and session replacement must not mix ownership.
- Scope limited to `plugins/provider-pi`, using existing SDK/protocol and Node facilities. Subagents, restart adoption, a full live-log viewer and standalone Pi CLI changes are out of scope.
- Source audit at BB main commit `9a47d42`: bb launches Pi in RPC mode with a bundled extension (`plugins/provider-pi/src/bridge/rpc-session.ts`).
- Implementation constraints: task deltas use `status: "pending"`, `taskStatus: "running"`, `taskType: "local_bash"`, `skipTranscript: false` and a unique `familyId`; `item.close` has no `attach` field; schemas in `thread-delta.ts` and the delta assembler under `provider-bridge-protocol`.
- Pi 1.1.0 idle `followUp()` only queues input; the issue proposes custom-message delivery with `triggerTurn: true` (in pi `agent-session.ts`).
- Open task events already prevent idle-session reaping; explicit stop must release per-thread resources per `docs/provider-bridge-protocol.md`; recovery must verify process ownership, not only PID liveness.
- Existing alternative: the `@aliou/pi-processes` extension. Referenced issues: #1681, merged PR #2154 (completion-input projection), #2461 (ACP wake delivery), #2520 (terminal completion), #2572 (live output).
- Bot comment (bb-slop-cop, 2026-10-09): Type Feature, Priority Medium, Effort High; medium priority attributed to the available detached-shell workaround.

## Related

bb provider-pi plugin; provider bridge protocol (thread deltas); Pi RPC mode; ACP wake delivery; pi-processes.
