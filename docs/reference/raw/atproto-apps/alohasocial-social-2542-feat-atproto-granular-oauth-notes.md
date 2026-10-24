# AlohaSocial/social#2542: feat(atproto): granular OAuth permissions, and trusted apps (source notes)

> Source: https://github.com/AlohaSocial/social/pull/2542
> Collected: 2026-10-23
> Published: Unknown
> Representation: Source notes written by fetcher-02 from the fetched original. NOT a verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. Numbers, dates, quotes and code identifiers were mechanically checked against the original.
> License: GitHub-ToS-user-content — GitHub pull request; user content. Verbatim export not permitted; full fetch kept only in the git-ignored cache build/reference-wiki/fulltext/github-com-f502489b/001.md.
> Work: AlohaSocial/social#2542
> Quotations: 59 characters verbatim in this file; 59 of 90 allowed for this work across the knowledge base.

## About this source

A merged pull request in AlohaSocial/social (PR 2542, author @karlitschek), titled "feat(atproto): granular OAuth permissions, and trusted apps". Created and merged within two days in October 2026 (API metadata). It changes 32 files, +1163/-38. The description states it was written with AI assistance (Claude Code). The repo is a PHP project that acts as a Bluesky/atproto OAuth authorization server and client.

## Key facts

- Purpose: let an app signing in with Bluesky OAuth request atproto granular permissions (atproto.com/specs/permission) instead of the all-or-nothing `transition:generic`.
- Supported permission kinds: `repo:` (records per collection and action), `rpc:` (methods at a service), `blob:` (uploads by type), `account:email`, `identity:`, and `include:` (permission sets).
- Permission sets are resolved via the `_lexicon` TXT record of the set's authority, then that DID's `com.atproto.lexicon.schema` record, cached at most a day. Only `repo` and `rpc` permissions inside the set's own namespace are accepted (the spec's namespace-authority rule). An `rpc` permission that inherits takes the `aud` named by the `include`.
- Enforcement per call: writes checked per collection and action (each write inside `applyWrites` separately), AppView calls per method and service, service-auth tokens per method and audience, uploads per type. `getSession` is always answered.
- Malformed scopes or unresolvable sets are refused at the pushed authorization request with `invalid_scope`. Transitional scopes and app passwords behave as before.
- Consent page: a sentence per scope, permission sets shown by their own title and detail (localised if available), and a mark on permissions that let an app act rather than only read.
- Trusted apps: an administrator may list client IDs; for those the consent page shows `client_name` and `logo_uri` (https only, host added to the CSP). Other apps are shown by address only.
- New classes named in the PR: `Atproto\OAuth\Permissions`, `PermissionSets`, `PermissionDescriber`; `ClientSession::permissions()`; setting `atproto_oauth_trusted`.
- Testing claims: PHP 8322 tests and JS 4194 tests; interop test signs in with `@atproto/oauth-client-node` using only `repo:app.bsky.feed.post?action=create`; posting works, timeline and like are refused with 403 `InsufficientScope`. The `include:` path cannot be tested end to end in CI because no DNS exists for `_lexicon` there.
- The only comment is an automated CodeRabbit notice that review was skipped.

## Relevance to session sharing

- Shows a worked implementation of scope enforcement per record collection, which is the mechanism by which an agent-session app could request write access limited to its own session-record collection.

## Related

- atproto permissions spec, permission sets, Lexicon resolution, `@atproto/oauth-client-node`, PR 2541 (stacked-on).
