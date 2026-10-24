# get-bb/bb#5350: provider-pi bridge: resumed session can use a stale extensionPath from a dead bridge worker temp dir (source notes)

> Source: https://github.com/get-bb/bb/issues/5350
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-07 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue: user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-572fe878/001.md.
> Work: get-bb/bb#5350
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

Bug report get-bb/bb#5350 about the provider-pi bridge, where a resumed session may use a stale extension path pointing into a dead bridge worker's temp directory. Opened by cameronm123 on 2026-10-11; still open. Labels: providers, provider-pi, no-repro. One comment from the triage bot.

## Key facts

- Symptom: a pi-provider thread failed at startup with `pi exited (code 1)`; pi could not load the bb extension because a referenced tools JSON file was missing (ENOENT).
- Two different per-worker temp roots (`bb-provider-bridge-provider-pi-*`) appeared in one spawn: the `--extension` path came from an old worker, while the `PI_BB_TOOLS_FILE` environment variable pointed into the current worker's directory (pid 92942, 2026-10-10 04:11 UTC), and that file was already gone.
- The reporter says the user's `~/.pi` config (settings, extensions, auth) was unaffected.
- Environment: bb 0.46.0, macOS, plugin `provider-pi`, pi 1.1.0.
- Reporter's diagnosis (from the host artifact): `spawnAndVerify()` writes `pi-tools-${process.pid}-${Date.now()}.json` into the scratch dir, spawns pi with `--extension` and `PI_BB_TOOLS_FILE`, and deletes the tools file on child exit. The worker temp dir is per-process and force-removed on exit; `bb-pi-extension.mjs` is staged per worker (`requireExtensionPath`).
- Hypothesis: a resumed or forked session received a persisted `extensionPath` from an earlier worker that the new worker never staged.
- Suggested fix: treat a persisted `extensionPath` as untrusted on start or resume, verify it lies inside the current worker's temp root, or always restage per session like the tools file.
- Workaround: retry the thread or start a new pi thread.
- Bot triage (2026-10-11): Bug, Priority High, Effort Medium; NOT REPRODUCED, root-cause confidence low; real Pi resumed and forked successfully in two clean checkouts of `origin/main` (`3912f4aae`); current main builds worker-local extension and tools paths rather than restoring a persisted one; no PR opened.

## Related

bb provider-pi plugin; pi extensions and `--extension` flag; bb provider bridge worker; other bb pi resume problems.
