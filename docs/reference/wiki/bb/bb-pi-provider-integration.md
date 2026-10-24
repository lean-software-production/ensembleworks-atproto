# bb Pi Provider Integration

> Sources: Diffuzmetall/bb-plugin-pi-command-sync README and repo metadata (bb-plugin-pi-command-sync contributors, MIT); regutierrez/traicr issue #37 (notes only); Flavio Copes on bb internals (notes only); all collected 2026-10-23; source inventory: Diffuzmetall/bb-plugin-pi-command-sync (Copyright (c) 2026 bb-plugin-pi-command-sync contributors, Diffuzmetall/bb-plugin-pi-command-sync; Unknown); regutierrez/traicr#37: Collect Pi traces from bb bridge sessions (~/.bb/pi-bridge-sessions) (source notes) (attributed source notes; Unknown); How bb, the programmable IDE for coding agents, is built (source notes) (attributed source notes; Unknown); VladimirGVP/bb-plugin-provider-pi-durable (source notes) (attributed source notes; Unknown); jgarrow-springhealth/bb-plugin-pi-usage (Copyright (c) 2026 Janessa Garrow, bb-plugin-pi-usage; Unknown); get-bb/bb#5254: provider-pi: add background shell tasks with task cards and automatic completion delivery (source notes) (attributed source notes; Unknown); get-bb/bb#5080: thread/resume inherits the 30s JSON-RPC default and fails large pi sessions (source notes) (attributed source notes; Unknown); get-bb/bb#5350: provider-pi bridge: resumed session can use a stale extensionPath from a dead bridge worker temp dir (source notes) (attributed source notes; Unknown); get-bb/bb#1668: Pi SDK bridge does not expose standard extension UI requests to BB (source notes) (attributed source notes; Unknown)
> Raw: [bb-plugin-pi-command-sync](../../raw/bb/diffuzmetall-bb-plugin-pi-command-sync.md); [regutierrez/traicr#37 (notes)](../../raw/pi/regutierrez-traicr-37-collect-pi-traces-from-bb-bridge-notes.md); [Flavio Copes on bb internals (notes)](../../raw/bb/how-bb-the-programmable-ide-for-coding-agents-is-built-notes.md); [vladimirgvp-bb-plugin-provider-pi-durable-notes](../../raw/bb/vladimirgvp-bb-plugin-provider-pi-durable-notes.md); [jgarrow-springhealth-bb-plugin-pi-usage](../../raw/bb/jgarrow-springhealth-bb-plugin-pi-usage.md); [get-bb-bb-5254-provider-pi-add-background-shell-tasks-with-notes](../../raw/bb/get-bb-bb-5254-provider-pi-add-background-shell-tasks-with-notes.md); [get-bb-bb-5080-thread-resume-inherits-the-30s-json-rpc-notes](../../raw/bb/get-bb-bb-5080-thread-resume-inherits-the-30s-json-rpc-notes.md); [get-bb-bb-5350-provider-pi-bridge-resumed-session-can-use-a-notes](../../raw/bb/get-bb-bb-5350-provider-pi-bridge-resumed-session-can-use-a-notes.md); [get-bb-bb-1668-pi-sdk-bridge-does-not-expose-standard-notes](../../raw/bb/get-bb-bb-1668-pi-sdk-bridge-does-not-expose-standard-notes.md)
> Updated: 2026-10-24

## Overview

bb ships a built-in **Pi** provider (`pi`). According to the command-sync README it runs pi as a child process in pi's **RPC mode**, so bb talks to pi over stdin/stdout rather than embedding the SDK. Third-party addons can change how that child is launched through the provider-environment variable `BB_PI_BRIDGE_COMMAND`. With that variable a plugin can load extra pi extensions into every bb-hosted pi session without touching terminal pi. This is the most direct documented hook for a sharing integration that wants to observe pi sessions inside bb with a pi extension. Alternatively, a sharing tool can read the bridge session files that bb writes. They use pi's own format, but they live in a different directory.

> **Status: Disputed**
> How bb drives pi is described differently. The command-sync README says bb's built-in Pi provider runs pi in RPC mode. Flavio Copes' source walkthrough describes `@bb/agent-runtime` as having a Pi adapter that goes through pi's SDK bridge (paraphrased from notes). traicr#37 describes a bridge that launches pi with `PI_SESSION_FILE` and `PI_SESSION_ID` set. These may describe layers of one mechanism (a bridge process speaking RPC), but the sources do not say so. Check `provider-pi` in get-bb/bb before designing against either.

## Where bb-hosted pi sessions are stored

traicr issue #37 (open, no comments) reports that bb does not use pi's native session directory:

- bb launches pi with `PI_SESSION_FILE` pointing into `~/.bb/pi-bridge-sessions/` and sets `PI_SESSION_ID`. `PI_CODING_AGENT_DIR` is not set.
- Bridge files are named `pi_<uuid>.jsonl`, not pi's native `<timestamp>_<id>.jsonl`. The issue recommends taking identity from the header `id`.
- The content is format-identical to native pi sessions: a version-3 header, then `model_change`, `thinking_level_change`, `custom` and `message` entries. An existing pi JSONL parser reads them unchanged. See [Pi Session File Format](../pi/pi-session-format.md).
- The header `cwd` points into a bb plugin workspace path, not the user's project path. A sharing tool that groups sessions by project folder must map bb workspace paths back to projects.
- Claude Code threads in bb run the real `claude` CLI and land in its native store. Pi is the exception because bb overrides the session path.
- The acceptance criteria proposed in the issue are a useful checklist for any exporter:
  - de-duplicate sessions that exist in both stores
  - take the trace id from the header
  - take the working directory from the header `cwd`
  - leave native-only behaviour unchanged

## How the command-sync addon hooks in

The addon targets BB 0.45.0 and `@get-bb/plugin-sdk` 0.6.15. It is tested on Linux only. It works in four steps:

1. Its server entry calls `bb.providers.experimental_contributeEnv("pi", …)` to set `BB_PI_BRIDGE_COMMAND` to a generated launcher. The README calls this the documented public provider-environment surface.
2. The launcher (`pi-bb`, mode `0700`, written under `<dataDir>/runtime/<sha256(…)>/`) `exec`s pi with `--extension <commands.ts>`. It prefers the pi CLI resolved next to the running Node.
3. On every `session_start` the pi extension writes content-addressed command catalogs under `~/.pi/bb-commands/`.
4. A model-free discovery run starts `pi-bb --mode rpc --no-session` and sends a `get_commands` RPC. It is bounded at 20 s and 2 MiB of output.

## Constraints it reveals

- **Only one owner of `BB_PI_BRIDGE_COMMAND`.** The README says a second addon cannot replace the launcher without replacing this one. Cooperation goes through `BB_PI_SUBAGENTS_*` variables. A session-sharing addon that also needs to inject a pi extension would collide with this addon unless it cooperates the same way.
- **No additive SDK API (BB 0.45.0).** There was no way for one plugin to register native-command roots for another plugin's provider. The addon therefore patches the installed `provider-pi` bundle with four exact string edits and backups. The README stresses that this patch is pinned to one BB 0.45.0 build. This is evidence that deep pi integration inside bb may need upstream changes or a bb fork, as the brief anticipated.
- **Unrecognised slash text falls through to the model** as a real, billable turn. Terminal-only pi controls such as `/tree` and `/resume` cannot work in a headless RPC child.

## See Also

- [bb Plugin System](bb-plugins.md)
- [bb Architecture and Data Model](bb-architecture.md)
- [Pi Extensions](../pi/pi-extensions.md)
- [Pi Session File Format](../pi/pi-session-format.md)

## Alternative durable provider

The VladimirGVP durable-provider fork describes a separate Pi Durable integration with transactional SQLite session storage and a bundled JSON-RPC bridge. Its claimed crash recovery and task-graph behavior belong to this alternative runtime, not automatically to bb’s built-in Pi provider. The plugin describes a thin adapter boundary: the runtime owns agent mechanics while the plugin translates protocol events. Its README says MIT but the collected repository metadata found no license file; the exported source therefore remains factual notes.

## Usage indexing without transcript publication

Janessa Garrow’s Pi Usage plugin scans both terminal and bb bridge session directories and stores a derived index in plugin-scoped SQLite. It groups assistant-message usage by source, provider, model and day without contacting providers. The cost values are Pi’s list-price estimates, including subscription providers, so they are not invoices. Its restricted index illustrates an alternative to copying complete conversation content into a sharing service.

## Detached work does not imply completion delivery

The background-shell request reports a detached process finishing while the bb thread stayed idle. A shell process alone did not create a task card or wake-up input; the author requests explicit task ownership, bounded output and completion delivery with duplicate suppression. Those acceptance criteria are proposed work. The source audit in this issue names the bundled RPC-session bridge, supporting an RPC implementation at that snapshot without resolving every older SDK-based report.

## Large-history resume and compaction clocks

The completed resume-timeout issue reports session construction outlasting a default transport deadline. Applying the construction timeout resolved the reproduced resume case, but follow-ups encountered separate turn-start and compaction deadlines. Increasing one timer did not eliminate those other clocks. For a session-sharing importer, loading a valid large history and accepting a new turn are separate readiness events; queue work around compaction rather than assuming successful transport admission means the agent has started.

## Unconfirmed stale-extension diagnosis

An open startup-failure report hypothesizes that a resumed session retained an extension path from a dead worker’s temporary directory. The triage bot could not reproduce it and found current main using worker-local paths.

> **Status: Disputed**
> The reporter’s observed missing-file error is distinct from the proposed persisted-path cause. Clean-checkout tests did not confirm that cause; do not present it as an established persistence bug. An exporter should avoid treating transient worker paths as portable resources regardless.

## Resolved extension-UI gap

The standard extension-UI issue records an older SDK bridge binding extensions without a UI context. Merely declaring RPC mode did not create that transport. The maintainer later says the linked fix made select, confirm, input and editor requests answerable in bb.

> **Status: Outdated** (2026-10-08)
> The blanket UI-unavailable limitation in this article describes the earlier bridge. The maintainer’s resolution reports portable prompt methods working after the fix; executable custom TUI components remain outside the requested portable scope. Check the deployed bridge version before relying on either behavior.
