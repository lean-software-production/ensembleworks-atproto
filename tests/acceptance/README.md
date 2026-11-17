# Real prototype acceptance

Run from the repository root after `npm run up`. These tests publish only generated synthetic data to the real private pilot Space; they leave it there for inspection. They read `.local/accounts.json` and `.local/feed.env` inside scripts and do not log secrets. Never point them at personal Claude logs.

```sh
node --import tsx tests/acceptance/live.ts
ACCEPTANCE_LARGE=1 node --import tsx tests/acceptance/live.ts
# Coordinate this window with everyone using the stack:
ACCEPTANCE_LARGE=1 ACCEPTANCE_DISRUPT=1 node --import tsx tests/acceptance/live.ts
```

The final command stops/starts PDS and restarts postgres, PLC, PDS and feed, preserving volumes. Failure during the outage uses `finally` to start PDS again. It requires Docker access. `FEED_TEST_URL` defaults to `http://localhost:3100`. Fixtures/checkpoints and a successful summary are retained in ignored `.local/acceptance-TIMESTAMP/`; no passwords are written there. Each run uses a unique namespace. The test exits after stopping its own watcher; the demo watcher is independent.

`live.ts` launches the actual CLI child process, asserts exact PDS readbacks through Bob's account, and checks the authenticated feed API. It verifies initial import, all representative native types, invalid timestamp metadata, partial and malformed lines, nested files, repeated scans, graceful/SIGKILL restarts, numbered rotation and UUID replacement. The optional large event includes Unicode, quotes and backslashes so raw native byte length differs from serialized envelope size; exact payload and SHA-256 must match. Disruptive mode verifies recovery even after pending source truncation, then exact records/CIDs after Compose restart.

For browser checks, open an explicit local headless session and retain its returned ID:

```sh
bb browser-automation open --backend local --headless --machine HOST_ID --json
node tests/acceptance/browser.mjs SESSION_ID HOST_ID http://localhost:3100
bb browser-automation close SESSION_ID --json
```

The browser test uses the real login form, checks every acceptance event's complete native text, checks hostile markup stays text, then imports another synthetic event through the CLI and verifies browser polling adds it without navigation. It uses a temporary mode-600 login script removed in `finally`; it prints only assertions. Run without concurrent feed writes/rebuilds to keep the card index snapshot stable.

Additional account isolation/anonymous/impersonation assertions: `node infra/transport-check.mjs`. This checks live PDS, not a fake transport. Tests do not prove fresh-volume installation, host reboot, membership revocation, interrupted individual chunk writes, or production readiness. See `docs/prototype-review.md` for actual execution evidence and limits.
