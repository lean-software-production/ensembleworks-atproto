# get-bb/bb#5080: thread/resume inherits the 30s JSON-RPC default and fails large pi sessions (source notes)

> Source: https://github.com/get-bb/bb/issues/5080
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-07 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue: user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-f8ee379f/001.md.
> Work: get-bb/bb#5080
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

Bug report get-bb/bb#5080 about the title issue that `thread/resume` inherits the 30s JSON-RPC default and fails large pi sessions. Opened by Diffuzmetall on 2026-10-07 and closed as completed the same day. Labels: providers, provider-pi, confirmed-repro. Four comments: a triage bot report and three follow-ups by the author.

## Key facts

- Summary: `thread/resume` was the only session-construction command that passed no explicit deadline to `sendCommand`, so it used the transport default of 30 seconds (`30_000` ms). `thread/start` and `thread/fork` already use `threadCreationRequestTimeoutMs`.
- Symptom: the thread goes to `error` with a turn.submit command failure caused by a JSON-RPC request timeout on resume; retrying fails identically.
- Production case (self-hosted bb 0.45.0, pi provider): session file 26.9 MB, 4366 records, 12 compactions totalling 5.6 MB of summaries, about 108k tokens of live context. Construction finished at 31 to 34 seconds, after the daemon gave up at 30.0s. A cold resume on an unloaded dev host took about 15 seconds.
- Reproduction on a dev instance with injected delay: before the fix `timeoutMs=undefined` and failure at 30001 ms; after, `timeoutMs=120000` and success at 35847 ms.
- Root cause files: `packages/provider-bridge-protocol/src/bridge-kit/runtime-json-rpc.ts` (timer falls back to 30_000) and `packages/agent-runtime/src/runtime.ts` (`DEFAULT_THREAD_CREATION_REQUEST_TIMEOUT_MS` is 2 * 60_000; start at line 1608, fork at line 1749, resume command at line 1912 and `sendCommand` at line 1938 without `timeoutMs`).
- For pi, `thread/resume` goes through `handleThreadConstruction`, `constructPiThreadSession`, `await session.start()`; the bridge answers with the provider thread id only after that resolves, so latency scales with session size.
- Proposed fix: pass `timeoutMs: threadCreationRequestTimeoutMs` at the resume call, or (structural option) derive the deadline from command type inside `sendCommand`. Tests proposed: unit assertion of timeouts per command type, and a behavioural test using the existing `threadCreation.requestTimeoutMs` option with a fake provider that delays resume.
- Residual risk the author notes: a genuinely stuck provider would now hold a turn for the longer deadline; a progress heartbeat in the bridge protocol would allow an idle timeout instead.
- Environment: bb-app 0.45.0, Linux, pi provider with an `openai-codex` model, full permission mode; the pi bridge worker had idle-stopped after about 5 minutes (uptime about 300s), forcing a cold resume. The author expects other providers whose resume blocks on construction to be affected too.
- Bot triage (2026-10-07): Bug, Priority High, Effort Low; reproduced with high confidence; fix PR #5082 ready but not merged at that time; says all 309 runtime tests passed.
- Follow-up comment 1: after deploying the resume fix, the next failure was `turn/start` timing out at 30 seconds because the pi session (31.6 MB) began compacting on load; compaction took about four and a half minutes. The author applied a ten minute provider-busy deadline to `turn/start` and `turn/steer` as local mitigation, and argues the better fix is for the bridge to answer immediately with the existing compaction-in-progress outcome so the runtime can retry or queue.
- Follow-up comment 2: on a 32 MB session compaction took about seven minutes versus the ten minute deadline, zero JSON-RPC timeouts afterwards; the author calls it a race against compaction time.
- Follow-up comment 3: a separate guard, error code `provider_turn_start_timeout`, fires if the provider does not start a turn within 120s of accepting it; the turn still completed. The author concludes two clocks race (30 second transport default and the 120 second guard) and recommends not submitting prompts during `session_before_compact` / `compaction_start`, or queueing them.
- Relevance to session sharing: pi session files grow to tens of MB with many compactions; resuming or loading them is slow, which matters for any scheme that stores or replays whole sessions.

## Related

get-bb/bb PR #5082; bb provider bridge protocol; pi session compaction; bb agent-runtime idle worker stop.
