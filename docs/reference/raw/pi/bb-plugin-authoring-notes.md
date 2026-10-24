# Bb Plugin Authoring (source notes)

> Source: https://www.skillsdirectory.com/skills/get-bb-bb-plugin-authoring
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-06 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: all-rights-reserved — No license statement on the page. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/skillsdirectory-com-ec6e5dc4/001.md.
> Work: https://www.skillsdirectory.com/skills/get-bb-bb-plugin-authoring
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A Skills Directory listing for the skill bb-plugin-authoring from the get-bb author, mirroring the SKILL.md in the get-bb/bb repository (plugins/bb-guide/skills/bb-plugin-authoring). It carries directory metadata plus the skill text. Listing says Added August 31, 2026. The page states no license, so these are notes.

## Key facts

- Directory metadata: 4,140 stars, security grade A (100/100), scanned October 6, 2026, 19 files, works with cli and api.
- Skill purpose: create or change BB plugins and Plugin SDK extensions, covering CLI commands, agent tools, providers and UI surfaces.
- A BB plugin is a TypeScript package that may add server behavior, agent capabilities, host-rendered UI or a frontend bundle.
- The skill says the current SDK types and repo source are the contract and the installed BB version decides the exact API.
- The Plugin Guide is available inside bb or at https://getbb.app/plugin-guide.
- Scaffold with `bb plugin new <name>`; the scaffold includes frontend files that should be removed for a headless plugin (remove `bb.app`).
- New public Plugin SDK surfaces start with an experimental underscore prefix and an entry in `docs/api_to_audit.md`, plus a Plugin Guide card and API inventory in the same change.
- Reference files in the skill cover quickstart, distribution (Git or npm release, custom marketplaces), backend foundation, backend SDK (projects, environments, threads, interactions, provider models, browser sessions, event history, plugin RPC), backend events (lifecycle, environment providers, HTTP, RPC, realtime, schedules), machines, CLI and agent tools, providers, provider bridge and ACP exports, UI lifecycle, and several frontend and testing references.
- Frontend extension points named: `definePluginApp`, thread header, sidebar replacement, homepage, settings, navigation, thread panels, source and diff renderers, message and timeline renderers, composer.
- Contract rules: parse freeform input at the boundary, keep secret settings on the server, treat frontend parameters and persisted values as untrusted, return bounded CLI and tool output, dispose every service, schedule and listener.
- Run `bb plugin types` when SDK declaration versions may drift and `bb plugin build` before install, release or marketplace submission.
- Install command shown for the directory: `npx -y skills add get-bb/bb`.

## Related

- get-bb/bb repository, bb Plugin Guide, bb plugin SDK provider bridge and ACP exports.
