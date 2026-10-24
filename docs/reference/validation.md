# Completion validation

Codex completed the fetched-source backlog serially and reviewed the pre-handoff articles and compiled-source associations. The terminal inventory is **110 compiled, 4 No material, 3 blocked, 1 failed**, with **25 concept articles** and **114 unchanged raw packets**. The [source appendix](source-inventory.md) covers every ledger entry; blocked and failed sources remain unavailable and were not retried.

## Evidence review

The unchanged upstream [checker report](evidence-check.md) contains **6 fidelity suspects, 0 evidence errors and 0 unreferenced raw files**. Its process exit status was not used as an evidence verdict. Every remaining suspect was located in linked raw context:

| Article / suspect | Raw context and judgment |
|---|---|
| [Spaces](wiki/atproto/atproto-spaces-permissioned-data.md): `49379732` | [HN notes](raw/atproto/atproto-spaces-a-new-extension-to-atproto-that-enables-non-notes.md), Source and Work metadata: the HN item identifier. The checker omits raw metadata/URLs when testing body literals. Not an unsupported quantity. |
| [Blob limits](wiki/atproto/blobs-and-size-limits.md): `3392` | [Blobstore issue notes](raw/atproto/bluesky-social-atproto-3392-add-restrictions-on-blobstore-notes.md), title, Source and Work: issue identifier. The article's attribution is correct. |
| [Blob limits](wiki/atproto/blobs-and-size-limits.md): `1740` | [Blob-limit discussion notes](raw/atproto/consider-raising-the-size-limit-of-blobs-bluesky-social-notes.md), title, Source and Work: discussion identifier. Not a measured limit. |
| [Blob limits](wiki/atproto/blobs-and-size-limits.md): `4832` | [Image-limit discussion notes](raw/atproto/increasing-bluesky-post-image-size-limit-bluesky-social-notes.md), title, Source and Work: discussion identifier. Not a measured limit. |
| [bb status](wiki/bb/bb-project-status.md): `2026-02-24` | [Repository packet](raw/bb/get-bb-bb.md), Repository metadata: `Created: 2026-02-24T22:32:40Z`. The wiki retains the complete exact timestamp. The checker treats the date inside the timestamp as a standalone token. |
| [bb status](wiki/bb/bb-project-status.md): `2026-10-24` | Same packet: `Last pushed: 2026-10-24T05:55:31Z`. Same token-boundary false positive; not an invented date. |

The initial report also flagged editorial phrases in the Germ and Tangled articles that had been styled as direct quotations without source support. They were rewritten as editorial prose, and Germ's session-sharing extension was explicitly labeled a design inference. Facts were not changed to satisfy the regex. The checker itself and all raw files remain unchanged.

An additional literal scan included smaller integers and inspected candidate misses: trailing punctuation, plural HTTP response codes and audit Status dates explained its remaining candidates. The hosted guide's approximate create throughput is derived from the displayed point budget and per-create cost, and is also stated in the linked guide. No new numerical estimates were introduced during compilation. The audit is a grounding and consistency check against the exported source packets, not an independent experiment verifying external authors' claims.

## Repairs and judgment findings

- The pre-handoff index omitted thirteen existing articles. It now has exactly one entry for each actual article, with matching metadata dates. Four references to planned pages now point to compiled privacy or trace-format concepts. All relative wiki and Raw links resolve.
- The append-only log retains its checkpoint contents as an exact byte prefix. Audit backfills use the completion date and identify themselves as backfills; historical entries were not rewritten. Every source id is accounted for in the log or failure inventory, and No material headings use the skill's exact machine-readable syntax.
- Pi guide differences in tool defaults, package scope/counts and storage overrides are source-qualified. The upstream lifecycle and SDK examples clarify settle boundaries, resource cleanup and in-memory sessions. The branchWithSummary issue describes unsupported mutation through a cast rather than failure of supported navigation.
- The bb extension-UI issue's reported resolution is distinguished from its earlier limitation. The stale-extension-path diagnosis is unconfirmed. Built-in Pi, the separate durable provider, and bb-lite's multiplayer rewrite remain distinct products/snapshots. Handoff acceptance criteria and open PR titles are not presented as shipped guarantees.
- Reference-PDS defaults, vendor-reported hosted limits and the historic arbitrary-blob experiment are separate host/source snapshots. Spaces access control is not E2EE; Germ is application-layer encryption. Group standards remain divergent. These are explicit limitations rather than a falsely resolved single specification.
- ATIF, code attribution and telemetry serve different purposes. Reconstructed context, synthetic timing, omitted content, source order and inferred causal links are qualified. Agentimport is a merged importer change with reported synthetic tests, not merely a request or proof of corpus-wide losslessness. The vendor telemetry guide's content-placement and attribute-spelling differences are disputed against the registry snapshot.
- The research articles distinguish observations, contextual confounds and research proposals from causal or evaluated-system claims. The EDPB guidance is treated as a blockchain/replication analogy, not legal advice or a claim that ATProto is a blockchain.
- Completion cascade references connect the new concepts and existing applications. Every article has an inbound link from another article. No archives exist, so archive staleness does not apply. No unresolved malformed Status block, material unannotated contradiction or obviously missing concept page was identified; related cross-references can still be expanded as new evidence arrives.

## Independent preservation and structure checks

A separate validation script compares original id/URL/references values against the input ledger and hashes the reports, prompt, vision and all seven pinned upstream files against the audit baseline. It checks terminal states, repository-relative existing ledger paths, exact index/file coverage, link resolution, raw coverage, one-level layout, inbound links and log preservation. The ledger helper's own terminal verification also passes.

All raw hashes match both the start-of-Codex snapshot and all 114 raw files in the read-only on-camera checkpoint. No raw path or content was added, removed or overwritten. The raw headers identify 44 licensed verbatim packets and 70 notes packets; recorded quotation totals across 68 underlying notes-work keys stay within the per-work budget. New wiki prose synthesizes facts rather than adding full unlicensed source material or direct quotations from notes-only works. Required license notices in existing verbatim exports were preserved.

The durable machine-readable results are `build/reference-wiki/codex-validation.json` and `build/reference-wiki/codex-completion.json`. The validator and compiler batch records also remain under that ignored build directory for supervising review. No network retrieval, capture, Claude invocation, commit, merge or push was performed in this completion pass.

## Supervising integration review

A separate supervising check reproduced the terminal counts, exact index/date
coverage, resolving relative links, unchanged raw hashes, append-only log and
preserved input provenance and pinned skill files. It reproduced the same six
reviewed checker suspects, with no evidence-link errors or unreferenced raw files.
The original ledger baseline and dependency lock are now included beside these
documents so the documented verification commands work outside the ingestion
worktree. The status example and local helper docstring were corrected to omit
an unsupported `--json` flag; the helper already emits JSON by default, and its
runtime behavior was not changed. The claim-test suite now uses the published
baseline and selects a successful claimant without assuming process scheduling
order; all tests passed with sixteen simultaneous claimants and 118 distinct
claims. Build caches and bytecode are ignored.
