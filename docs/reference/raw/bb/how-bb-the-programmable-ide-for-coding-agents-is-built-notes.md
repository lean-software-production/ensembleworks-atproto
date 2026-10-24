# How bb, the programmable IDE for coding agents, is built (source notes)

> Source: https://flaviocopes.com/bb-agentic-ide/
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-03 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — no license statement in archived page; text says bb itself is MIT. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/flaviocopes-com-d126e1f4/001.md.
> Work: https://flaviocopes.com/bb-agentic-ide
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A blog article by Flavio Copes, titled How bb, the programmable IDE for coding agents, is built, marked Updated Oct 21, 2026 on the page. The author says he read the bb source (get-bb/bb) and traced one coding-agent task through the server, SQLite database, host daemon, provider runtime, event stream and app. The page carries site promotional content that is not summarised. License: all rights reserved (no license statement found); the text states that bb itself is MIT-licensed.

## Key facts

- bb is described as an open source IDE for coding agents with the tagline about loop-driven development. The app, CLI, SDK and HTTP API all control the same system.
- Unit of work is a thread, recording project, agent provider, execution environment, lifecycle state, parent or source thread, and an ordered stream of messages, tool calls, approvals and file changes. Threads are standard or manager; a child thread points at its parent.
- Four runtime pieces: server (product state, policy, HTTP API, SQLite storage, WebSocket notifications), host daemon (runs on every executing machine, provisions workspaces, starts provider processes, returns events), app (web UI), and CLI plus SDK.
- Contract packages: `@bb/server-contract` and `@bb/host-daemon-contract`.
- Task walkthrough: the CLI call `bb thread spawn` with project and prompt options creates a thread row in SQLite, commonly with initial status `starting`, before any agent process exists.
- Environments: an existing directory or a managed one, which can be an isolated Git worktree. Lifecycle given as provisioning, ready, retiring, destroying, destroyed. An environment identifies both host and workspace.
- The server sends a `thread.start` command to the daemon over a WebSocket used as an RPC protocol; the command result is separate from the stream of thread events.
- The daemon passes the thread to `@bb/agent-runtime`, which has adapters for Codex (app-server protocol), Claude Code, Pi (via its SDK bridge) and agents implementing the Agent Client Protocol. Adapters convert provider output into shared thread events.
- Example events: `turn/started`, a command awaiting approval, a file change completing, `turn/completed`, provider errors.
- Event queue: ordinary events batched for up to 100 milliseconds; important events (approvals, completed items, completed turns, interruptions, non-retrying errors) flush immediately. The queue is in memory, so events are lost if the daemon crashes before delivery.
- The server validates that each thread belongs to the posting daemon's host and writes events in one SQLite transaction, assigning a monotonically increasing per-thread sequence number. The event table stores thread, environment, turn, provider thread, event type, item identity, data, timestamp and server sequence. Clients can ask for everything after a given sequence.
- Thread state machine: idle, starting, active, stopping, with error; transitions driven by events such as `run.preparing`, `run.started`, `run.succeeded`, `run.failed`, `stop.requested`, `stop.settled`, applied with compare-and-swap writers, and stale events become recorded no-ops.
- Manager threads are ordinary threads given the bb CLI through a built-in skill, using `bb thread wait` and `bb thread output` among other commands.
- One bb server can enroll several machines, with per-host project paths. Security: the author says bb docs warn that binding the server to a public interface exposes an unauthenticated command and file-reading API; use the managed connection or a private network such as Tailscale.
- Plugins can add server behavior, CLI commands, skills, automations and UI panels using the same APIs as the built-in app.
- A single SQLite database is the source of truth; one server owns one coordination domain.
- Stated limits: bb is young, the repository says the core architecture is stable while workflows evolve; normalizing events does not make providers identical (resume, approvals, models, tool semantics differ); remote hosts widen the trust surface.
- Quick start given by the author is `npx bb-app@latest`, then open `http://localhost:38886`.

## Relevance to session sharing

- bb thread events are an ordered, server-sequenced, provider-neutral stream, a natural source for exporting session records; the Pi adapter and ACP adapter are the integration points named.

## Related

- bb (getbb.app, get-bb/bb), Pi, Codex, Claude Code, Agent Client Protocol, T3 Code.
