# Extensions - pi (source notes)

> Source: https://hochej.github.io/pi-mono/coding-agent/extensions/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-01 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: unknown — Mirror carries no license statement. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/hochej-github-io-761277c4/001.md.
> Work: earendil-works/pi:packages/coding-agent/docs/extensions.md
> Quotations: 0 characters verbatim in this file; 37 of 90 allowed for this work across the knowledge base.

## About this source

A MkDocs-style rendering of the pi coding agent's Extensions documentation hosted at hochej.github.io under a pi-mono path. It carries no license statement. The content matches the extensions document from the earendil-works/pi repository (the project was previously named pi-mono), but is an older snapshot than the other mirror. The page shows no publication date. These are factual notes, not the original text.

## Key facts

- Opening matches the upstream doc: extensions are TypeScript modules that can subscribe to lifecycle events, register custom tools, add commands, and more.
- Discovery locations are the same as in the newer snapshot: `~/.pi/agent/extensions/` and `.pi/extensions/`, with `pi -e ./path.ts` for quick tests and `/reload` for hot reload.
- It carries the same security warning that extensions run with full system permissions and can execute arbitrary code.
- Lifecycle list in this older snapshot: `session_start`, `session_before_switch` followed by `session_switch`, `session_before_fork` followed by `session_fork`, `session_before_compact` followed by `session_compact`, `session_before_tree` followed by `session_tree`, and `session_shutdown`.
- Difference observed against the newer mirror (observation): there is no project_trust heading, no ctx.isProjectTrusted section, and no registerEntryRenderer reference in this snapshot; switch and fork are separate after-events here whereas the newer text routes them through shutdown plus a fresh `session_start` with a reason.
- Session persistence is still done through `pi.appendEntry`, and `pi.sendUserMessage` supports steer and followUp delivery modes.
- `pi.registerProvider` already exists in this snapshot.
- The shorter length of this snapshot compared to the newer mirror reflects fewer documented features, not a different work (observation).

## Related

pi coding agent, extension API, session events. See the notes for the newer mirror (pi.ubitools.com) for the fuller feature list.
