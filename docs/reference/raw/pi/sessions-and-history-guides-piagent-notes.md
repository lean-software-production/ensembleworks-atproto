# Sessions and History - Guides | Piagent (source notes)

> Source: https://piagent.fyi/guides/sessions-and-history/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-07 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — footer says "(c) 2026 piagent.fyi - MIT" with no license text or holder; treated conservatively. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/piagent-fyi-e83328b4/001.md.
> Work: https://piagent.fyi/guides/sessions-and-history/
> Quotations: 25 characters verbatim in this file; 25 of 90 allowed for this work across the knowledge base.

## About this source

A third-party guide on piagent.fyi covering how the pi coding agent stores, navigates, forks, compacts, exports and shares sessions. The page shows "Last updated: Aug 7, 2026" (an update label, not asserted as publication date). It states it follows the official pi.dev sessions docs and `packages/coding-agent/docs/sessions.md`.

## Key facts

- Sessions are append-only JSONL files under `~/.pi/agent/sessions/`, grouped by working directory; one file per session, path encodes the project.
- Location can be overridden with the `PI_SESSIONS_DIR` environment variable (per this guide); `pi --no-session` disables persistence.
- A session is a tree: every entry carries an `id` and a `parentId`; the current position is the active leaf.
- Entry kinds listed: user prompts and assistant replies, model changes, thinking-level changes, labels (set with `Shift+L`), compactions, branch summaries, and extension-emitted entries.
- Branching never deletes the old path; a new branch grows from the selected entry.
- Slash commands: `/resume`, `/new`, `/name <name>`, `/session`, `/tree`, `/fork`, `/clone`, `/compact [prompt]`, `/export [file]`, `/share`.
- CLI flags: `-c` (continue latest), `-r` (browse), `--no-session`, `--name`, `--session` (file path or partial ID), `--fork`.
- Session filenames are timestamp-prefixed, for example `2026-08-07-1530-refactor`; partial-ID matching is loose.
- `/tree` stays in the same file; `/fork` creates a new file from a chosen earlier user message; `/clone` creates a new file from the current active branch only.
- When `/tree` leaves a branch, pi can summarize the abandoned branch (no summary, default prompt, or custom focus prompt).
- `/compact` condenses older entries into one entry; the guide says that as of v0.81.1 compaction and branch summaries honor the provider retry policy and emit retry lifecycle events to interactive, JSON, RPC and SDK consumers.
- Searching: plain JSONL works with `grep` and `jq`; the guide's jq example selects `.type == "user"` and reads `.content` (an illustration by the guide author, not a verified schema).
- `/export` writes a self-contained HTML file; `/share` uploads the session as a private GitHub gist and copies the URL.
- Safety: the guide says shared session content is sanitized for credentials before upload but advises reviewing the gist before wider sharing.
- For large-scale publishing the guide points to the `pi-share-hf` tool (github.com/badlogic/pi-share-hf) covering redacting, reviewing and uploading sessions as a Hugging Face dataset.
- Further reading links: pi.dev docs for sessions, session-format (JSONL schema, entry types, tree semantics), compaction, usage and CLI.

## Related

pi coding agent; pi session-format doc; pi-share-hf; GitHub gist sharing; Hugging Face datasets.
