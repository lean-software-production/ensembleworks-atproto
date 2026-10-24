# get-bb/bb#4809: Thread list: date group headings (Today, Yesterday, …) in the Custom organization's Threads section (source notes)

> Source: https://github.com/get-bb/bb/issues/4809
> Resolved: https://api.github.com/repos/get-bb/bb/issues/4809
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-08 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub issue; user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-5ca059fa/001.md.
> Work: get-bb/bb#4809
> Quotations: 15 characters verbatim in this file; 15 of 90 allowed for this work across the knowledge base.

## About this source

A feature-request issue in the bb repository (get-bb/bb#4809), opened by the GitHub user hxy91819 and still open at collection time. The issue is labelled `ui`. The description ends with an "AGENT GENERATED" marker, and a bot account (bb-slop-cop[bot]) added a triage comment. The issue was created 2026-10-03.

## Key facts

- The request is for date group headings (Today, Yesterday and so on) in the sidebar thread list when the organization mode is Custom.
- Today the `chronological` organization mode, labelled Custom, renders loose root items as one flat list with no separators.
- The existing chronology controls are `chronologicalSort` and `sortDirection`; there is no grouping preference.
- Proposed: a synced Thread list preference `dateGrouping`, default `true`, exposed in the UI under Organize, Rows, Date groups, and via the CLI as `bb thread-list prefs set dateGrouping false`.
- Buckets use the local calendar day of the sort field: `updatedAt` for Updated, `createdAt` for Created. Buckets are Today, Yesterday, weekday name for 2-6 days ago, Previous 30 days for 7-29 days ago, then localized month and year.
- Pinned items, custom sections, By project and By machine views would be unchanged. Alphabetical sort would disable the menu item and hide headings.
- Nested children and worktree groups stay under their root thread; headings are display-only, not collapsible, draggable or keyboard jump targets.
- Labels would refresh at local midnight and on window focus.
- The author's prototype is on a fork branch based on `desktop-v0.45.0`: 3 commits, 13 files, +519/-4.
- Touched files named: `plugins/thread-list/shared/preferences.ts`, `plugins/thread-list/app/list/dateGroups.ts`, `plugins/thread-list/app/list/ProjectRow.tsx`, `plugins/thread-list/app/list/SidebarViewItems.tsx`, plus docs including `docs/configuration.md`.
- The thread-list is implemented as a plugin under `plugins/thread-list`, and has a `SKILL.md` and `PLUGIN_OVERVIEW.md`, showing that bb plugins ship agent skill docs.
- The author notes CONTRIBUTING.md asks for an issue before a PR for UI changes, so the PR would follow sign-off and contributor approval.
- Issue #1533 is cited as a related request for date dividers inside the thread timeline rather than the sidebar.
- The triage bot classified it as Type Feature, Priority Low, Effort Medium, and opened no pull request.

## Related

- get-bb/bb repository (MIT per license hint), bb thread-list plugin, `bb thread-list prefs` CLI.
