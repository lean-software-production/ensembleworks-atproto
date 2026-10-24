#!/usr/bin/env python3
"""Structural and license audit for the reference knowledge base.

Local extension to the upstream karpathy-llm-wiki skill (see UPSTREAM.md).
Report-only; never modifies files. Complements the upstream
check_evidence.py (fidelity) with:

- Index: every article listed once; every index row resolves; index Updated
  equals the article's Updated metadata.
- Links: every relative markdown link in wiki/ resolves (body, Raw, See Also).
- Inbound links: articles with no inbound link from another article.
- Raw coverage: every raw is linked from an article's Raw field or logged
  "no material" in wiki/log.md.
- Raw headers: every raw declares Source, Collected, Published,
  Representation and License; notes raws also Work and Quotations.
- Quotation budget: quoted characters per Work key (recomputed from notes
  bodies) must be <= 90 and match each file's declared count.
- Article quotations: no quoted span in an article may come only from
  notes-representation raws (their budget is spent in raw/).
- Ledger: every compiled source lists existing articles whose Raw field
  links its raw(s); every no_material source's raws are logged no material.

Usage: audit_kb.py [reference-root] [--ledger docs/research/sources.yaml]
"""

from __future__ import annotations

import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[3]
BUDGET = 90
_spec = importlib.util.spec_from_file_location("check_evidence", HERE / "check_evidence.py")
ce = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ce)
_spec = importlib.util.spec_from_file_location("write_source_notes", HERE / "write_source_notes.py")
notes_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(notes_mod)

LINK_RE = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADER_FIELD_RE = re.compile(r"^>\s*([A-Za-z][A-Za-z -]*):\s*(.*)$")


def header_fields(path: Path) -> dict:
    doc = ce.parse_document(path.read_text(encoding="utf-8"))
    fields = {}
    for line in doc.header:
        m = HEADER_FIELD_RE.match(line.strip())
        if m:
            fields[m.group(1)] = m.group(2)
    return fields


def main(argv):
    root = Path(argv[1]).resolve() if len(argv) > 1 and not argv[1].startswith("--") else REPO_ROOT / "docs/reference"
    ledger_path = REPO_ROOT / "docs/research/sources.yaml"
    if "--ledger" in argv:
        ledger_path = Path(argv[argv.index("--ledger") + 1])
    wiki, raw = root / "wiki", root / "raw"
    findings = defaultdict(list)
    articles = [p for p in sorted(wiki.rglob("*.md")) if p.name not in ("index.md", "log.md")]
    raws = sorted(raw.rglob("*.md"))

    # depth rule
    for a in articles:
        if len(a.relative_to(wiki).parts) != 2:
            findings["Structure"].append(f"{a.relative_to(root)}: articles must live at wiki/<topic>/<article>.md")

    # index
    index_text = (wiki / "index.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|(.*)\|\s*([^|]*?)\s*\|\s*$", index_text, re.M)
    listed = defaultdict(int)
    for _, target, _, updated in rows:
        path = (wiki / target).resolve()
        listed[path] += 1
        if not path.is_file():
            findings["Index"].append(f"index row points to missing file: {target}")
            continue
        art_updated = header_fields(path).get("Updated", "").strip()
        if art_updated and art_updated != updated.strip():
            findings["Index"].append(f"{target}: index Updated {updated.strip()} != article Updated {art_updated}")
    for a in articles:
        if listed[a.resolve()] == 0:
            findings["Index"].append(f"article missing from index: {a.relative_to(root)}")
        elif listed[a.resolve()] > 1:
            findings["Index"].append(f"article listed {listed[a.resolve()]} times: {a.relative_to(root)}")

    # links + inbound
    inbound = defaultdict(set)
    for f in articles + [wiki / "index.md"]:
        text = ce.strip_fences(f.read_text(encoding="utf-8"))
        text = ce.INLINE_CODE_RE.sub(" ", text)
        for _, target in LINK_RE.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            dest = (f.parent / target.split("#")[0]).resolve()
            if not dest.exists():
                findings["Links"].append(f"{f.relative_to(root)}: broken link {target}")
            elif f.name != "index.md" and dest != f.resolve():
                inbound[dest].add(f)
    for a in articles:
        if not inbound[a.resolve()]:
            findings["Orphans (no inbound article links)"].append(str(a.relative_to(root)))

    # raw headers + budget
    representation = {}
    per_work = defaultdict(list)
    for r in raws:
        fields = header_fields(r)
        rel = r.relative_to(root).as_posix()
        for key in ("Source", "Collected", "Published", "Representation", "License"):
            if key not in fields:
                findings["Raw headers"].append(f"{rel}: missing {key}")
        rep = fields.get("Representation", "")
        kind = "notes" if rep.startswith("Source notes") else "verbatim" if rep.startswith("Verbatim") else "unknown"
        representation[r.resolve()] = kind
        if kind == "unknown":
            findings["Raw headers"].append(f"{rel}: unrecognised Representation")
        if kind == "notes":
            if "Work" not in fields or "Quotations" not in fields:
                findings["Raw headers"].append(f"{rel}: notes raw missing Work/Quotations")
            body = "\n".join(ce.parse_document(r.read_text(encoding="utf-8")).body)
            used = notes_mod.quoted_chars(body)
            declared = re.match(r"(\d+)", fields.get("Quotations", ""))
            if declared and int(declared.group(1)) != used:
                findings["Quotation budget"].append(f"{rel}: declares {declared.group(1)} quoted chars, body has {used}")
            per_work[fields.get("Work", rel)].append((rel, used))
    for work, items in sorted(per_work.items()):
        total = sum(n for _, n in items)
        if total > BUDGET:
            findings["Quotation budget"].append(f"work {work!r}: {total} > {BUDGET} chars across {[p for p, _ in items]}")

    # article quotes vs notes raws
    article_quotes = defaultdict(int)
    for a in articles:
        text = a.read_text(encoding="utf-8")
        links = [(a.parent / l).resolve() for l in ce.raw_links_of(text)]
        bodies = {p: ce.source_content(p) for p in links if p.is_file()}
        doc = ce.parse_document(text)
        body = "\n".join(doc.body)
        quotes = notes_mod.quotes_in(ce.strip_fences(body))
        for line in doc.body:
            if line.strip().startswith(">") and not ce.STATUS_LINE_RE.match(line.strip()):
                pass
        for q in quotes:
            nq = ce.normalize(q)
            hits = [p for p, b in bodies.items() if nq in b]
            if hits and all(representation.get(p) == "notes" for p in hits):
                findings["Article quotations from notes-only works"].append(
                    f"{a.relative_to(root)}: \"{q}\" appears only in notes raws {[p.name for p in hits]}")
            if hits:
                article_quotes[a] += len(q)

    # coverage vs log
    referenced = ce.referenced_raws(root)
    no_material = ce.no_material_paths(wiki / "log.md")
    for r in raws:
        rel = r.relative_to(root).as_posix()
        if r.resolve() not in referenced and rel not in no_material:
            findings["Raw coverage"].append(f"{rel}: neither linked from an article Raw field nor logged no material")

    # ledger cross-check
    ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
    counts = defaultdict(int)
    for s in ledger["sources"]:
        ing = s.get("ingestion") or {}
        counts[ing.get("status", "uninitialised")] += 1
        raws_rel = [REPO_ROOT / p for p in ing.get("raw") or []]
        if ing.get("status") == "compiled":
            for art in ing.get("articles") or []:
                ap = REPO_ROOT / art
                if not ap.is_file():
                    findings["Ledger"].append(f"{s['id']}: article missing {art}")
                    continue
                linked = {(ap.parent / l).resolve() for l in ce.raw_links_of(ap.read_text(encoding="utf-8"))}
                if not any(r.resolve() in linked for r in raws_rel):
                    findings["Ledger"].append(f"{s['id']}: {art} does not link any of its raws")
        if ing.get("status") == "no_material":
            for r in raws_rel:
                if r.relative_to(root).as_posix() not in no_material:
                    findings["Ledger"].append(f"{s['id']}: no_material raw not logged: {r.relative_to(root)}")
        if ing.get("status") in ("claimed", "fetched", "pending"):
            findings["Ledger backlog"].append(f"{s['id']}: {ing.get('status')}")

    print("# Knowledge base audit\n")
    print(f"- Articles: {len(articles)}; raw files: {len(raws)} "
          f"({sum(1 for v in representation.values() if v == 'verbatim')} verbatim, "
          f"{sum(1 for v in representation.values() if v == 'notes')} notes)")
    print(f"- Ledger statuses: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    print(f"- Works with quotations in notes: {sum(1 for v in per_work.values() if sum(n for _, n in v))}; "
          f"max chars for one work: {max([sum(n for _, n in v) for v in per_work.values()] or [0])}")
    sections = ["Structure", "Index", "Links", "Raw headers", "Quotation budget",
                "Article quotations from notes-only works", "Raw coverage", "Ledger", "Ledger backlog",
                "Orphans (no inbound article links)"]
    total = 0
    for name in sections:
        items = findings.get(name, [])
        total += len(items) if name != "Orphans (no inbound article links)" else 0
        print(f"\n## {name}\n")
        print("\n".join(f"- {i}" for i in items) if items else "(none)")
    print(f"\n## Summary\n{total} structural/license finding(s); "
          f"{len(findings.get('Orphans (no inbound article links)', []))} orphan article(s) (judgment)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
