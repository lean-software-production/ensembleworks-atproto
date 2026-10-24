# regutierrez/traicr#37: Collect Pi traces from bb bridge sessions (~/.bb/pi-bridge-sessions) (source notes)

> Source: https://github.com/regutierrez/traicr/issues/37
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-01 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-5afd3d54/001.md.
> Work: regutierrez/traicr#37
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A GitHub issue (number 37) on the regutierrez/traicr repository, opened by the repository owner, requesting that Traicr collect Pi traces written by bb. State is open with no comments. These are factual notes, not the original text.

## Key facts

- Problem: Pi sessions started from bb are written to bb's own bridge directory rather than the native Pi sessions directory that Traicr's Pi adapter scans, so bb-originated Pi traces are silently missing from the archive.
- Bridge mechanism reported: bb launches Pi with `PI_SESSION_FILE` pointing into `~/.bb/pi-bridge-sessions/` and sets `PI_SESSION_ID`; `PI_CODING_AGENT_DIR` is not set.
- Traicr's Pi discovery lives in `internal/collector/adapters/files.go` and uses `PI_CODING_AGENT_DIR` or the default `~/.pi/agent/sessions`; it never scans the bridge directory.
- The author argues this is a discovery problem, not a parsing problem: the bridge session is format-identical to a native Pi session, so the existing `pi-jsonl` adapter parses it.
- The first record is a session header (type session, version 3, with id, timestamp and cwd); later records are `model_change`, `thinking_level_change`, `custom` and `message` entries.
- Bridge file names look like `pi_<uuid>.jsonl`, whereas native names are `<timestamp>_<id>.jsonl`; identity should come from the header id, not the filename.
- The `cwd` of a bb-run Pi session points into a bb plugin workspace path (an environment-personal-workspace plugin directory), not the user's project path.
- Contrast: bb runs the real claude CLI for Claude Code, so those threads land in the native `~/.claude/projects/` store and are collected already; Pi is the odd one out because bb overrides the session path.
- Proposed options in order of preference: add the bridge directory to the Pi roots when it exists (derive from `BB_HOME` / `~/.bb`), make it configurable via an env var, or document adding it to `Sources["pi"]` in `collector.json`.
- Acceptance criteria include: native trace id equals the session header id; working directory comes from header `cwd`; no duplicate traces when a session exists in both stores; native-only behavior unchanged.

## Related

Traicr trace collector, pi-jsonl adapter, bb Pi provider bridge, pi session format version 3, `~/.bb/pi-bridge-sessions`.
Relevance: any ATProto session-sharing tool for pi must find bb-launched Pi sessions in the bridge directory as well as the native pi sessions directory.
