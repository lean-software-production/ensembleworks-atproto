# get-bb/marketplace#410: Add plugin entry: hooks (source notes)

> Source: https://github.com/get-bb/marketplace/pull/410
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-07 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub PR: user content under GitHub ToS. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-6fe2a7e0/001.md.
> Work: get-bb/marketplace#410
> Quotations: 46 characters verbatim in this file; 46 of 90 allowed for this work across the knowledge base.

## About this source

A pull request in the get-bb/marketplace repository, number 410, titled "Add plugin entry: hooks", opened by MacHatter1 on 2026-09-29 and merged on 2026-10-02. It adds a marketplace entry for a bb plugin named hooks. Reviewer comments are from SawyerHood, written as automated notes from a Claude Code agent on behalf of the marketplace maintainer.

## Key facts

- Plugin purpose per the description: run shell commands or webhooks when bb thread events occur, and hold each outgoing message to a user-defined policy before it reaches the provider.
- Managed through a Hooks sidebar page, the `bb hooks` CLI, and bundled agent skills named `hooks` and `create-hook`.
- Source repository MacHatter1/bb-plugin-hooks (MIT); entry uses git semver range `^0.4.0`, resolving to tag `v0.4.0`. Plugin ID `hooks`, derived from package name `bb-plugin-hooks`.
- Plugin checks reported: typecheck passed; 87 tests passed; `bb plugin build` passed; used live in bb 0.43.4.
- Marketplace checks reported: build passed with 256 entries; marketplace tests 37/37; `npm run gate:v1` passed; one unrelated warning (entry `command-center` lacks a category).
- Security notes in the PR: gate hooks on `message.dispatch` may proceed, reject with a reason, or wait; they are capped at an 8-second dispatch budget and proceed on errors by default.
- Hook definitions are kept in plugin settings; run history (paged, 25 at a time) and secrets (AES-256-GCM encrypted) are stored in the plugin database. Webhook requests do not follow redirects; commands run with `/bin/sh` and with the server user's access on the machine hosting the bb server.
- Optional templates may post to third-party endpoints (Slack, Discord, PagerDuty, ntfy) only after the user configures credentials.
- The PR changes 6 files (+26/-0): `entries/hooks.json`, an icon, `overview/hooks.md`, and three screenshots; the overview is copied from the plugin repo's `PLUGIN_OVERVIEW.md`.
- Review history: on 2026-10-01 the maintainer agent reported that a clean install of Hooks 0.4.0 on bb 0.44.0 failed at frontend bundling because the `@hugeicons/core-free-icons` barrel referenced filenames with the wrong letter case on a case-sensitive Linux host. The author replied that v0.4.1 pins that dependency to 4.3.5 (where 6,025 references match filenames) and asked for re-test of tag `v0.4.1`.
- Approved on 2026-10-02 under the maintainer's "four admission criteria" (the release passed installation/loading on bb 0.44.0, source identity rechecked, format and CI pass).
- Illustrates the marketplace submission and agent-assisted review process for bb plugins.

## Related

get-bb/marketplace; bb plugin system; bb-plugin-hooks; bb `message.dispatch` gate hooks.
