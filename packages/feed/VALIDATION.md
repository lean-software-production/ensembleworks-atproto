# Feed validation — 2026-11-17

Implemented and checked against the running published Bluesky TypeScript PDS and company Space, with synthetic fixtures only.

- `npm test -w @ensemble/feed`: six unit/HTTP tests passed; opt-in live test skipped by default.
- `npm run typecheck -w @ensemble/feed`: passed.
- `FEED_TEST_URL=http://localhost:3100 node --env-file=.local/feed.env --test packages/feed/test/live.test.ts`: passed against the real PDS after the CLI published its synthetic corpus. Unknown non-protocol records also remained visible.
- `browser-check.mjs`: passed real browser form login, session cards, complete native inspector and absence of interpreted native HTML. Browser reported six cards, 22 events at 08:06:48 UTC; other reviewers were adding fixtures concurrently.
- Live append: appended synthetic UUID `feed-browser-append-20261117` to the explicitly synthetic running watcher. Selected fixture session remained open; the new event appeared through normal polling without navigation or feed restart. Verified literal image-handler and script text, no inserted `img`/`script` nodes and no execution marker. Browser reported eight sessions/27 records at 08:07:28 UTC while concurrent tests were active.
- Visual screenshot inspected: readable two-column card/timeline page, author labels, project, date, refresh state and expandable native content. Screenshot retained in BB thread storage `feed-evidence/feed-20261117.jpg`.

Browser validation caught an HTTP-only test gap: `Referrer-Policy: no-referrer` made browser form Origin null. The policy is now `same-origin`; null/invalid origins receive 403. Real browser login subsequently passed.

Space writer attribution uses transport `authorDid`, with a Space URI fallback. Tests explicitly cover two writers with identical native session IDs. Custom titles take priority over generated names and compaction summaries. A final model test verifies unknown events without session IDs join the unique session in the same author/stream; ambiguous streams remain separate. Infrastructure was asked to include that final change in its next image build.

PDS outage, restart/persistence, oversized payload and broader independent security validation are owned by the manager's reviewer, not claimed by these component checks. See README for scale and prototype authentication limits.

## Final rebuilt image check — 08:14 UTC

Infrastructure confirmed running image source hashes match final feed model and transport. After the reviewer's coordinated restart suite, reran `browser-check.mjs`: login, cards, complete inspector and no interpreted native HTML passed; browser reported **14 sessions / 65 events**, with nine events in the selected session. Reran the real-PDS HTTP integration test successfully. Inspected the final screenshot and retained it as `feed-evidence/feed-final-20261117.jpg` in BB thread storage. Final stream grouping is now included in the tested image. Infrastructure reports the independent outage/restart suite passed; the reviewer's own report remains the authority for those checks.
