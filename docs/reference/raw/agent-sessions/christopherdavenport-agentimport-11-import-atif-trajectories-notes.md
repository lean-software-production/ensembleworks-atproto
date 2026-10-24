# ChristopherDavenport/agentimport#11: Import ATIF trajectories (source notes)

> Source: https://github.com/ChristopherDavenport/agentimport/pull/11
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-05 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub pull request content. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-94399583/001.md.
> Work: ChristopherDavenport/agentimport#11
> Quotations: 24 characters verbatim in this file; 24 of 90 allowed for this work across the knowledge base.

## About this source

A merged GitHub pull request (#11, "Import ATIF trajectories") in ChristopherDavenport/agentimport, opened by the repo owner. Created 2026-10-16T02:14:23Z, merged 2026-10-16T15:07:24Z. It touches 110 files (+8154/-30). The description ends with an attribution line to Claude Code, so the change appears to be agent-assisted. Zero comments are recorded. The repo is MIT licensed, but PR text is treated here as GitHub user content.

## Key facts

- Adds ATIF (Harbor's Agent Trajectory Interchange Format, v1.0-v1.8 per the description) as the fourth import source of agentimport: package `atif/` reads documents and `atif/convert` turns them into sessions.
- A document written by agentsession's own exporter is rebuilt from the raw items it carries; a document produced by Harbor's adapters is mapped from its steps.
- Reader is tolerant: a bad step, call, result, ref or part becomes a finding and the rest still converts. Undeclared members and numbers are preserved as written, and truncated documents (the PR mentions Terminus 2 rewriting in place) are read up to the cut.
- ATIF is a single JSON document, not JSONL, so the tally counts roots and steps through a new `Report.Unit`; the other three sources count lines.
- Context handling: RFC section VII `replace` rule applied; Terminus 2 post-summary context rebuilt; Claude Code sidechain steps move into separate sessions per sub-agent linked to the originating Task call; mini-swe-agent results pair with calls.
- Related files: continuations become `continued_in` links; file-referenced and embedded sub-agent trajectories become subsessions; nesting stops at depth 32 or on repeat; related files are read only within the document's directory.
- Native IDs the store would refuse get a deterministic safe ID, with the original kept in `atif:session_id`.
- Four new gaps for the ATIF RFC are recorded in `docs/incompatibilities.md`: a sub-agent no call spawned, an unrecorded compaction summary, pruning that does not name what it removed, and tool calls no model produced (`llm_call_count: 0`).
- Testing: `make check` passes; round trip test exports with `export.ToATIF` and re-imports; fixtures are synthetic, one per producer shape (e.g. claude-code, codex, compaction, continuation, embedded, vibe testdata directories); `make corpus` was not run. A separate agent review gave 17 findings, 15 fixed and 2 partly declined.
- Docs added: `docs/formats/atif.md` (+360 lines).

## Related

- ATIF, Harbor, agentimport, agentsession.
