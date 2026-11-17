# Claude JSONL watcher spike

`@ensemble/cli` scans an explicitly supplied directory and publishes completed JSONL entries through `@ensemble/transport` to a real PDS company Space. There is no default Claude folder and no public-repository fallback. The reproducible demo uses synthetic files under `.local/demo-fixtures`; tests never read personal logs.

Requires Node 24, installed root npm workspaces, and Linux `flock` (util-linux). Infrastructure owns installation and PDS bootstrap. Set the account's Space membership before starting. The CLI accepts credentials through a mode-600 JSON file with `service`, `identifier`, `password`, `space`, optional `namespace` and `stateFile`. `PDS_SERVICE`, `PDS_IDENTIFIER`, `PDS_PASSWORD`, `PDS_SPACE` override those fields. Passwords never belong in command arguments.

After infrastructure setup and local pilot-account bootstrap, run these from the repository root:

```sh
npm run demo:seed
npm run demo:once
npm run demo:watch
```

In another terminal, run `npm run demo:append` to add a synthetic prompt and observe the feed refresh. `demo:seed` copies the checked-in fixture only if absent; reruns preserve existing appends. These commands use `.local/demo-fixtures`, `.local/demo-state.json`, and `.local/demo-writer.json`. The writer configuration contains Alice's local pilot credentials, is written mode 600, and must not be printed or committed. The watcher polls every two seconds. `demo:once` and `demo:watch` also prepare missing fixture/config files themselves. Linux `flock` from util-linux remains required on the watcher host.

To watch a separately selected folder using the generated local demo account:

```sh
npm run start -w @ensemble/cli -- once --dir /path/to/selected-folder --config .local/demo-writer.json --state .local/selected-folder-state.json
npm run start -w @ensemble/cli -- watch --dir /path/to/selected-folder --config .local/demo-writer.json --state .local/selected-folder-state.json --interval 2000
```

Use a separate checkpoint per selected directory, and run only one watcher against each checkpoint. The source folder must be explicitly selected; the demo commands never discover or default to a personal Claude store. For ongoing use choose a persistent state path. Without `--state`, checkpoints use `$XDG_STATE_HOME/ensemble-watcher` or `~/.local/state/ensemble-watcher`. The directory, namespace and destination account/Space bind each checkpoint; mismatches and corrupt checkpoints fail closed. `--namespace` defaults to a hash of the supplied absolute root; records carry only relative file paths. Choose an explicit stable namespace when moving a dataset. Original native payloads may themselves contain absolute paths or secrets and are deliberately not redacted.

`once` backfills everything currently complete, retries pending writes, prints counts, and exits nonzero on errors. `watch` repeats reconciliation, picks up new nested files, and backs off source-directory and publication failures from the configured interval to 30 seconds. Ctrl-C/SIGTERM finish an in-flight scan and release the checkpoint lock. Files and all complete lines are read on every scan; mtime/offsets are not correctness boundaries. This favors correctness for a small spike over scalability.

## Records and exports

`@ensemble/protocol` exports `EventRecord`, `EVENT_COLLECTION`, `MAX_PAYLOAD_BYTES`, `eventLexicon`, `chunkLexicon`, `manifestLexicon`, `companySpaceLexicon`, `createEvent`, `validateEvent`, `assertEvent`, `validateLexiconRecord`, and `digest`. Actual Lexicon JSON definitions live in `packages/protocol/lexicons/`. These are experimental names, not a claim of DNS-authorized public Lexicon publication. `validateEvent` checks Lexicon shape; `assertEvent` additionally checks payload size, JSON syntax and SHA-256. Transport's chunk codec separately checks ordered chunks, lengths, encoding and digest.

The local `com.ensembleworks.company` Space Lexicon lists both `com.ensembleworks.session.event` and `com.ensembleworks.session.chunk` in its `collections` array. The pinned alpha supports this Space declaration; record definitions have no separate Space-membership field. This source declaration documents the shared Space boundary. Bootstrap still configures membership, and transport still targets the same Space and author repository for event and chunk writes. No DNS publication or server enforcement of this local declaration is claimed.

The collection is `com.ensembleworks.session.event`. Each record includes:

- Versioned harness/source envelope: `schemaVersion`, `harness`, `sourceKind`, `harnessVersion` when a valid bounded native string exists.
- `streamId` derived from namespace and logical relative file identity, `sourcePath`, one-based `sourceLine`, zero-based `sourceOrder`.
- Optional recorded fields: `nativeId` from `uuid`, `nativeType` from `type`, `sessionId`, `parentId` from `parentUuid`, `occurredAt` from valid RFC3339 `timestamp`.
- `identityKind`, `capturedAt`, `payloadEncoding=json`, `payloadDigest`, and `payloadJson`.

`payloadJson` preserves the exact UTF-8 JSON line text, including whitespace, decimal spellings, large integers, nulls and unknown fields; the newline delimiter is excluded. CR in CRLF remains JSON whitespace in the payload. Parsing supports every JSON value, including arrays and primitives. There is no native event-type whitelist. Invalid optional metadata projections are omitted while the original payload remains intact. `capturedAt` remains stable while the payload and source metadata are unchanged; it is observation time, not a native event timestamp.

Native UUIDs determine deterministic record keys within each logical source stream. Content corrections overwrite the same record. Repeated UUIDs within a scan choose the last observed occurrence. No-UUID entries use exact payload digest plus same-content occurrence ordinal; reordering keeps identity but updates source position, while edits produce a new identity. This is an explicit ambiguity: logs without stable IDs cannot establish whether a changed entry is an edit or a new event. Metadata/title events still survive. Native parent IDs remain native references; no invented AT URI parent/anchor is asserted. Session grouping is by native sessionId, falling back to streamId. Record authorship comes from the repository DID; a native user role does not identify a human author.

Numbered rotation files `a.jsonl.1`, `a.jsonl.2`, etc. share logical stream identity with `a.jsonl`. Oldest numbered segments are scanned before the active file; active content wins for a repeated UUID. `sourcePath` and order retain the observed segment location. Arbitrary renames are new stream identities; copied files at different relative locations intentionally remain distinct. Nested subagent files have distinct stream identities even when UUID/sessionId values overlap. Source removal or compaction never deletes already published archive records. Exact duplicates without native IDs across separate rotation segments are inherently ambiguous and may collapse when their occurrence ordinal matches.

## Durability and gaps

Each mode-600 ledger contains record bodies, digest/signature, attempt count, last error and successful URI/CID. Pending records are fsynced before network writes; each acknowledgment is fsynced using atomic rename plus directory sync. A lost response retries the same rkey and same record bytes, including after the original file disappears. Published signatures suppress restart duplicates. Checkpoint loss causes idempotent rkey overwrites rather than minting new UUID keys; observation timestamps can change. The OS advisory lock prevents concurrent checkpoint writers. A small helper releases it when the watcher's stdin pipe closes, including SIGKILL; lockfile existence does not mean a live lock. Do not remove a live lockfile.

Incomplete final lines wait for a newline even in `once` mode. Malformed complete JSON/UTF-8 lines are reported by relative path and line, recorded as issues in the ledger, and rescanned until corrected. They cannot become native JSON records. Symlinks are not followed. Read failures are reported without exposing native payloads. A missing root or directory traversal failure produces a relative-path source issue. Pending ledger writes are still retried, and watch mode backs off and resumes scanning automatically when the directory returns. Checkpoint corruption, destination mismatches and checkpoint storage failures still stop the CLI.

Native payloads up to 16 MiB are accepted. The event collection Lexicon permits either native-envelope or manifest fields; runtime validation enforces the corresponding complete `#native` or `#chunkManifest` object shape. A manifest uses `$type=com.ensembleworks.session.event` with `transportType=com.ensembleworks.session.chunkManifest` because PDS record types must match their collection. Transport stores large full envelopes as ordered content-addressed chunks in the same Space and commits the manifest last; reads reconstruct and verify the original event for the feed. Full envelope JSON is limited to 20 MiB, so JSON escaping overhead can make a payload below 16 MiB exceed the transport cap. Such writes remain pending with a visible error. Payloads above 16 MiB remain in the source with a persisted validation issue, and are retried by full rescans; the ledger does not copy an invalid oversized source. No truncation occurs. Removed invalid sources cannot later be recovered from the ledger. Chunked publishing depends on the infrastructure implementation and its integration tests.

This spike preserves every valid completed entry available in the selected files. It cannot reconstruct events emitted only live by Claude, missing historical files, deleted logs, or attachments referenced by path. It preserves attachment references but does not copy external files. Synthetic fixtures test the structures observed in Claude 2.1.325 research; they are not a claim that a disposable live Claude run has exercised every native variant. Prompts, assistant/tool content, tool results, metadata/titles, compaction, branches/subagents, usage, progress and unknown types are preserved opaquely; semantic projections belong to the feed.

## Validation and live evidence

```sh
npm test -w @ensemble/protocol
npm test -w @ensemble/cli
npm run typecheck -w @ensemble/protocol
npm run typecheck -w @ensemble/cli
node --import tsx packages/cli/scripts/verify-live.ts .local/accounts.json
```

On 2026-11-17: 5 protocol tests and 10 watcher tests passed, plus both typechecks. Tests cover exact JSON, unknown/primitives, UUID corrections, deterministic fallback, nested logs, backfill/restart dedupe, partial UTF-8, malformed-line repair, rewrite/rotation, outage/ambiguous response/source removal, overflow, corrupt checkpoints, concurrent writers, live append, SIGKILL/restart, and source-directory disappearance/restoration with pending writes. The last command is an explicitly invoked real-PDS check using local pilot accounts, not part of ordinary test runs.

Actual CLI publication of the 10-entry synthetic corpus succeeded with `published:10, issues:[]`; a second CLI process returned `published:0, unchanged:10`. Bob's separate account read back 8 native records belonging to `synthetic-session` and verified the unknown record's large-integer and decimal text exactly. The other two fixture entries have no native sessionId and are displayed by stream. The original live check used a disposable temporary folder; reproduction uses the repository `demo:*` commands above and needs no historical `/tmp` path. Continuous demo watchers run at a 2-second interval. Feed browser acceptance and PDS persistence/restart evidence are owned by the feed/infrastructure/review threads.
