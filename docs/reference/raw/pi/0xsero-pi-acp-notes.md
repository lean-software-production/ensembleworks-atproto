# 0xSero/pi-acp (source notes)

> Source: https://github.com/0xSero/pi-acp
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-06 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — GitHub API reports no license; README mentions MIT but no LICENSE file. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-b616f6ba/001.md.
> Work: github.com/0xSero/pi-acp
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

README and repository metadata for the GitHub repo 0xSero/pi-acp, an adapter that connects Agent Client Protocol (ACP) clients to the pi coding agent running in RPC mode. Author is the repo owner 0xSero. Published date is not shown.

## Key facts

- Metadata at collection time: TypeScript, default branch main, 34 stars, 0 forks, 0 open issues, not archived, not a fork. Created 2026-01-19T19:47:37Z, last pushed 2026-01-21T19:03:09Z.
- The GitHub API reports no license for the repo. The README ends with a License heading naming MIT, but no LICENSE file is in the top-level listing.
- It bridges ACP clients (IDEs, UIs) to a pi process started with `--mode rpc`.
- Listed responsibilities: spawn and manage pi sessions in RPC mode, translate ACP requests into pi RPC commands, stream output and tool calls back, and persist sessions across restarts.
- Transport is NDJSON over stdin/stdout between the client and the adapter.
- Documented message flow: client sends initialize, adapter returns capabilities, client sends newSession, adapter spawns pi in RPC mode and returns a sessionId, prompts are forwarded, streaming events become session updates, and the turn ends with end_turn.
- Session persistence uses a map file at `~/.pi/pi-acp/session-map.json`.
- Slash commands such as `/compact`, `/model` and `/thinking` pass through to pi.
- Run with `npm start`; an optional `npm run setup:zed` injects a pi-acp provider into the Zed settings file (`~/.config/zed/settings.json` or the macOS Application Support path).
- Adapter logs go to stderr. Troubleshooting advice is to check that pi is on PATH.
- Top-level files include `package.json`, `tsconfig.json`, `src`, `scripts` and `.github`.

## Related

- svkozak/pi-acp, a separate and much more active adapter for the same purpose.
- Agent Client Protocol SDK, pi coding agent.
