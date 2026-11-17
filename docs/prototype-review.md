# Independent prototype acceptance review

Reviewer: `thr_v9p7v753gi`; manager: `thr_7bpmnfv8pr`. Reviewed 2026-11-17 against the shared working tree, using only synthetic logs and the real pinned Spaces PDS, official local PLC and Postgres. No component code, research, personal Claude stores, merges or public publication were changed by this review.

**Recommendation: accept the bounded local prototype, subject to the manager's final acceptance.** The required live watcher → private PDS → feed path passed. No unresolved material defect was reproduced within the tested scope. This is not production approval or a claim of unlimited payload support.

## Reproducible evidence

Run from the repository root; credentials are read only inside scripts, never included here. [Acceptance instructions](../tests/acceptance/README.md), [infrastructure runbook](prototype-infrastructure.md), [watcher semantics](claude-watcher.md).

| Command / check | Observed result |
| --- | --- |
| `node --import tsx tests/acceptance/live.ts` | PASS, `acceptance-1794902801787`, 12 native events |
| `ACCEPTANCE_LARGE=1 ACCEPTANCE_DISRUPT=1 node --import tsx tests/acceptance/live.ts` | PASS, `acceptance-1794903054564`, 14 native events; exact PDS/feed payloads, outage and full restart |
| `node tests/acceptance/browser.mjs SESSION HOST http://localhost:3100` | PASS after final startup: 52 acceptance events inspected byte-for-byte as native text; actual CLI append appeared without navigation |
| `ACCEPTANCE_LARGE=1 node --import tsx tests/acceptance/live.ts` after final `npm run up` | PASS, `acceptance-1794903266609`, 13 native events on final image |
| `node infra/transport-check.mjs` | PASS: live idempotency, writer attribution, cross-member read, pagination, outsider/anonymous denial, public absence, impersonation denial, maximum-size refusal |
| Final held-lock SIGKILL rerun of `live.ts` | PASS, `acceptance-1794903370289`, 13 events; OS lock confirmed held before kill |
| `npm test` | 24 passed, 0 failed, 1 optional live feed test skipped; separate real-stack tests above were executed |
| `npm run typecheck` | PASS across CLI, protocol, transport and feed |
| `npm run up` | PASS, exit 0 on existing stack; bootstrap reused pilot state, images rebuilt and services running |

After the final startup run, independent SHA-256 checks confirmed the running feed image matches host `model.ts`, transport `index.ts`, and CLI `watcher.ts` (including directory recovery).

The large fixture uses 220,000 repetitions of Unicode, quote and backslash characters inside a tool-result payload. This exceeds 750,000 native UTF-8 bytes and incurs additional JSON escaping overhead in the envelope. Equality is checked on the exact original JSON string and its SHA-256, not just a parsed object. The real PDS stores private chunks; feed and browser reconstruct the complete event.

## Checked acceptance criteria

- Actual CLI `watch` process imports an existing log, then receives appended prompt, assistant `tool_use`, user `tool_result`, title and unknown native event. Exact original payloads survive. Invalid native timestamp and numeric version remain in raw JSON without blocking the event.
- Incomplete final line is absent until completion/newline. A malformed completed line produces a visible issue; the next valid event publishes. Recursive subagent file publishes.
- Repeated scans and clean process restart leave values, CIDs and `capturedAt` unchanged. Actual SIGKILL restart acquires the checkpoint lock and publishes a subsequent append. A final targeted rerun additionally confirmed `flock --nonblock` failed because the lock was held immediately before killing the CLI; recovery still passed.
- Numbered rotation shares identity, adds only new events, and a repeated UUID updates in place. Pending content survives source truncation during an outage. Prior published archive records remain readable.
- Alice and Bob write separate records. Bob reads Alice's records. Both feed API and browser inspect exact native payloads; API asserts each writer DID rather than the authority DID in the Space URI.
- Oversized event successfully traverses actual CLI, PDS, feed API and browser. Public event **and chunk** collections are empty for both writers. Outsider transport read/write fails; infrastructure live check separately verifies anonymous access and author impersonation denial.
- Feed API returns 401 without login, page redirects to login, foreign-origin login is rejected. Actual browser form login succeeds. Hostile `img`/`svg` markup stays literal text with no injected elements or execution marker. Browser polling displays another actual CLI import without navigation.
- Coordinated PDS stop produces visible retry state and feed 502. Source is truncated after pending state exists. Restart publishes that pending event and feed recovers.
- Coordinated `docker compose restart postgres plc pds feed` preserves exact record values/CIDs and restores authenticated feed reads. Named volumes were retained. Stack was left running at PDS `localhost:2583`, feed `localhost:3100`, PLC `localhost:2582`.

## Defects and fixes verified

| Severity before fix | Finding | Independent verification |
| --- | --- | --- |
| High | Company authority DID mistaken for writer | Two different authenticated CLI writers correctly attributed by PDS/feed API; browser displays account names |
| High | Stale checkpoint lock prevented crash restart | Actual SIGKILL followed by a new watch process and successful append |
| High | Payload above 750k could never publish | Large Unicode/escaped tool output now round-trips with exact payload/digest, including feed/browser |
| Medium | Arbitrary native timestamp rejected whole event | Unknown event with `timestamp: not-a-date` and numeric version publishes unchanged |
| Medium | Browser form login failed due to Origin/referrer handling (found by feed owner) | Independent actual browser form login passes |

An intermediate large-run feed assertion failed while the old feed image was running during transport deployment; the final full run and browser reruns passed after rebuilding. An initial browser-test mismatch was a reviewer selector ambiguity between identically titled cards; the harness was corrected and rerun. Neither is an outstanding component defect.

## Remaining limits and untested criteria

- **Medium, documented bounds:** native payload limit 16 MiB; serialized envelope limit 20 MiB. Above-cap events fail visibly, with retry behavior; invalid native payloads above 16 MiB are retained only in source plus a validation issue. Removing that invalid source loses the ability to recover it. The acceptance run proves successful >750k publication, not arbitrary-size ingestion.
- **Low, documented source ambiguity:** arbitrary filename changes create distinct streams; no-UUID edits create new content identities; identical no-UUID rotation copies can collapse. Numbered UUID rotation/update was tested live; arbitrary rename and no-UUID ambiguity were reviewed in code/docs and covered by component tests, not independently exercised against PDS.
- Fresh empty-volume installation, host reboot, sustained large datasets, a PDS session lasting beyond expiry, membership revocation, and interrupted/corrupted individual chunk writes were not independently tested live. Missing/corrupt chunks have unit coverage; chunks can be orphaned after interruption and have no garbage collection.
- Browser access uses a company shared password and server-side company reader, not individual OAuth. Local development settings, dependency advisories and loopback deployment limits are documented by infrastructure. No production deployment was requested or assessed.
- No live Claude process was launched. Representative fixtures and arbitrary unknown types prove opaque retention; they cannot prove capture of events absent from files, deleted history, or attachment bytes referenced externally.

Browser verification used the local endpoint. The manager subsequently exposed the feed through BB Connect; remote proxy login/cookie behavior was not independently tested by this reviewer. Login compares the browser Origin host directly with the HTTP Host header; BB Connect must preserve the external Host and Origin consistently. Forwarded-host headers are not consulted. Cookies are host-only, HttpOnly and SameSite=Strict, so the proxy must pass Set-Cookie and Cookie through.

Final acceptance belongs to the manager. Reproducible tests and this report are the review deliverables.

Latest non-disruptive workspace checks: `npm test` and `npm run typecheck` exited 0. Raw local outputs: `/tmp/acceptance-final-tests.txt` and `/tmp/acceptance-final-types.txt` (temporary evidence; result counts above are retained in this report).
