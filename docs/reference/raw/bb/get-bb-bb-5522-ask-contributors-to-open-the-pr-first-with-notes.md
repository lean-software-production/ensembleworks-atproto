# get-bb/bb#5522: Ask contributors to open the PR first, with maintainer edits on (source notes)

> Source: https://github.com/get-bb/bb/pull/5522
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-01 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub PR. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-18d4c7e7/001.md.
> Work: get-bb/bb#5522
> Quotations: 0 characters verbatim in this file; 0 of 90 allowed for this work across the knowledge base.

## About this source

A merged GitHub pull request (number 5522) on get-bb/bb by ymichael, changing the contribution process. The description is marked as agent generated. These are factual notes, not the original text.

## Key facts

- Purpose: contributors previously needed approval in Discord before opening a pull request; the change has them open the PR first from their fork with the option allowing edits by maintainers enabled.
- Files changed: `CONTRIBUTING.md`, `.github/workflows/pr-gate.yml` and a workflow test file; 3 files changed, +80/-7.
- The PR gate workflow keeps its allow-list check and adds a rule that closes any PR from a personal-account fork when `maintainer_can_modify` is false. Organization forks, branches in the main repository and deleted forks are exempt.
- Non-approved authors are told the automatic close is expected and are asked to post the PR link in Discord so a maintainer can add them to the allow list and reopen.
- The author tested the workflow script with a fake `gh` command across eight cases; it had not yet run on GitHub at merge time.
- The description ends with a Claude Code attribution line.

## Related

bb contribution workflow. Little relevance to ATProto session sharing; it may only illustrate that bb development is heavily agent-assisted (observation).
