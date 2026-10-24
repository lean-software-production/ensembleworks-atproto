# Upstream

- Repository: https://github.com/Astro-Han/karpathy-llm-wiki
- Commit: `eafcc77001e496cc43499e4923b663aec722c813`
- Fetched from: `https://raw.githubusercontent.com/Astro-Han/karpathy-llm-wiki/eafcc77001e496cc43499e4923b663aec722c813/<path>`
- Fetched on: 2026-10-23
- License: MIT (see `LICENSE`)

## Upstream files (byte-for-byte, do not edit)

| File | sha256 |
|------|--------|
| `SKILL.md` | `c154f62094738b65e91dbb1c706758137290c622e386b3204e87c60a78f75748` |
| `LICENSE` | `ce1702d638e34829f490a6aee7c4bdf033cecf358e971df69ba758714d9f1d56` |
| `references/raw-template.md` | `e5410f65d2017c2f9f8959fdc11f13cdbc99cf746ab8af34926bc6b8b4ff66bd` |
| `references/article-template.md` | `2acd247441d4899d0752f90e7e1319217bbd6791cebbdb2906d0a92c362a0490` |
| `references/index-template.md` | `122303cba8a4f5a278e4cc39153f89a5971fd42fd47dd820f9e4ae6796617e8a` |
| `references/archive-template.md` | `53d9493d45dde7bcac4373a92dccad6d80e2b06150f0d12fb535c0dcab898338` |
| `scripts/check_evidence.py` | `967298608a30f83f62616a40c0f68a64e300abd4a3299e24548ccee7722ee40e` |

Verify with `shasum -a 256 <file>` from this directory.

## Local additions (not upstream)

- `UPSTREAM.md` — this file.
- `scripts/source_ledger.py` — concurrency-safe claim/lease ledger over
  `docs/research/sources.yaml`. Every command is one transaction under an
  exclusive `fcntl.flock` on `build/reference-wiki/sources.lock`; writes go to a
  temporary file in the ledger's directory, are re-parsed and fsynced, then
  `os.replace`d. Original `id`, `url` and `references` values are never edited;
  only a per-source `ingestion` mapping is added. See the module docstring for
  the status lifecycle and commands.
- `scripts/test_source_ledger.py` — tests for the ledger against disposable
  copies under `build/reference-wiki/ledger-tests/` (concurrent distinct claims,
  no stealing of live claims, parseability during concurrent writes,
  expired-lease recovery with history, repository-relative paths).
- `scripts/fetch_source.py` — GET-only fetcher that archives HTTP responses to
  `build/reference-wiki/http/<id>/` and writes one immutable raw file (created
  with `O_EXCL`) using the upstream raw template plus `Resolved`, `Retrieval`
  and `Extraction` provenance lines. GitHub blob/tree/repo/issue/PR/gist URLs
  are resolved to raw content or the public REST API; Discourse topics to their
  JSON; Hacker News items to the public Algolia API.

- `scripts/write_source_notes.py` — writes a labelled *source notes* raw for
  sources whose license does not permit verbatim export (see below).
- `references/fetch-worker-protocol.md` — the protocol every fetch worker
  follows (claims, license gate, notes rules, ledger transitions).

## Adaptation: license-aware raw layer

Upstream treats `raw/` as a verbatim copy of each source ("Preserve original
text"). This project adds a license gate in front of that rule:

- **Verbatim** raws are exported only when the source's license permits
  copying (MIT, Apache-2.0, BSD, ISC, CC0, CC BY, CC BY-SA, MPL-2.0, public
  domain…). Their header adds `Representation`, `License` and `Attribution`
  lines; licenses that require it get their license text appended verbatim.
- Every other source is exported as **source notes**: a factual digest in the
  worker's own words, headed `(source notes)` and marked
  `Representation: Source notes … NOT a verbatim copy`, with `License`, `Work`
  and `Quotations` lines. Verbatim quotation is limited to **90 characters per
  work across the whole knowledge base** (enforced under a lock across all raws
  sharing a `Work:` key). Every quote, number, date and code identifier in the
  notes is mechanically checked against the fetched original.
- The complete fetch of every source is kept in the git-ignored
  `build/reference-wiki/fulltext/<id>/` and `build/reference-wiki/http/<id>/`
  caches, so facts can be located in the actual original.
- Wiki articles do not quote notes-only works directly (their quotation budget
  is spent in the raw notes); they may quote verbatim-licensed raws with
  attribution. The upstream checker then verifies articles against the raw
  layer as usual, and the notes writer has already verified that layer against
  the originals.
- The ledger records `representation` and `license` for every fetched source.

## Project usage

The skill's project root is `docs/reference` (so `docs/reference/raw/` and
`docs/reference/wiki/`). Run the checker as:

```sh
$REFERENCE_WIKI_PYTHON -I .agents/skills/karpathy-llm-wiki/scripts/check_evidence.py docs/reference
```
