# open-telemetry/semantic-conventions-genai#338: ATIF trajectory format used by Harbor (source notes)

> Source: https://github.com/open-telemetry/semantic-conventions-genai/issues/338
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-05 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue content. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-e2d2ed95/001.md.
> Work: open-telemetry/semantic-conventions-genai#338
> Quotations: 37 characters verbatim in this file; 37 of 90 allowed for this work across the knowledge base.

## About this source

An open GitHub issue (#338) in open-telemetry/semantic-conventions-genai titled "ATIF trajectory format used by Harbor", filed by @jeremyeder on 2026-06-23T17:18:42Z, last updated 2026-06-29T16:01:46Z, with one comment. It is a request for feedback and a tracking list of OpenTelemetry GenAI items an ATIF-to-OTel conversion needs. Treated as GitHub user content.

## Key facts

- The author says they and others convert ATIF trajectories to OpenTelemetry spans for visualization, and calls the current conversion bespoke and incomplete until the conventions cover more of the surface.
- The issue links to Phoenix's ATIF helper code as one example of such a converter.
- The author lists related OTel issues and PRs with priorities. P1 (Must): cost conventions (#287), cache/phase token breakdowns in metrics (#197), cache and reasoning token metric attributes (#96), causal span linking for tool execution (#309).
- P2 (Want): `gen_ai.agent.steps` metric (#203), inference/tool calls per invocation (#336), evaluation experiments and test cases (#79), evaluation operation and span (#185).
- P3 (Nice): detailed token usage metrics (#76), agent harness hook conventions (#320).
- Stated motivations in the table include that cache tokens are 88% of the author's input volume, and that step count variance (7–48×) drives cost variance.
- The issue was filed after a June 23 call and mentions @lmolkova and @trask.
- The one comment, by @HarperZ9 on 2026-06-29, proposes a conformance fixture for ATIF to OTel: a source trajectory (parallel tool calls, a retry, a skipped eval case, context selection, a scorer verdict), an expected OTLP-style trace, and a conversion coverage report that labels each field family as `preserved`, `represented_by_ref_or_hash`, `intentionally_not_exported`, `unsupported` or `unverifiable`.
- That comment raises a privacy question: whether private prompt or output is absent due to a privacy boundary or due to converter loss. It also links a Pydantic AI PR (#6135) about stable span names and turn-index attributes.

## Related

- ATIF / Harbor, OpenTelemetry GenAI semantic conventions, Phoenix ATIF helper.
