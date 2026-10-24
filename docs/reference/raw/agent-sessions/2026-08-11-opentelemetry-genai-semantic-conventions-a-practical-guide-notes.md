# OpenTelemetry GenAI Semantic Conventions: A Practical Guide (source notes)

> Source: https://openobserve.ai/blog/opentelemetry-genai-semantic-conventions/
> Collected: 2026-10-23
> Published: 2026-08-11
> Representation: Source notes written by fetcher-12 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — No license statement on page; only copyright text OpenObserve Inc.. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/openobserve-ai-f4701cc2/001.md.
> Work: https://openobserve.ai/blog/opentelemetry-genai-semantic-conventions/
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A vendor blog post by Simran Kumari on the OpenObserve site, dated August 11, 2026. It is a practical walkthrough of the OpenTelemetry GenAI semantic conventions (the `gen_ai.*` namespace) for LLM and agent telemetry. It is vendor material and also promotes OpenObserve.

## Key facts

- The conventions cover three telemetry kinds: spans, metrics and opt-in content events.
- The post says the OTel GenAI Special Interest Group has defined them since April 2024.
- Core span attributes listed: `gen_ai.operation.name`, `gen_ai.provider.name`, `gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`.
- Further attributes: `gen_ai.request.temperature`, `gen_ai.request.top_p`, `gen_ai.request.max_tokens`, `gen_ai.response.id`, `error.type`.
- `gen_ai.response.finish_reasons` is an array of strings, for example `["tool_use"]`.
- `gen_ai.conversation.id` groups spans of one multi-turn session; the author says OpenObserve's LLM Sessions view keys on it. This is the closest convention to a session identifier.
- Operation names given: `chat`, `text_completion`, `embeddings`, `execute_tool`, `create_agent`, `invoke_agent`.
- Tool attributes: `gen_ai.tool.name`, `gen_ai.tool.call.id`, `gen_ai.tool.description`.
- Agent attributes: `gen_ai.agent.name`, `gen_ai.agent.id`, `gen_ai.agent.description`, and `gen_ai.agent_version` (as spelled in the post).
- Embeddings attributes: `gen_ai.request.encoding_formats`, `gen_ai.embeddings.dimension.count`.
- Span naming pattern is the operation name followed by the request model, for example a span named `chat gpt-4o`.
- Metrics: two histograms, `gen_ai.client.token.usage` and `gen_ai.client.operation.duration`.
- Stability per the author: core chat attributes Stable or Release Candidate, embeddings Release Candidate, tool and agent attributes Development. The author advises checking the live spec before building dashboards on agent attributes.
- Content privacy: prompt and response bodies are deliberately not standard span attributes because they often contain PII. They are emitted as separate opt-in log-based events correlated by `trace_id` and `span_id`.
- The post names the environment variable `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` as a common switch, and recommends keeping capture off in production and redacting via an OTel Collector processor.
- Migration: `gen_ai.system` is being superseded by `gen_ai.provider.name`; many libraries emit both. Older `llm.*` names should be renamed to `gen_ai.*`.
- Libraries mentioned: OpenLIT, OpenLLMetry, and the official contrib instrumentation for OpenAI and Anthropic.
- The author shows a Claude Code agent trace in OpenObserve with `gen_ai_*` fields, where dots become underscores.
- Worked example values: input tokens 312, output tokens 148, temperature 0.7, top_p 0.9, max_tokens 1024.

## Related

- OpenTelemetry GenAI semantic conventions and registry (opentelemetry.io), now moved to the semantic-conventions-genai repository.
- OpenLIT, OpenLLMetry, Arize Phoenix, Opik as other observability stacks.
