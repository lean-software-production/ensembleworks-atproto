# Company session feed

Minimal Node 24 server and browser UI. The server polls `@ensemble/transport.listEvents` across every page in the company PDS Space; it never reads Claude logs or a local session database. Browser polling runs every five seconds. Cards show writer identity, project/repo where present, first recorded time, title and prompt preview. Every record remains inspectable, including unknown record types, native JSON primitives, tool blocks and branch metadata.

Start the complete stack using the root prototype runbook. The Compose feed is at **http://localhost:3100** (container port 3000).

For a local feed against the already bootstrapped PDS:

```sh
FEED_ACCOUNTS_FILE=.local/accounts.json node --env-file=.local/feed.env packages/feed/src/main.ts
```

The local command defaults to port 3000; set `PORT=3101` if occupied. `FEED_ACCOUNTS_FILE` supplies service, Space, company reader credentials and DID-to-name labels. Alternatively set `PDS_URL`, `PDS_IDENTIFIER`, `PDS_PASSWORD`, `COMPANY_SPACE` and optional `PDS_COLLECTION`. The credentials never enter browser responses. `FEED_LOGIN_PASSWORD` and `FEED_SESSION_SECRET` (at least 32 characters) are mandatory. Use `FEED_SECURE_COOKIE=true` behind HTTPS. Do not expose the plain HTTP prototype to an untrusted network.

A shared company password protects the HTML, JavaScript and data API; the login page, static stylesheet and credential-free health check are public. Successful login sets an eight-hour signed HttpOnly, SameSite=Strict cookie. Forms require a same-host Origin. Sign out clears the cookie. This prototype login has no per-person login, rate limiting, password recovery or centralized session revocation; restart with a new signing secret to invalidate existing cookies. Per-person *authorship* comes from authenticated PDS writer DIDs, independently of the shared feed reader.

The UI uses only DOM `textContent` for native data. No native HTML or markdown is interpreted. A restrictive CSP blocks inline scripts, object embedding and framing. Full native payloads appear verbatim in expandable, scrollable text panels; the metadata panel retains URI/CID, ordering, parent and source fields. Custom titles take precedence over generated titles and summaries. The feed prefers transport `authorDid`; its fallback understands Space record URIs, whose first DID is the authority, not the writer.

## Verification

```sh
npm test -w @ensemble/feed
npm run typecheck -w @ensemble/feed
FEED_TEST_URL=http://localhost:3100 node --env-file=.local/feed.env --test packages/feed/test/live.test.ts
```

The live test requires synthetic watcher fixtures already published to the real PDS. It checks unauthenticated rejection, login, complete record counts, raw payload preservation and expected event types. Override `FEED_EXPECT_TYPES` with a comma-separated list if necessary. Other unknown envelopes remain visible and do not fail payload-format checks.

Browser smoke check uses an explicitly opened BB browser session on the same host:

```sh
bb browser-automation open --backend local --headless --machine HOST_ID --json
node --env-file=.local/feed.env packages/feed/test/browser-check.mjs SESSION_ID HOST_ID http://localhost:3100
```

The runner temporarily writes a private script containing the login password and removes it afterward; it prints only verification results. It verifies actual browser form login, cards and native inspector, and absence of interpreted HTML nodes. For refresh validation, append a synthetic event to the demo watch directory, then observe the event without navigating/restarting the feed. Browser state retains selection and expanded inspectors during refresh. Never use personal session stores as fixtures.

## Prototype limits

The server loads a complete Space snapshot on each poll and coalesces concurrent reads. It rejects repeated pagination cursors and incomplete snapshots rather than silently dropping records. It is intended for a small overnight demonstration, not large histories. A failed read returns a generic 502 without upstream credentials; the browser displays the error and retains the last successful snapshot. The health check indicates HTTP liveness, not PDS availability. A 30-second response deadline does not cancel an already-running multi-page transport read.

Cross-stream ordering uses the recorded timestamp then stream/source order and URI; this is a deterministic view, not a reconstruction of a branch graph. Missing project/time/prompt fields are labeled, never invented. Display parsing can round very large native JSON numbers, but the complete native event panel preserves the exact `payloadJson` text supplied by the protocol.
