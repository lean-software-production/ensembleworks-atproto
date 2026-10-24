# Evaluate LLM Agents with Harbor - Opik (source notes)

> Source: https://www.comet.com/docs/opik/integrations/harbor
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-05 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — No license statement found in archived HTML. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/comet-com-c854c2b8/001.md.
> Work: https://www.comet.com/docs/opik/integrations/harbor
> Quotations: 34 characters verbatim in this file; 34 of 90 allowed for this work across the knowledge base.

## About this source

Comet's Opik documentation page "Observability for Harbor with Opik", describing an Opik integration that logs Harbor benchmark trial runs and their ATIF trajectories as traces and spans. No explicit publication date and no license statement found.

## Key facts

- Harbor is described as a benchmark evaluation framework for autonomous LLM agents, with benchmarks such as SWE-bench, LiveCodeBench and Terminal-Bench; it tracks trajectories using ATIF (Agent Trajectory Interchange Format).
- Opik logs each trial result as an Opik trace, trajectory steps as nested spans, tool calls and observations as execution records, and aggregates token usage and costs from ATIF metrics.
- Install with `pip install opik harbor`. Configure Opik with `opik configure` or `opik.configure()`.
- The integration is driven by the `opik harbor` CLI wrapper, which exposes Harbor commands such as `opik harbor run`, `opik harbor jobs start`, `opik harbor jobs resume`, `opik harbor trials start`.
- Example invocation shown runs `opik harbor run` against dataset `terminal-bench@head` with agent `terminus_2` and model `gpt-4.1`; another uses `swebench-lite@head`, agent `claude-code` and model `claude-sonnet-4-6`.
- Custom agents can be passed via `--agent-import-path`; two types are described: external agents (via a `BaseEnvironment` interface) and installed agents (run headless in the container). Opik's `@track` decorator on agent methods creates nested spans.
- Each trial creates a trace with the trial name and task as name and input, agent execution time as start/end, verifier rewards as feedback scores, agent and model metadata, and exception info on failure.
- Each trajectory step becomes a span showing source (user, agent, system), message, tool calls and arguments, observations, token usage and cost per step, and model name.
- Verifier rewards such as a pass flag and a tests-passed count are converted to feedback scores.
- Cost tracking reads `prompt_tokens`, `completion_tokens` and `cost_usd` from step metrics.
- Environment variables: `OPIK_PROJECT_NAME`, `OPIK_API_KEY`, `OPIK_WORKSPACE`.
- The page offers a hosted Comet service or local self-hosting of Opik.

## Related

- Harbor, ATIF, Opik, Arize Phoenix ATIF import.
