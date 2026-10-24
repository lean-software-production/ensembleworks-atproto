# Import ATIF trajectories - Phoenix (source notes)

> Source: https://arize.com/docs/phoenix/tracing/how-to-tracing/importing-and-exporting-traces/importing-atif-trajectories
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-05 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — No license statement found in archived HTML. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/arize-com-781cc2d9/001.md.
> Work: https://arize.com/docs/phoenix/tracing/how-to-tracing/importing-and-exporting-traces/importing-atif-trajectories
> Quotations: 24 characters verbatim in this file; 24 of 90 allowed for this work across the knowledge base.

## About this source

A page in the Arize Phoenix documentation titled "Import ATIF trajectories", describing the `phoenix-client` helper that converts ATIF (Agent Trajectory Interchange Format) trajectory JSON into OpenTelemetry-compatible spans and uploads them to Phoenix. No explicit publication date. No license statement was found; the page links to the arize-ai/phoenix repository for edits.

## Key facts

- ATIF is described as an open schema for recording agent execution traces; Claude Code, OpenHands, Gemini CLI and Codex are listed as agents exporting ATIF via the Harbor benchmark harness.
- The helper converts ATIF v1.0 through v1.7 into span trees. It uploads traces only; the separate Harbor plugin also records experiment runs.
- Entry point: `upload_atif_trajectories_as_spans`, imported from `phoenix.client.helpers.atif`, called with a client, a list of trajectory dicts and `project_name`.
- Remote Phoenix is configured via `PHOENIX_COLLECTOR_ENDPOINT` and, if authentication is on, `PHOENIX_API_KEY`.
- Span hierarchy: AGENT root per trajectory; `iteration N` CHAIN span per fresh agent step; LLM and TOOL spans as children. Context-management steps use `compaction N`, other system steps use `system event N`. Original step ID is kept in `metadata.atif.step_id`.
- Multi-turn trajectories add `turn N` AGENT spans. Steps marked `is_copied_context: true` add context but no execution spans. A step with `llm_call_count: 0` yields no LLM span.
- Subagents: parent and child trajectories link via `subagent_trajectory_ref`; they must be loaded and uploaded together, parents before children. The helper does not read referenced files or fetch URLs. ATIF v1.7 embedded `subagent_trajectories` resolve by `trajectory_id`.
- Continuations: when the context window fills, Harbor splits a session into files whose `session_id` ends in `-cont-N`; the converter merges them when all are in the same batch. Continuation roots carry `metadata.is_continuation = True`.
- LLM inputs are reconstructed from ATIF, flagged by `metadata.atif.input_source = "reconstructed"`. ATIF sources `user`, `system`, `agent` map to roles `user`, `system`, `assistant`.
- Observations become tool responses only if `source_call_id` matches a declared call. Media bytes are not read or uploaded; ATIF v1.8 audio fields are not supported.
- Timestamps describe events, not durations; unmeasured spans are zero-duration. The Harbor plugin can use `api_request_times_msec`.
- Attribute mapping to OpenInference includes `metrics.prompt_tokens` to `llm.token_count.prompt`, `metrics.completion_tokens` to `llm.token_count.completion`, `metrics.cached_tokens` to `llm.token_count.prompt_details.cache_read`, `metrics.cost_usd` to `llm.cost.total`, `session_id` to `session.id`, and `final_metrics` to root span metadata.
- IDs are deterministic for the same documents, but uploads are not idempotent: Phoenix rejects a batch containing an existing span ID.
- Known limitation: for very long sessions (roughly 16+ turns with dense tool calls) full history in each LLM span can exceed OpenTelemetry attribute size limits.
- The converter rejects duplicate span IDs, unresolved span parents, cross-trace parent links and cycles before upload.

## Related

- ATIF / Harbor, OpenInference, Arize Phoenix, Opik Harbor integration.
