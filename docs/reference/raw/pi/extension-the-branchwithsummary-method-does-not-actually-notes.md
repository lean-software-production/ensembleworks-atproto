# Extension: The branchWithSummary method does not actually implement Tree Navigation (source notes)

> Source: https://github.com/earendil-works/pi/issues/1781
> Resolved: https://api.github.com/repos/earendil-works/pi/issues/1781
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-12 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue; user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-a83ba21f/001.md.
> Work: earendil-works/pi#1781
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

GitHub issue earendil-works/pi#1781, opened by @ttttmr against the pi coding agent, with two comments (one from @badlogic, one from the reporter). The issue is closed (completed) and labelled bug. Reported against version 0.55.4. This is a discussion of session-tree mutation from extensions.

## Key facts

- The reporter called `ctx.sessionManager.branchWithSummary(...)` from inside a tool, in their pi-context extension, and found that the session tree view showed a switch but the model still behaved as if it saw the other branch's messages.
- Expected behaviour stated by the reporter: after `branchWithSummary`, the actual LLM context should follow the tree.
- The reporter supplied a repro that loads the extension with the `pi` CLI with the flags `-ne`, `-ns`, `--skill` and `-e` and a task that tags a start point, writes a random token to a file, checks out the tag and asks the model to guess the token.
- A shared pi.dev session link was used as the minimal case, which shows sessions can be shared as web URLs.
- The maintainer @badlogic traced the cause to extension-side misuse of the context API, not a bug in `branchWithSummary` itself.
- The extension cast the tool context's session manager to a writable `SessionManager`, bypassing a read-only contract, and mutated session state during an active agent loop. The tree updated but the in-flight context buffer was not swapped mid-turn, hence the desync.
- Recommended path for tree switching: command-context navigation such as `ctx.navigateTree(...)`, which keeps message state and session state synchronized.
- The maintainer copied the extension code into the repo under `packages/coding-agent/examples/extensions/pi-context/` and noted it did not type-check as is.
- The maintainer also said runtime guards should be hardened so unsupported session mutations from tool or event context fail fast with a clear error.
- The reporter replied that command context can only be triggered by humans, and asked whether `ctx.navigateTree` could be exposed safely in specific events such as `agent_end`.
- Timeline: created 2026-03-03T15:22:01Z, closed 2026-03-03T15:54:38Z.

## Related

- pi session manager and session tree (`/tree`), pi extensions API.
- Earlier discussion referenced by the reporter: badlogic/pi-mono issue 1376.
- ttttmr/pi-context extension.
