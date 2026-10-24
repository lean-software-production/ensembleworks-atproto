# ATProto OAuth and Permissions

> Sources: atproto.com OAuth spec and Permissions spec (Bluesky Social PBC and Contributors, CC-BY), undated; haileyok/cocoon `oauth/scopes` Go package docs via pkg.go.dev (MIT); AlohaSocial/social PR #2542 (notes only); all collected 2026-10-23; source inventory: OAuth - AT Protocol (Bluesky Social PBC and Contributors, AT Protocol website; Unknown); Permissions - AT Protocol (Bluesky Social PBC and Contributors, AT Protocol website; Unknown); scopes package - github.com/haileyok/cocoon/oauth/scopes - Go Packages (Copyright (c) 2025 me@haileyok.com, haileyok/cocoon (docs via pkg.go.dev); Unknown); AlohaSocial/social#2542: feat(atproto): granular OAuth permissions, and trusted apps (source notes) (attributed source notes; Unknown)
> Raw: [atproto OAuth spec](../../raw/atproto/oauth-at-protocol.md); [atproto Permissions spec](../../raw/atproto/permissions-at-protocol.md); [cocoon oauth/scopes package](../../raw/atproto/scopes-package-github-com-haileyok-cocoon-oauth-scopes-go.md); [AlohaSocial/social PR 2542 (notes)](../../raw/atproto-apps/alohasocial-social-2542-feat-atproto-granular-oauth-notes.md)
> Updated: 2026-10-23

## Overview

Apps act on a user's PDS through a specific atproto *profile* of OAuth. It is built on OAuth 2.1 with authorization code only, and it makes PKCE, PAR and DPoP with server nonces mandatory. Clients register themselves automatically by publishing a client-metadata JSON document whose URL *is* the `client_id`, so there is no shared client secret. Access is narrowed by **granular permissions** (`repo`, `rpc`, `blob`, `account`, `identity`), which can be bundled into **permission sets** that are published as Lexicons. A session-sharing app should ask for write access to *its own* session-record collections only. Space access for private sessions uses the separate `space:` scope described in [ATProto Spaces (Permissioned Data)](atproto-spaces-permissioned-data.md).

## OAuth profile essentials

- **Identity.** The `atproto` scope is required on every session. Tokens return the account DID in `sub`. A client must independently resolve the DID to confirm the Authorization Server is authoritative for the account. Login-only use ("Login with atproto") can request just `atproto`.
- **Client types.**
  - *Confidential* clients authenticate with a JWT client assertion (`private_key_jwt`) and may get longer sessions.
  - *Public* clients do not.
  - The spec notes that client-metadata registration was still an IETF draft "As of October 2026".
- **DPoP** is required for token requests and resource requests alike.
  - Server nonces rotate with "a maximum lifetime of 5 minutes".
  - `ES256` must be supported.
  - Each request carries a unique `jti`.
- **Token lifetimes** (spec guidance):
  - Access tokens should last under 30 minutes. If they cannot be individually revoked, the maximum is 15 minutes, and 5 minutes is recommended.
  - Untrusted public clients: overall session and individual refresh tokens limited to 2 weeks.
  - Confidential clients: the session may be unlimited, with refresh tokens limited to 180 days.
  - Refresh tokens are generally single-use, so clients need locking around refresh.
- **Transitional scopes** (`transition:generic`, `transition:chat.bsky`, `transition:email`) mirror the old App Password levels. They are coarse, and new apps should prefer granular permissions.
- **Security.** Authorization servers fetch client metadata from arbitrary URLs, so they need SSRF-hardened HTTP clients. `client_name`, `client_uri` and `logo_uri` are unverified and should not be shown for unknown clients.

## Granular permissions

| Resource | Grants | Notes |
|---|---|---|
| `repo` | create / update / delete records in the public repo, per collection NSID | Wildcard `*` is allowed in scope strings but not inside permission sets. Partial wildcards are not supported. |
| `rpc` | service-auth calls and PDS-proxied calls, per method (`lxm`) and audience (`aud`) | `aud` and `lxm` cannot both be wildcard. |
| `blob` | uploads by MIME `accept` pattern | Cannot appear in permission sets. |
| `account`, `identity` | account status, email, handle, and similar | |
| `include` | a permission set by NSID | `aud` can be passed down with `inheritAud`. |

- Scope string syntax is `resource:positional?key=val&…`, for example `repo:app.example.profile?action=create&action=update`.
- **Permission sets** are Lexicon schemas, for example `com.example.authBasicFeatures`, with user-facing titles. They may only reference resources in their own NSID namespace or its children. Authorization servers resolve them dynamically and cache them. The recommended stale lifetime is 24 hours, which the spec calls a firm upper bound. Sets can grow over time without forcing users to re-authenticate. Unknown resources or parameters inside a set must be ignored.

## Implementations seen in the wild

- **cocoon** (Go PDS by haileyok, `oauth/scopes`) parses and validates the granular resources plus legacy scopes for PAR-time validation and resource-server enforcement. It already includes space-scope helpers such as `ExpandSpaceCollections`, `ParseSpacePermission` and `SpaceCollectionsFromLexicon`. This shows `space:` scopes landing in third-party PDS code.
- **AlohaSocial/social PR 2542** (merged, October 2026) implements granular permissions in a PHP authorization server and client:
  - It resolves permission sets via the `_lexicon` DNS TXT record and the `com.atproto.lexicon.schema` record, cached at most a day.
  - It enforces each write inside `applyWrites` separately.
  - It refuses bad scopes at PAR with `invalid_scope`.
  - It shows `client_name` and logo only for admin-listed trusted apps.
  - Its interop test shows a client with only `repo:app.bsky.feed.post?action=create` can post, while timeline and like calls get 403 `InsufficientScope`.

## Implications for a session-sharing app

- Publish the session Lexicons under one namespace with a permission set, for example `…authSessions`. The consent screen then shows a human title, and new record types can be added without re-consent.
- Request `repo:` for the session collections, `blob:` for attachments (requested directly, since blobs cannot go in sets), and `space:` grants for private team spaces.
- Use a confidential client (a backend) if long-lived background sync from a pi or bb plugin is needed. Public-client sessions are capped at 2 weeks.

## See Also

- [ATProto Spaces (Permissioned Data)](atproto-spaces-permissioned-data.md)
- [ATProto Repository, Records and Lexicon](repository-and-records.md)
- [Atmospheric Groups](atmospheric-groups.md)
