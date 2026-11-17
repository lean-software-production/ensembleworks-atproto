# Local prototype infrastructure

Run from the repository root with Node 24 and Docker Compose:

```sh
npm ci --cache /tmp/ensembleworks-npm
npm run up
```

`npm run up` creates local secrets if absent, builds the local PLC directory, starts Postgres and the real Bluesky PDS, waits for its health endpoint, creates/reuses pilot accounts and the company Space, and builds/starts the feed. It never starts a watcher on personal logs. Infrastructure owns npm installs and the lockfile in this shared checkout.

- Feed: http://localhost:3100 (host 3000 was occupied). Login password is `FEED_LOGIN_PASSWORD` in ignored `.local/feed.env`.
- PDS: http://localhost:2583; health: `/xrpc/_health`.
- Local PLC identity directory: http://localhost:2582. No account identities are registered with the public PLC directory.
- Postgres is reachable only on the Docker network.

The `.local/accounts.json` file contains `{service,space,accounts:[{name,handle,did,password}]}`. Names are `company`, `alice`, `bob`, and `outsider`; handles are `pilot-NAME.test`. The first three have read/write membership. Outsider exists to test refusal. Files are mode 0600 and `.local` is ignored. Never print account passwords or commit these files. Bootstrap persists each credential before trying account creation so reruns can recover partial work. `node infra/bootstrap.mjs` reapplies the intended pilot membership.

## Pins and primary evidence

- Official PDS image: `ghcr.io/bluesky-social/atproto@sha256:70073bb96e55cfd967af0a10fcade42f0c85c1c372c81a61ee3f32601d14a741`.
- Image source revision: [`83d473dec69bbf19fe95fcbbb20a39842779db82`](https://github.com/bluesky-social/atproto/tree/83d473dec69bbf19fe95fcbbb20a39842779db82). Image reports PDS `0.5.57`, built November 13, 2026.
- Matching `@atproto/space`, `@atproto/crypto`, and protocol `@atproto/lexicon`: `0.0.0-spaces-alpha-20261113224550`, exact versions in manifests and npm lock.
- Official local identity server: `@did-plc/server` `0.0.1`, using its real PostgreSQL database, migrations, and operation validation. No mock identity store.
- Node image `24.11.1-bookworm-slim`; Postgres image `16.11-alpine`. The PDS image carries its own Node runtime.
- [Official alpha announcement](https://atproto.com/blog/atproto-spaces-alpha) identifies the alpha image and experimental status.
- [Pinned API handlers](https://github.com/bluesky-social/atproto/tree/83d473dec69bbf19fe95fcbbb20a39842779db82/packages/pds/src/api/com/atproto/space) and [pinned upstream tests](https://github.com/bluesky-social/atproto/blob/83d473dec69bbf19fe95fcbbb20a39842779db82/packages/pds/tests/_space.ts) are the implementation authority. The moving `permissioned-data` branch was inspected, then checked out at the image revision before implementation.

The current alpha differs from older wiki material. Bootstrap calls `com.atproto.space.createSpace` with `spaceType`, `skey`, and a `com.atproto.memberspace.policy` where both public flags are false; it calls `com.atproto.memberspace.putMembers`. The authority is the company account. Every person's records remain in that person's Space repo.

## Transport contract and authentication

```ts
import {createTransport} from '@ensemble/transport';
const transport = createTransport({
  service: 'http://localhost:2583',
  identifier: account.handle,
  password: account.password,
  space: companySpace,
  collection: 'com.ensembleworks.session.event', // default
});
await transport.authenticate(); // {did,handle}
await transport.putEvent(rkey, record); // {uri,cid}
await transport.listEvents({cursor,limit:100});
// {records:[{uri,cid,value,authorDid}],cursor?}
```

Account passwords establish a short-lived PDS session. Space reads exchange `getDelegationToken` through `authorizeSpaceSync`, with a P-256 key. `@atproto/space` signs the credential requests; `listWriters` discovers authors and `listRecords` reads each repo. The transport reauthorizes each list/write operation. It does not use administrator credentials. The authenticated user's DID determines the write repo. The explicit `authorDid` comes from the source repo, not the company authority component of a Space URI. All configured authors must be on this one PDS; multi-PDS resolution is outside this spike.

The feed has a company shared-password gate and signed HttpOnly cookie; its company PDS reader stays on the server. This is a local pilot login, not per-person browser OAuth. CLI writers use individual accounts. The PDS itself enforces repo ownership and company read credentials. The authority only advertises authorized writers; the protocol permits a person to retain their own records even after membership changes.

## Large records

The upstream write endpoint caps the full HTTP JSON body at 1,000,000 bytes. Transport keeps inline record JSON at or below 900,000 bytes. Larger records are serialized as UTF-8 JSON and split into 350,000-byte chunks, base64 encoded as records in `com.ensembleworks.session.chunk` in the **same private Space and same person's repo**. Rkeys are SHA-256 of the full serialized record followed by a six-digit chunk index. The event rkey holds a manifest with the original event `$type`, `transportType: com.ensembleworks.session.chunkManifest`, encoding, digest, byte count and chunk count. The manifest is written only after every chunk succeeds.

A retry writes the same chunk keys and event key. Readers reconstruct the original value and verify byte count and SHA-256; missing or corrupt chunks fail visibly. They never substitute truncated payloads. The returned `cid` belongs to the stored manifest for a chunked event; `value` is the reconstructed event. Chunks are invisible to ordinary event listings. Chunk lookup relies on the pinned PDS's descending URI cursor ordering and is covered by the live large-event check.

The watcher accepts native payloads up to 16 MiB; transport accepts the full serialized envelope up to 20 MiB. Larger entries remain visible retry failures. Interrupted or superseded chunk writes can leave unreferenced private chunks; this prototype has no garbage collector. A corrected event writes a new manifest last, so readers retain the prior complete version until replacement succeeds.

## Verification and restart

```sh
npm test
npm run typecheck
npm run test:transport:live
npm run test:transport:large
# Coordinate service outages with other running checks first:
docker compose restart postgres plc pds
# Wait for /xrpc/_health, then repeat readback / reviewer acceptance tests.
```

The live transport check verifies idempotent keys/CIDs, per-person attribution, pagination, member cross-person reads, outsider read/write refusal through transport, anonymous denial, empty public event repos, author impersonation denial, and maximum-size refusal. The large-event check writes and reads a 1,320,092-byte Unicode native payload through different members with exact equality and stable repeat CID. Unit chunk tests cover corrupt/missing chunks, stable serialization, and interruption after the first chunk: no manifest is published, and retries retain identical keys. Independent end-to-end and persistence evidence is recorded in `docs/prototype-review.md` by the reviewer.

`pds-data` and `plc-data` are named Docker volumes; accounts, signing keys, records, and PLC identities survive container replacement. `.local` retains passwords and PDS secrets. Keep both the volumes and `.local` for a restart. `docker compose down` preserves volumes; **do not use `down -v`** unless intentionally resetting synthetic data. Rebuild code with `DOCKER_CONFIG=/tmp/ensembleworks-docker docker compose build feed`, then `docker compose up -d --no-deps feed` to avoid interrupting PDS tests. Docker build configuration uses a writable `/tmp` path on this managed host.

## Known limits

This is the official experimental Spaces alpha, configured for local development with SSRF protection disabled so local identity and PDS calls work. Ports bind loopback; no public deployment is configured. Spaces provide access control, not end-to-end encryption. No production hardening, OAuth consent flow, schema migration compatibility, or chunk garbage collection is claimed.

`npm audit` reports seven high-severity dependency entries in the pinned legacy PLC/Lexicon dependency tree (including transitive `zod`/`kysely` and parents), with no automatic compatible fix reported. The upstream server package bundles some dependencies. This is a limitation of the pinned local spike, not a claim that these packages are ready for public exposure. See the lockfile and rerun `npm audit` for current advisories.
