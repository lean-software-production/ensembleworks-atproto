# Pi Session Sharing and Export

> Sources: See attributed source contributions below; publication dates unknown unless stated.; source inventory: auryan898/pi-dev: packages/coding-agent/docs/sessions.md (Copyright (c) 2025 Mario Zechner; auryan898/pi-dev; Unknown); Pi Coding Agent (Mario Zechner and contributors, Pi coding agent documentation (pi.dev); Unknown); Pi Coding Agent (Mario Zechner and contributors, Pi coding agent documentation (pi.dev); Unknown); gpxl-dev/pi-share-slice (gpxl-dev, pi-share-slice; Unknown); Sessions and History - Guides | Piagent (source notes) (attributed source notes; Unknown)
> Raw: [auryan898-pi-dev-packages-coding-agent-docs-sessions-md](../../raw/pi/auryan898-pi-dev-packages-coding-agent-docs-sessions-md.md); [pi-dev-docs-usage](../../raw/pi/pi-dev-docs-usage.md); [pi-dev-docs-sessions](../../raw/pi/pi-dev-docs-sessions.md); [gpxl-dev-pi-share-slice](../../raw/pi/gpxl-dev-pi-share-slice.md); [sessions-and-history-guides-piagent-notes](../../raw/pi/sessions-and-history-guides-piagent-notes.md)
> Updated: 2026-10-24

## Overview

Session navigation, durable tree storage and publication are separate choices. A viewer or exporter must declare whether it carries the full history, an active branch or a rendered transcript.

## Branch selection versus exported artifacts

The auryan898/pi-dev sessions document distinguishes in-place tree navigation from a fork into another file and a clone of the active branch. Tree navigation can attach a summary of the abandoned path; forking and cloning do not. Selecting a user message returns its text to the editor and moves the leaf to its parent, allowing a new alternative. HTML export and private-gist sharing are separate operations from preserving the complete JSONL tree.

## Diagnostic reports can carry conversation data

The pi.dev usage page warns that the diagnostic `pi-debug.log` should be reviewed before sharing: prompts, responses, tool output, file contents and terminal data can be present. Treat diagnostics and usage artifacts as possible transcript exports rather than assuming that a report contains only aggregate counters.

## Current upstream destinations and storage controls

The captured pi.dev sessions page supports HTML or JSONL export. Sharing defaults to a Radius artifact when Radius authentication is configured and otherwise to a private GitHub gist; `sessionShareDestination` can force the choice. Review includes extension messages and tool arguments as well as visible prose. Storage overrides are `--session-dir`, `PI_CODING_AGENT_SESSION_DIR` and `sessionDir`, with the CLI option taking precedence. Compaction preserves original entries while changing the active model context.

> **Status: Outdated** (2026-10-24)
> The earlier forked sessions document describes HTML export and gist sharing only. The pi.dev snapshot adds JSONL export and Radius selection; the older description is a narrower snapshot, not the full current destination contract.

## Selective publication with pi-share-slice

The pi-share-slice extension selects individual rows from the active branch and invokes the installed pi HTML exporter. User and assistant prose start selected; reasoning, tool bundles and system context start excluded. Filtering does not clear hidden selections, so a visible filter is not itself a disclosure boundary. The extension uses a distinct share command because built-in command dispatch cannot be replaced in its tested older snapshot. It depends on package internals and checks viewer-patch compatibility, making version drift an explicit integration risk.

## Third-party sharing safety and storage caveats

The piagent sessions guide recommends reviewing shared gists even though it describes credential sanitization. That statement is not proof that arbitrary tool output or private context is safe.

> **Status: Disputed**
> This guide names `PI_SESSIONS_DIR`, while the captured upstream sessions page names `PI_CODING_AGENT_SESSION_DIR`. Use the upstream setting for its documented snapshot; do not assume the guide’s alias works. Its example jq query is also illustrative rather than a verified entry schema.

## Related compiled concepts

- [Pi Session File Format](pi-session-format.md)
- [Secret and Context Leakage in Shared Sessions](../security-privacy/secret-leakage-in-shared-sessions.md)
