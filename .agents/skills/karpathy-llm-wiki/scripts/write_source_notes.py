#!/usr/bin/env python3
"""Write a labelled source-notes raw for a source whose license does not
permit verbatim export.

Local extension to the upstream karpathy-llm-wiki skill (see UPSTREAM.md).
The full fetched text stays in the git-ignored cache
(build/reference-wiki/fulltext/<id>/NNN.md, written by fetch_source.py). This
script publishes only factual notes to docs/reference/raw/<topic>/, under
these mechanical guarantees:

- Header marks the file as notes, not an original: Representation, License,
  Work and Quotations lines are always present.
- Quotation budget: verbatim text is allowed only inside "double quotes" or
  “curly quotes”, each quote attributed in the notes. The total quoted
  characters across ALL raw files declaring the same `> Work:` key must not
  exceed 90 (checked under an exclusive lock so parallel writers cannot both
  spend the same budget). Blockquotes are rejected in notes bodies.
- Grounding: every quote, and every number/date literal the upstream
  checker would extract (check_evidence.extract_candidates), must be found in
  the cached original. Inline-code spans (identifiers, NSIDs, commands) must
  also appear verbatim there and be at most 6 words each, so code formatting
  cannot smuggle prose quotations past the budget.
- O_EXCL creation: an existing raw file is never overwritten.

Usage:
  write_source_notes.py --id ID --url URL --topic TOPIC --title TITLE
      --work WORK_KEY --license LICENSE --license-evidence TEXT
      --fulltext build/reference-wiki/fulltext/<id>/NNN.md --notes NOTES.md
      --author WORKER [--slug S] [--published YYYY-MM-DD] [--resolved-url U]
      [--check-only]
NOTES.md holds the body only (Markdown; headings from H2 down).
Exit 0 = written (or check passed); 2 = refused (reasons printed as JSON).
"""

from __future__ import annotations

import argparse
import fcntl
import importlib.util
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[3]
RAW_ROOT = REPO_ROOT / "docs/reference/raw"
FULLTEXT_ROOT = REPO_ROOT / "build/reference-wiki/fulltext"
LOCK = REPO_ROOT / "build/reference-wiki/quote-budget.lock"
BUDGET = 90

_spec = importlib.util.spec_from_file_location("check_evidence", HERE / "check_evidence.py")
check_evidence = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_evidence)

QUOTE_RES = [re.compile(r'"([^"\n]+)"'), re.compile(r"“([^”\n]+)”")]
CODE_RE = re.compile(r"`([^`\n]+)`")
WORK_RE = re.compile(r"^>\s*Work:\s*(.+?)\s*$", re.M)
QUOTED_RE = re.compile(r"^>\s*Quotations:\s*(\d+)\b", re.M)


def quotes_in(text: str) -> list[str]:
    text = CODE_RE.sub(" ", text)
    found = []
    for line in text.split("\n"):
        for rx in QUOTE_RES:
            found += [m.group(1) for m in rx.finditer(line)]
    return found


def quoted_chars(text: str) -> int:
    return sum(len(q) for q in quotes_in(text))


def spent_on_work(work: str) -> list[tuple[str, int]]:
    spent = []
    for path in RAW_ROOT.rglob("*.md"):
        head = path.read_text(encoding="utf-8")[:4000]
        m = WORK_RE.search(head)
        if m and m.group(1) == work:
            q = QUOTED_RE.search(head)
            spent.append((path.relative_to(REPO_ROOT).as_posix(), int(q.group(1)) if q else BUDGET))
    return spent


def slugify(text: str, limit: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(slug) > limit:
        slug = slug[:limit].rsplit("-", 1)[0] or slug[:limit]
    return slug or "source"


def main(argv):
    ap = argparse.ArgumentParser(description="Write a license-safe source-notes raw.")
    for name in ("--id", "--url", "--topic", "--title", "--work", "--license", "--license-evidence",
                 "--fulltext", "--notes", "--author"):
        ap.add_argument(name, required=True)
    ap.add_argument("--slug")
    ap.add_argument("--published")
    ap.add_argument("--resolved-url")
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args(argv)

    problems = []
    fulltext_path = (REPO_ROOT / args.fulltext).resolve()
    if not fulltext_path.is_relative_to(FULLTEXT_ROOT.resolve()) or not fulltext_path.is_file():
        problems.append(f"--fulltext must be an existing file under build/reference-wiki/fulltext/: {args.fulltext}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.topic):
        problems.append(f"invalid topic: {args.topic}")
    if args.published and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.published):
        problems.append("--published must be YYYY-MM-DD")
    notes = Path(args.notes).read_text(encoding="utf-8").strip() + "\n"
    if problems:
        print(json.dumps({"ok": False, "problems": problems}, indent=2))
        return 2

    original_doc = check_evidence.parse_document(fulltext_path.read_text(encoding="utf-8"))
    original = check_evidence.normalize("\n".join(original_doc.body))
    full_lines = fulltext_path.read_text(encoding="utf-8").split("\n")
    start = 1
    while start < len(full_lines) and (not full_lines[start].strip() or full_lines[start].startswith(">")):
        start += 1
    # Body including fenced code, excluding the cache file's own metadata header.
    original_with_code = check_evidence.normalize("\n".join(full_lines[start:]))

    if re.search(r"^\s*>", notes, re.M):
        problems.append("blockquotes are not allowed in notes; use attributed \"quotes\" within the budget")
    if re.search(r"^#\s", notes, re.M):
        problems.append("notes body must not contain an H1 (the script writes the title)")
    for q in quotes_in(notes):
        if check_evidence.normalize(q) not in original_with_code:
            problems.append(f"quote not found verbatim in fetched original: {q!r}")
    for span in CODE_RE.findall(notes):
        if len(span.split()) > 6:
            problems.append(f"inline code span too long to be an identifier (>6 words): {span!r}")
        elif check_evidence.normalize(span) not in original_with_code:
            problems.append(f"inline code span not found in fetched original: {span!r}")
    for cand in check_evidence.extract_candidates("# t\n\n" + notes):
        cand = check_evidence.Candidate(cand.kind, check_evidence.normalize(cand.value))
        if cand.kind == "quote":
            continue  # handled above with the stricter any-length rule
        # A date may be written as the date part of an ISO timestamp in the original.
        if cand.kind == "date" and re.search(r"(?<![\d.,])" + re.escape(cand.value) + r"T\d{2}:\d{2}",
                                             original_with_code):
            continue
        if not (check_evidence.contains(original, cand) or check_evidence.contains(original_with_code, cand)):
            problems.append(f"{cand.kind} not found in fetched original: {cand.value!r}")

    used = quoted_chars(notes)
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        prior = spent_on_work(args.work)
        total = used + sum(n for _, n in prior)
        if total > BUDGET:
            problems.append(f"quotation budget exceeded for work {args.work!r}: {used} new + "
                            f"{sum(n for _, n in prior)} already in {[p for p, _ in prior]} > {BUDGET}")
        if problems or args.check_only:
            print(json.dumps({"ok": not problems, "check_only": args.check_only, "quoted_chars": used,
                              "work_total": total, "problems": problems}, indent=2))
            return 2 if problems else 0

        cache_rel = fulltext_path.relative_to(REPO_ROOT).as_posix()
        header = [
            f"# {args.title} (source notes)", "",
            f"> Source: {args.url}",
        ]
        if args.resolved_url and args.resolved_url != args.url:
            header.append(f"> Resolved: {args.resolved_url}")
        header += [
            f"> Collected: {date.today().isoformat()}",
            f"> Published: {args.published or 'Unknown'}",
            f"> Representation: Source notes written by {args.author} from the fetched original. NOT a "
            f"verbatim copy: only text inside quotation marks is verbatim; everything else is paraphrase. "
            f"Numbers, dates, quotes and code identifiers were mechanically checked against the original.",
            f"> License: {args.license} — {args.license_evidence}. Verbatim export not permitted; full fetch "
            f"kept only in the git-ignored cache {cache_rel}.",
            f"> Work: {args.work}",
            f"> Quotations: {used} characters verbatim in this file; {total} of {BUDGET} allowed for this work "
            f"across the knowledge base.",
        ]
        content = "\n".join(header) + "\n\n" + notes
        directory = RAW_ROOT / args.topic
        directory.mkdir(parents=True, exist_ok=True)
        base = slugify(args.slug or args.title)
        base = f"{args.published}-{base}" if args.published else base
        for n in range(1, 100):
            path = directory / (f"{base}-notes.md" if n == 1 else f"{base}-notes-{n}.md")
            try:
                fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
            except FileExistsError:
                continue
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(content)
            print(json.dumps({"ok": True, "raw": path.relative_to(REPO_ROOT).as_posix(),
                              "quoted_chars": used, "work_total": total}, indent=2))
            return 0
    print(json.dumps({"ok": False, "problems": ["no free filename"]}))
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
