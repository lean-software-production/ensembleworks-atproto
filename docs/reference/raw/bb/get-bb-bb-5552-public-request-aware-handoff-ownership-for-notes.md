# get-bb/bb#5552: Public request-aware handoff ownership for safe provider fallback (source notes)

> Source: https://github.com/get-bb/bb/issues/5552
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-07 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue: user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-9906b15c/001.md.
> Work: get-bb/bb#5552
> Quotations: 65 characters verbatim in this file; 65 of 90 allowed for this work across the knowledge base.

## About this source

Feature-request issue get-bb/bb#5552, "Public request-aware handoff ownership for safe provider fallback". Opened by wonderlandgardens on 2026-10-15; open. Labels: providers, threads, provider-retry. Marked agent generated. Two comments: a triage bot and the author.

## Key facts

- Workflow: when a Claude Code turn is rejected because Account Pooler has no eligible account, continue it on an available, authenticated Codex subscription using the existing Handoff plugin and workspace, without the source retry and the destination both executing the failed input.
- It requests agreement on a public core contract, not a new provider or billing route.
- Observed contracts (bb 0.46.0, SDK 0.6.37, Handoff 0.7.1, macOS, core main at `05771e3`): Handoff holds a memory-only lock and dispatches before persisting destination history; its public operation lacks request-aware durable identity; core same-thread retry validates request identity but spawn cannot conditionally consume that retry.
- A real-SQLite server test reportedly shows repeated `createThreadFromRequest` calls producing two different pending destination IDs; a proposed `experimental_failedTurnTransfer` field is stripped by the current schema. The author frames this as a missing feature, not a promise broken by current spawn.
- Proposed minimum: extend create/spawn with a failed-source request precondition and a durable operation identity; persist destination identity and the recoverable first input together; reconcile repeated, concurrent or restarted requests to the same destination.
- Preserve the original retry until destination admission; at admission one transaction checks source request identity, cancellation, archive or delete, and newer input, commits destination ownership and consumes the original retry-chain rows (including claimed ones). Every source retry append path (including Send-now and the no-hook queue fast path) must enforce ownership. Whichever side dispatches first invalidates the other.
- Division of responsibility: Handoff exports full history and the exact unaccepted input, preserves accepted side effects as history, checks Codex authentication and capacity, and links destination to source; Provider Retry owns the narrow exhaustion policy; no automatic bounce back from Codex.
- Related issues cited: #5188 (task claims) and #4547 (successor threads) as different ownership boundaries.
- Author's follow-up (2026-10-15): a local prototype adds `threads.experimental_transferFailedTurn`, durable source/request ownership, admission-time invalidation checks and exclusion of source retries after admission. Tests reported: 86 core, 622 database, 119 SDK, 155 Handoff; isolated acceptance with simulated Claude exhaustion produced one destination with no replayed accepted side effect and no Claude inference. No upstream PR opened pending maintainer agreement under CONTRIBUTING.
- Bot triage: Feature, Priority Medium, Effort High.

## Related

bb Handoff plugin; Account Pooler; Provider Retry; thread transfer across providers (Claude Code to Codex); idempotent session handoff.
