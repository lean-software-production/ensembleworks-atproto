# Pi Session File Format

> Sources: earendil-works/pi `docs/session-format.md` (Mario Zechner / pi contributors, MIT), undated; regutierrez/traicr issue #37 (notes only); both collected 2026-10-23; source inventory: earendil-works/pi: packages/coding-agent/docs/session-format.md (Copyright (c) 2025 Mario Zechner, earendil-works/pi; Unknown); regutierrez/traicr#37: Collect Pi traces from bb bridge sessions (~/.bb/pi-bridge-sessions) (source notes) (attributed source notes; Unknown)
> Raw: [pi session-format.md](../../raw/pi/earendil-works-pi-packages-coding-agent-docs-session-format.md); [regutierrez/traicr#37 (notes)](../../raw/pi/regutierrez-traicr-37-collect-pi-traces-from-bb-bridge-notes.md)
> Updated: 2026-10-23

## Overview

Pi persists each session as one JSONL file. The first line is a header. Every later line is a typed entry that points to a parent, so one file holds a whole tree of branches. Branching (`/tree`), forking, compaction and context edits are all append-only. Raw history is never rewritten: what the model sees is a *projection* computed from the current leaf. That makes the file a good candidate for a lossless, append-only record type to sync to other people. It also means a reader has to replay the tree to reconstruct what a participant actually saw.

## Location and identity

- Files live under `~/.pi/agent/sessions/`, in a per-project directory derived from the working directory. Pi strips the leading separator and replaces `/`, `\` and `:` with `-`. File names are `<timestamp>_<session-id>.jsonl`.
- The session id is a UUID by default. Callers can supply their own through the SDK or `--session-id`.
- Deleting a session means deleting its `.jsonl` file. Interactive `/resume` can also delete a session, and uses the `trash` CLI when it is available.
- A session created by `/fork`, `/clone` or `newSession({ parentSession })` records the path of the original file in a `parentSession` header field.
- **Sessions are not always in the default directory.** bb launches pi with `PI_SESSION_FILE` pointing into `~/.bb/pi-bridge-sessions/`, using `pi_<uuid>.jsonl` names in the same format (traicr#37). `PI_CODING_AGENT_DIR` also relocates the native store. A sharing tool should discover sessions from every root and key them by header `id`. See [bb Pi Provider Integration](../bb/bb-pi-provider-integration.md).

## Versions

The header carries a version:

- Version 1 was a linear sequence. It is legacy and auto-migrated on load.
- Version 2 introduced the tree (`id`/`parentId`).
- Version 3 renamed the `hookMessage` role to `custom`.

Pi migrates existing sessions to v3 when it loads them. A sharing layer should therefore expect older files on disk and normalise them, or let pi do it, before publishing.

## Entry model

Every entry except the header has `type`, `id`, `parentId` (null for a root) and an ISO `timestamp`. Nested message timestamps are Unix milliseconds. Entry types:

| Type | Purpose | In LLM context? |
|---|---|---|
| `message` | An `AgentMessage`: user, assistant, `toolResult` or system | yes |
| `model_change` / `thinking_level_change` | Model or reasoning switches | settings only |
| `usage` | Usage not tied to an assistant message, such as cache warming. Counts toward cost totals. Unknown `kind` values should be tolerated. | no |
| `compaction` | Summary of earlier entries plus a full system/tool checkpoint. `firstKeptEntryId` is required. | yes (replaces older entries) |
| `context_edit` | Append-only omission or replacement of one earlier entry's content in *future* model context. The latest edit on the active branch wins. | modifies projection |
| `branch_summary` | LLM summary of an abandoned branch when switching with `/tree` | yes |
| `custom` | Extension state persistence | no |
| `custom_message` | Extension-injected message, optionally displayed in the TUI | yes |
| `label` | Bookmark on an entry | no |
| `session_info` | Display name, set via `/name`, `--name` or `pi.setSessionName()` | no |

System prompt and tool loadout are also recorded in the log. The first request persists a system message with every prompt section and tool declaration. Later system messages patch sections by name and list `toolsAdded`/`toolsRemoved`. There is no separate prompt-state entry.

Assistant messages name the model that answered. Newer ones also record `thinkingLevel`.

## Reconstructing what the model saw

`buildContextEntries()` walks from the current leaf back to the root and applies the latest compaction on that path. `buildSessionProjection()` then applies `context_edit`s. `buildSessionContext()` converts the result into the message list for the LLM. The doc stresses that edits leave the target "unchanged in raw history, UI, exports, and session accounting" (pi docs, MIT).

Implications for sharing:

- A published session should carry the full tree, or at least the active path, plus its edits. A flat transcript loses branches and summaries.
- Collaborators viewing someone else's session see raw history. What the model actually received may differ because of compaction and edits. A viewer can show both views.
- Entries reference each other by short ids, which are usually 8-character hex according to the doc's type comments. A record-per-entry mapping onto an ATProto repository therefore needs a deterministic key scheme. See [ATProto Repository and Records](../atproto/repository-and-records.md).
- System messages contain the full prompt and tool declarations. They can be large and may embed sensitive project context, so they deserve a redaction step before publication. See [Secret and Context Leakage in Shared Sessions](../security-privacy/secret-leakage-in-shared-sessions.md).

## Extension hooks in the format

Extensions persist state as `custom` entries keyed by `customType`, which stay out of model context. They inject model-visible content as `custom_message` entries. A sharing extension could record its own bookkeeping (for example, the AT URI each entry was published under) in `custom` entries without disturbing the conversation. Pi itself stores virtual-model router state this way under `customType` `pi.virtual-model-state`.

## See Also

- [Pi Extensions](pi-extensions.md)
- [Pi Session Sharing and Export](pi-session-sharing-and-export.md)
- [Agent Session and Trace Formats](../agent-sessions/agent-session-trace-formats.md)
