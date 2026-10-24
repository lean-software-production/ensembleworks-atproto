# Agent Session and Trace Formats

> Sources: See attributed source contributions below; publication dates unknown unless stated.; source inventory: Import ATIF trajectories - Phoenix (source notes) (attributed source notes; Unknown); ATIF - Harbor (Harbor Framework contributors, harbor-framework/harbor docs; Unknown); ChristopherDavenport/agentimport#11: Import ATIF trajectories (source notes) (attributed source notes; Unknown); yzhao062/agentpile (yzhao062 and agentpile contributors, agentpile; Unknown); Evaluate LLM Agents with Harbor - Opik (source notes) (attributed source notes; Unknown); open-telemetry/semantic-conventions-genai#338: ATIF trajectory format used by Harbor (source notes) (attributed source notes; Unknown); open-telemetry/semantic-conventions-genai (open-telemetry/semantic-conventions-genai contributors (Apache-2.0 licensed); Unknown); openai/codex: codex-rs/rollout/src/recorder.rs (openai/codex contributors (Apache-2.0 licensed); Unknown); google-gemini/gemini-cli: docs/cli/session-management.md (google-gemini/gemini-cli contributors (Apache-2.0 licensed); Unknown); Gen AI (The OpenTelemetry Authors, OpenTelemetry documentation; Unknown); OpenTelemetry GenAI Semantic Conventions: A Practical Guide (source notes) (attributed source notes; 2026-08-11)
> Raw: [import-atif-trajectories-phoenix-notes](../../raw/agent-sessions/import-atif-trajectories-phoenix-notes.md); [atif-harbor](../../raw/agent-sessions/atif-harbor.md); [christopherdavenport-agentimport-11-import-atif-trajectories-notes](../../raw/agent-sessions/christopherdavenport-agentimport-11-import-atif-trajectories-notes.md); [yzhao062-agentpile](../../raw/agent-sessions/yzhao062-agentpile.md); [evaluate-llm-agents-with-harbor-opik-notes](../../raw/agent-sessions/evaluate-llm-agents-with-harbor-opik-notes.md); [open-telemetry-semantic-conventions-genai-338-atif-notes](../../raw/agent-sessions/open-telemetry-semantic-conventions-genai-338-atif-notes.md); [open-telemetry-semantic-conventions-genai](../../raw/agent-sessions/open-telemetry-semantic-conventions-genai.md); [openai-codex-codex-rs-rollout-src-recorder-rs](../../raw/agent-sessions/openai-codex-codex-rs-rollout-src-recorder-rs.md); [google-gemini-gemini-cli-docs-cli-session-management-md](../../raw/agent-sessions/google-gemini-gemini-cli-docs-cli-session-management-md.md); [gen-ai](../../raw/agent-sessions/gen-ai.md); [2026-08-11-opentelemetry-genai-semantic-conventions-a-practical-guide-notes](../../raw/agent-sessions/2026-08-11-opentelemetry-genai-semantic-conventions-a-practical-guide-notes.md)
> Updated: 2026-10-24

## Overview

Native session logs, normalized trajectories and observability spans preserve different information. Exporters should retain source identity and document omissions, reconstruction and timing assumptions.

## Phoenix conversion boundaries

Phoenix’s ATIF importer builds span trees from trajectories and reconstructs LLM inputs. Copied context does not become new execution; unmeasured events have no measured duration. Subagent documents must be provided together, and continuation files need a common batch for merging. Media bytes are not uploaded. Deterministic span identifiers do not make repeated uploads idempotent: existing identifiers can cause rejection. These limitations mean a trace view is a projection, not proof that every original interaction was preserved.

## ATIF capability and validation contract

Harbor describes ATIF as a JSON representation of messages, reasoning, tool calls, observations and metrics. The captured documentation uses `ATIF-v1.7`, with optional document identifiers and embedded subagent trajectories. Ordered steps have sequential identifiers and observations reference tool calls. Producing a valid trajectory and loading one to seed an agent are separate capabilities. Custom metadata belongs in `extra`; undeclared schema fields are rejected by Harbor’s models. Validation checks schema, step ordering, references, timestamps and local image references.

## Agentimport tolerant ingestion

The merged agentimport pull request adds ATIF import through document readers and session converters. Malformed steps and references become findings while usable content still converts. Native raw items are restored when available; Harbor-produced documents map from steps. Continuations become linked sessions and subagents become subsessions, with related-file reads restricted to the document directory. Synthetic fixtures and round trips passed according to the PR, but corpus testing was not run. Its documented gaps include missing compaction summaries and pruning targets, so successful import does not establish losslessness.

## Agentpile normalization and inferred analysis

Agentpile reads datasets, trace files and live runs into a common ATIF-based record while retaining what the input actually recorded. It downloads datasets from publishers at pinned revisions rather than redistributing them. Exported OTLP timings can be synthetic ordering when the input has no timestamps; those durations are not runtime measurements. Value-flow dependencies are inferred from reused values and name their rule, so they should remain distinguishable from recorded causality.

## Benchmark context in Opik

Opik’s Harbor integration wraps benchmark execution and represents trials as traces and trajectory steps as nested spans. It also records verifier rewards as feedback, token/cost metrics and failures. This benchmark context differs from Phoenix’s standalone trace upload: an experiment result and a captured conversation are related artifacts, not interchangeable evidence of success.

## Conversion coverage remains an open concern

The OpenTelemetry GenAI issue about ATIF calls existing conversions bespoke and incomplete. It requests cost, cache-token and causal tool-execution conventions. A commenter proposes fixtures and field-family coverage labels separating preserved data, references, intentional exclusions, unsupported data and unverifiable data. This is proposed conformance work, not an adopted standard. The distinction between deliberate privacy exclusion and accidental converter loss is especially relevant to shared sessions.

## GenAI convention repository and generated specifications

The OpenTelemetry GenAI repository covers spans, metrics and events for GenAI clients, MCP and provider-specific conventions. It builds on core conventions using Weaver and generates much of its human-readable documentation from model definitions. The README’s schema-URL section is still a placeholder in the captured source. Convention definitions and reference compliance reports therefore need explicit version scope rather than an assumed universal trace contract.

## Codex native rollout recorder

The captured Codex recorder persists canonical rollout items as JSONL and distinguishes creating a rollout from resuming a path. Creation metadata includes conversation and session identity, fork/parent relationships, source and originator, base instructions and dynamic tools. The code comments distinguish stable thread identity from a newly created immutable rollout on revert. An exporter should therefore preserve rollout identity as well as the conversation identifier instead of assuming one file per thread forever.

## Gemini project-scoped sessions and retention

Gemini CLI documents automatic project-scoped history, including tool input/output, usage and available reasoning summaries. Its session browser and command-line controls resume or delete saved sessions; manual tagged checkpoints are a separate feature. Retention cleanup can remove associated plans, task trackers, tool output and activity logs. A collector must account for this lifecycle and avoid assuming the native store is a permanent archive.

## Moved and deprecated telemetry attributes

The captured GenAI attribute registry marks current attributes as moved to the separate GenAI convention repository and retains deprecated entries. It includes conversation identity and input-message representations among the moved families. An exporter should distinguish semantic attribute stability and migration status from the existence of a string key in a historical registry. Content-bearing attributes also require disclosure review; a trace is not inherently aggregate-only data.

## Vendor telemetry guide versus registry

OpenObserve’s guide explains conversation-level correlation, operation spans and opt-in content capture, with redaction recommended for production. Its account says prompt/response bodies are separate log events rather than ordinary span attributes.

> **Status: Disputed**
> The captured registry also lists input-message attribute representations and marks attributes moved to the GenAI repository. The vendor guide’s blanket placement and stability descriptions should not override versioned convention definitions. Its agent-version spelling also differs from the registry; choose keys from the intended schema rather than copying the guide uncritically.

## Related compiled concepts

- [Pi Session File Format](../pi/pi-session-format.md)
- [Message Provenance and Attribution](../security-privacy/message-provenance-and-attribution.md)
- [Secret and Context Leakage in Shared Sessions](../security-privacy/secret-leakage-in-shared-sessions.md)
