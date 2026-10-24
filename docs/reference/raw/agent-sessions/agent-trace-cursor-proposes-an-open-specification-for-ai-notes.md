# Agent Trace: Cursor Proposes an Open Specification for AI Code Attribution (source notes)

> Source: https://www.infoq.com/news/2026/02/agent-trace-cursor/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-05 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — No license statement found in archived HTML. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/infoq-com-2a5dd8ce/001.md.
> Work: https://www.infoq.com/news/2026/02/agent-trace-cursor
> Quotations: 12 characters verbatim in this file; 12 of 90 allowed for this work across the knowledge base.

## About this source

A short InfoQ news item by Robert Krzaczyński, dated Feb 04, 2026 on the page, about Cursor's publication of Agent Trace, a draft open specification (released as an RFC) for attributing AI-generated code. Secondary news coverage, not the specification itself.

## Key facts

- Agent Trace is presented as a vendor-neutral data specification for recording AI contributions next to human authorship in version-controlled code.
- The article says tools like git blame cannot tell whether a change came from a human, an AI or both; Agent Trace aims to add that context.
- A JSON "trace record" connects code ranges to the conversations and contributors behind them.
- Contributions can be tracked at file or line level, grouped by conversation, and classified as human, AI, mixed or unknown. Optional model identifiers can be attached to AI-generated code without tying the format to one provider.
- Storage-agnostic: records may live in files, git notes, database entries or other mechanisms.
- Supports several version control systems named in the article: Git, Jujutsu and Mercurial. Optional content hashes help follow attributed code when it moves or is refactored.
- Extensibility: vendors add metadata through namespaced keys without breaking compatibility. The spec avoids UI requirements and ownership semantics, and does not judge code quality or track training-data provenance.
- Cursor ships a reference implementation showing a coding agent capturing trace records as files change; the patterns are meant to be reusable by other editors and agents.
- The article reports two positive reactions from X users about review and debugging value (reproducibility).
- As an RFC, it leaves open questions on merges, rebases and large-scale agent-driven changes.
- Relevance to agent session sharing: it links code ranges to conversation identifiers, which is a pointer-style attribution model rather than a full session transcript format.

## Related

- Cursor, the Agent Trace spec at agent-trace.dev (linked by the article), git notes, Jujutsu, Mercurial.
