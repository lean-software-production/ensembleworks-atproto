# bb Project Status, Licensing and Contribution

> Sources: get-bb/bb repository metadata and README (Michael Yong / bb contributors, MIT), collected 2026-10-23; getbb.app landing page (Terragon Labs, notes only), collected 2026-10-23; get-bb/bb PR #5522 by ymichael (notes only), collected 2026-10-23; source inventory: get-bb/bb (Copyright (c) 2026 Michael Yong; get-bb/bb; Unknown); bb (source notes) (attributed source notes; Unknown); get-bb/bb#5522: Ask contributors to open the PR first, with maintainer edits on (source notes) (attributed source notes; Unknown); get-bb/bb: package.json (Copyright (c) 2026 Michael Yong, bb; Unknown); get-bb/bb: open pull requests (source notes) (attributed source notes; Unknown); get-bb/bb: LICENSE (Copyright (c) 2026 Michael Yong, get-bb/bb; Unknown)
> Raw: [get-bb/bb repository + README](../../raw/bb/get-bb-bb.md); [getbb.app landing page (notes)](../../raw/bb/bb-notes.md); [get-bb/bb PR 5522 (notes)](../../raw/bb/get-bb-bb-5522-ask-contributors-to-open-the-pr-first-with-notes.md); [get-bb-bb-package-json](../../raw/bb/get-bb-bb-package-json.md); [get-bb-bb-open-pull-requests-notes](../../raw/bb/get-bb-bb-open-pull-requests-notes.md); [get-bb-bb-license](../../raw/bb/get-bb-bb-license.md)
> Updated: 2026-10-24

## Overview

bb ("The agent IDE that builds itself", per the repo description) is a young, fast-moving MIT-licensed TypeScript project. Its README says core architecture is stable while workflows and surfaces still evolve. The captured license permits copying and modification subject to notice retention. bb's contribution gate rewards upstreaming instead: it requires contributors to open PRs from forks that let maintainers edit, and an allow-list workflow closes PRs from non-approved authors until a maintainer intervenes.

## Status at collection

- The repository `get-bb/bb` is MIT-licensed, primary language TypeScript, homepage getbb.app.
- Repo creation timestamp: 2026-02-24T22:32:40Z. Last push: 2026-10-24T05:55:31Z.
- Stars at collection: 4587. Forks: 692. Open issues: 720. These counts are volatile.
- Platforms: the desktop app supports macOS on Apple Silicon. The Linux x64 AppImage and Windows x64 installer are alpha. Elsewhere, run `npx bb-app@latest` and open `http://localhost:38886`.
- The landing page says bb is MIT-licensed end to end and invites organisations to fork it and deploy their own build. It lists Claude Code, Codex, Cursor, Pi, OpenCode, Grok, omp and Hermes as hosted agents, plus five more.

## Telemetry

Production runs send anonymous usage telemetry:
- what is sent: app starts, thread-creation counts, user-message counts and public plugin installs
- what each event carries: app version, install method, OS release, CPU architecture and Node version
- identification: a random per-install id

The README says no user, host, project, workspace or message content is attached. Development runs never send telemetry, and `BB_TELEMETRY=false` opts out. A sharing plugin that adds its own network traffic should be equally explicit.

## Contribution process (PR 5522, merged)

- Contributors previously needed approval in Discord before opening a PR. After this change they open the PR first, from a fork with the allow-edits-by-maintainers option enabled.
- The PR-gate workflow keeps its allow-list check. It now also closes PRs from personal-account forks when `maintainer_can_modify` is false. Organization forks, in-repo branches and deleted forks are exempt.
- Non-approved authors are auto-closed, and the closing message asks them to post the PR link in Discord so they can be allow-listed and reopened.
- The PR description is marked as agent generated, which matches bb's self-description as an IDE that builds itself.

## Implications for a temporary bb fork

- Licensing permits a fork. The MIT notice must be retained; see the license notice appended to the verbatim raws.
- An upstream path exists but is gated. Expect a Discord step and maintainer edits to your branch.
- The pace of change is high (see the push timestamp and open-issue count). Compatibility shims pinned to one build, like the one in [bb Pi Provider Integration](bb-pi-provider-integration.md), will rot quickly. A plugin built on public SDK surfaces is preferable to a fork wherever the surfaces suffice.

## See Also

- [bb Architecture and Data Model](bb-architecture.md)
- [bb Plugin System](bb-plugins.md)

## Repository manifest is a development artifact

The captured root package manifest identifies bb as a private module package with MIT licensing and a Node engine constraint. Its scripts orchestrate generated scaffolds, server, daemon and app development. The private package flag describes publication of that package; it does not contradict the repository license or imply that every bundled integration has the same release lifecycle.

## Open-PR inventory is not release evidence

The captured first page of open pull requests shows active plugin extraction, lifecycle tooling, provider integration, remote-host and storage work. Some entries are drafts. Their titles establish development directions, not merged behavior. No title in that page mentions ATProto session sharing, but a partial listing cannot establish the absence of all related work elsewhere in the project.

## License text and notice retention

The captured bb license grants MIT permissions subject to retaining its copyright and permission notice in copies or substantial portions, and disclaims warranty. The raw license packet retains that text. A repository manifest’s short license field is less complete evidence than this notice; third-party plugins still require their own license determination.
