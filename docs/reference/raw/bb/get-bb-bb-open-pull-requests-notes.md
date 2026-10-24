# get-bb/bb: open pull requests (source notes)

> Source: https://github.com/get-bb/bb/pulls
> Resolved: https://api.github.com/repos/get-bb/bb/pulls?state=open&per_page=100
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-11 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub PR list is user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-3add5ba4/001.md.
> Work: get-bb/bb:pulls
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A snapshot of the first page of open pull requests for the get-bb/bb repository (the bb agentic IDE), taken through the read-only GitHub REST API on the collection date. Titles, authors and creation timestamps only; 100 entries returned. The listing is a moving target and the entries are user content under GitHub's terms. Creation times in the snapshot run from 2026-10-20T00:54:22Z up to 2026-10-24T05:50:09Z.

## Key facts

- Most prolific authors in the snapshot: ymichael, brsbl, alexandre-vl, plus vznh, smsunarto, pascal-de-ladurantaye, luketraas, aotd1, Willhong, and a bot account bb-slop-cop[bot]. Several entries are marked draft.
- Plugin architecture themes: a bundled Git plugin is being extracted from core (#6057 draft, #6157 and #6165 for parts A and B moving git reads, the Diff tab, Info git rows and the composer segment into it); a GitHub plugin pull-request inbox (#6037); plugin-rendered interactions in ThreadChat (#6072); plugin lifecycle tooling for update ranges, rollback and `bb plugin track` (#6042, #6043, #6044, #6045); containing plugin errors after reload (#5967); a single change-message model for core and plugin live data (#6028, draft); avoiding full-page restyles when plugin stylesheets load (#6148); and a sidebar thread-row slot with the GitHub PR badge (#6145).
- Threads and sub-threads: child threads starting on the parent's service tier and documenting what a child inherits (#6112); active child threads shown as rows with a count chip (#6009); parent thread rows leading with disclosure and counting sub-threads (#5910); local workflow launchers kept out of delegation inference (#6035); withholding Claude Code subagent tools when provider subagents are disabled (#6084).
- Provider and agent support: Pi service tiers Fast and Ultrafast (#6154) and a Long cache tier for the Pi provider (#6097); installing Pi with bb's own runtime when Node.js is missing (#5943); installing Codex without Node.js and asking for Node.js before a Pi install that cannot run (#5930); offering Codex on a free ChatGPT account (#5998); normalising Codex guardian notifications as provider warnings (#5934); native Claude Code discovery outside PATH (#5948).
- Remote and multi-machine behaviour: showing a thread whose machine is offline as waiting (#6176); resuming an active provider machine whose daemon is gone (#6160); keeping a supervised host daemon running when a memory killer stops it (#6159); frp-based `bb connect next` work-connection and 404 changes (#6207, #6206); retrying failed connect gate lookups before answering 502 (#5886); iOS share target with durable draft imports (#6152, draft); phone command prefetch changes (#6219).
- Performance and storage: compressing realtime WebSocket pushes with permessage-deflate (#6209); watching each viewed thread's storage directory rather than the storage root (#6213); caching large timeline pages within a shared byte budget (#6000); shrinking timeline pushes (#6220); lowering CPU priority for agent processes, terminals and setup scripts (#6216); archiving threads while keeping local work safe (#5957) and a guide to archiving and storage (#6041, draft).
- Updates and telemetry: updating bb once all threads finish (#6203); resuming threads after an update interrupts them (#6098, draft); anonymous app update telemetry behind a flag (#6099, draft); per-install holdouts with an A/A check (#5980, draft).
- No pull request in this snapshot mentions AT Protocol, ATProto, sharing of sessions, or Bluesky by title; relevance to the project is in the plugin extension points, thread and sub-thread model, and Pi provider support.

## Related

- Other get-bb/bb issues (separate sources)
- bb plugin system and Extend bb documentation (#5911, draft)
