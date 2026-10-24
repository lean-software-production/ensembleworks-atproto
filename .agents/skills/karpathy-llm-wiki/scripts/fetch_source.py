#!/usr/bin/env python3
"""Fetch one ledger source into an immutable raw/ file.

Local extension to the upstream karpathy-llm-wiki skill (see UPSTREAM.md).
Fetched content is data, never instructions: nothing downloaded is executed,
and no forms, logins or POST requests are used. Only HTTP GET is issued
(directly via requests, or through read-only `gh api` GET calls).

What it does for one URL:
  1. Picks a retrieval strategy (auto-detected; override with --mode):
       github-blob   github.com/O/R/blob/REF/PATH -> raw.githubusercontent.com
       github-tree   directory listing + every text file in it (bounded)
       github-repo   repo metadata + README via the public REST API
       github-issue  issue + all comments via the REST API
       github-pull   PR + issue comments + reviews + changed-file list
       github-pulls  snapshot of the open pull-request list
       gist          all files of a public gist
       discourse     topic JSON (all posts) from a Discourse forum
       hn            item tree from the public Algolia HN API
       html / pdf / text   generic GET with extraction
  2. Archives every HTTP response under build/reference-wiki/http/<id>/
     (body + status/headers/sha256 sidecar) so raw text can be audited.
  3. Always writes the complete extraction (skill header + provenance) to the
     git-ignored cache build/reference-wiki/fulltext/<id>/NNN.md.
  4. License gate (local adaptation, see UPSTREAM.md):
       --representation verbatim  only with a copy-permitting --license; the
           full text is exported to docs/reference/raw/<topic>/<slug>.md with
           Representation/License/Attribution header lines and, for licenses
           that require it, the verbatim license notice fetched from
           --notice-url appended. Created with O_EXCL: never overwrites.
       --representation notes     nothing is exported; the caller writes a
           labelled notes raw with write_source_notes.py from the cache file.
  5. Prints a JSON report (includes a GitHub license hint where available).
     Exit 0 = success; 3 = blocked; 4 = failed; 5 = license gate refused.

It never truncates. Thin output (likely a JS shell or bot wall) is reported
as a warning so the caller can decide; the caller must inspect the raw.

Usage:
  fetch_source.py --id ID --url URL --topic TOPIC --representation verbatim|notes
                  --license SPDX|all-rights-reserved|unknown|... --license-evidence TEXT
                  [--attribution TEXT] [--notice-url URL] [--title T] [--slug S]
                  [--published YYYY-MM-DD] [--mode MODE] [--fetch-url U] [--dry-run]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import date
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

REPO_ROOT = Path(__file__).resolve().parents[4]
RAW_ROOT = REPO_ROOT / "docs/reference/raw"
HTTP_ROOT = REPO_ROOT / "build/reference-wiki/http"
FULLTEXT_ROOT = REPO_ROOT / "build/reference-wiki/fulltext"
# Licenses that permit verbatim redistribution (with attribution/notices).
COPY_PERMITTED = {"CC-BY", "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "0BSD", "Unlicense",
                  "CC0-1.0", "CC-BY-4.0", "CC-BY-3.0", "CC-BY-SA-4.0", "CC-BY-SA-3.0", "MPL-2.0",
                  "public-domain"}
# Licenses whose terms require the license text/notice to travel with copies.
NOTICE_REQUIRED = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0"}
USER_AGENT = "ensembleworks-reference-wiki/0.1 (archival fetch of cited research sources; python-requests)"
TIMEOUT = (10, 40)
MAX_ATTEMPTS = 3
MAX_RETRY_AFTER = 90
TREE_FILE_CAP = 40
TEXT_EXTS = {".md", ".markdown", ".txt", ".json", ".yaml", ".yml", ".ts", ".tsx", ".js", ".mjs",
             ".rs", ".go", ".py", ".toml", ".lexicon"}
FENCE_LANG = {".ts": "ts", ".tsx": "tsx", ".js": "js", ".mjs": "js", ".rs": "rust", ".go": "go",
              ".py": "python", ".json": "json", ".yaml": "yaml", ".yml": "yaml", ".toml": "toml"}
CHALLENGE_MARKERS = ("Just a moment...", "cf-browser-verification", "challenge-platform",
                     "Attention Required! | Cloudflare", "Enable JavaScript and cookies to continue")


class FetchError(Exception):
    def __init__(self, classification: str, reason: str, http_status: int | None = None,
                 resolved_url: str | None = None):
        super().__init__(reason)
        self.classification = classification
        self.reason = reason
        self.http_status = http_status
        self.resolved_url = resolved_url


class Archive:
    def __init__(self, source_id: str):
        self.dir = HTTP_ROOT / source_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.count = len(list(self.dir.glob("*.meta.json")))
        self.entries: list[dict] = []

    def save(self, url: str, status: int | None, headers: dict, body: bytes, ext: str) -> str:
        self.count += 1
        stem = f"{self.count:03d}"
        body_path = self.dir / f"{stem}{ext}"
        body_path.write_bytes(body)
        meta = {"url": url, "status": status, "headers": headers, "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(), "body": body_path.name}
        (self.dir / f"{stem}.meta.json").write_text(json.dumps(meta, indent=2))
        rel = body_path.relative_to(REPO_ROOT).as_posix()
        self.entries.append({"url": url, "status": status, "sha256": meta["sha256"], "path": rel})
        return rel


# ---------------------------------------------------------------- transport


SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en"})


def http_get(url: str, archive: Archive, accept: str | None = None, ext: str = ".bin",
             allow_404: bool = False) -> requests.Response:
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            headers = {"Accept": accept} if accept else {}
            resp = SESSION.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=True)
        except requests.RequestException as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            time.sleep(2 * attempt)
            continue
        archive.save(resp.url, resp.status_code, dict(resp.headers), resp.content,
                     guess_ext(resp, ext))
        if resp.status_code in (429, 502, 503, 504) and attempt < MAX_ATTEMPTS:
            wait = retry_after(resp, attempt)
            if wait is None:
                raise FetchError("blocked", f"rate limited (HTTP {resp.status_code}); Retry-After exceeds "
                                 f"{MAX_RETRY_AFTER}s", resp.status_code, resp.url)
            time.sleep(wait)
            continue
        if resp.status_code == 404 and allow_404:
            return resp
        if resp.status_code in (401, 403, 451):
            raise FetchError("blocked", f"HTTP {resp.status_code} access denied", resp.status_code, resp.url)
        if resp.status_code == 429:
            raise FetchError("blocked", "rate limited (HTTP 429) after retries", 429, resp.url)
        if resp.status_code == 404 or resp.status_code == 410:
            raise FetchError("failed", f"HTTP {resp.status_code} not found", resp.status_code, resp.url)
        if resp.status_code >= 400:
            raise FetchError("failed", f"HTTP {resp.status_code}", resp.status_code, resp.url)
        text_head = resp.content[:20000].decode("utf-8", "replace")
        if any(marker in text_head for marker in CHALLENGE_MARKERS):
            raise FetchError("blocked", "bot/JavaScript challenge page instead of content",
                             resp.status_code, resp.url)
        return resp
    raise FetchError("failed", f"network error after {MAX_ATTEMPTS} attempts: {last_error}")


def retry_after(resp: requests.Response, attempt: int) -> float | None:
    value = resp.headers.get("Retry-After")
    if value and value.isdigit():
        wait = int(value)
        return wait if wait <= MAX_RETRY_AFTER else None
    return 5 * attempt


def guess_ext(resp: requests.Response, default: str) -> str:
    ctype = resp.headers.get("Content-Type", "")
    for needle, ext in (("html", ".html"), ("json", ".json"), ("pdf", ".pdf"), ("text/plain", ".txt"),
                        ("markdown", ".md")):
        if needle in ctype:
            return ext
    return default


def gh_get(path: str, archive: Archive, accept: str | None = None, paginate: bool = False):
    cmd = ["gh", "api", "--method", "GET", path]
    if accept:
        cmd += ["-H", f"Accept: {accept}"]
    if paginate:
        cmd += ["--paginate", "--slurp"]
    for attempt in range(1, MAX_ATTEMPTS + 1):
        proc = subprocess.run(cmd, capture_output=True, timeout=120)
        url = f"https://api.github.com/{path.lstrip('/')}"
        archive.save(url, 200 if proc.returncode == 0 else None, {"gh-cmd": " ".join(cmd)},
                     proc.stdout if proc.returncode == 0 else proc.stderr,
                     ".json" if not accept or "json" in accept else ".txt")
        if proc.returncode == 0:
            if accept and "raw" in accept:
                return proc.stdout.decode("utf-8", "replace")
            data = json.loads(proc.stdout or b"null")
            if paginate:
                return [item for page in data for item in (page if isinstance(page, list) else [page])]
            return data
        err = proc.stderr.decode("utf-8", "replace")
        status = int(m.group(1)) if (m := re.search(r"HTTP (\d{3})", err)) else None
        if status in (403, 429) and "rate limit" in err.lower() and attempt < MAX_ATTEMPTS:
            time.sleep(30 * attempt)
            continue
        if status == 404:
            raise FetchError("failed", f"GitHub API 404 for {path}", 404, url)
        if status in (401, 403, 451):
            raise FetchError("blocked", f"GitHub API {status} for {path}: {err.strip()[:200]}", status, url)
        raise FetchError("failed", f"gh api error for {path}: {err.strip()[:200]}", status, url)
    raise FetchError("blocked", f"GitHub API rate limited for {path}", 429)


# ---------------------------------------------------------------- extraction


DROP_TAGS = ("script", "style", "noscript", "svg", "nav", "footer", "form", "iframe", "button",
             "template", "dialog")


def html_to_markdown(html: str, base_selector: str | None = None) -> tuple[str, str | None, dict]:
    soup = BeautifulSoup(html, "html.parser")
    title = None
    meta = {}
    og = soup.find("meta", attrs={"property": "og:title"})
    if og and og.get("content"):
        title = og["content"].strip()
    elif soup.title and soup.title.string:
        title = soup.title.string.strip()
    for key in ("article:published_time", "og:published_time", "datePublished", "citation_date",
                "citation_publication_date", "dc.date"):
        tag = soup.find("meta", attrs={"property": key}) or soup.find("meta", attrs={"name": key})
        if tag and tag.get("content"):
            meta.setdefault("published_meta", f"{key}={tag['content'].strip()}")
    for tag in soup(DROP_TAGS):
        tag.decompose()
    for tag in soup.find_all(attrs={"aria-hidden": "true"}):
        if tag.name not in ("main", "article", "body"):
            tag.decompose()
    root = None
    if base_selector:
        root = soup.select_one(base_selector)
    if root is None:
        candidates = soup.find_all("article") or soup.find_all("main") or soup.find_all(attrs={"role": "main"})
        if candidates:
            root = max(candidates, key=lambda t: len(t.get_text(" ", strip=True)))
    if root is None:
        root = soup.body or soup
        for tag in root.find_all(["header", "aside"]):
            tag.decompose()
    md = markdownify(str(root), heading_style="ATX", bullets="-", strip=["img"])
    return clean_markdown(md), title, meta


def clean_markdown(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    out = []
    blank = 0
    for line in lines:
        if not line.strip():
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        out.append(line)
    return "\n".join(out).strip() + "\n"


def pdf_to_text(data: bytes) -> tuple[str, str | None]:
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(data))
    pages = []
    for number, page in enumerate(reader.pages, 1):
        pages.append(f"## Page {number}\n\n{(page.extract_text() or '').strip()}\n")
    title = (reader.metadata or {}).get("/Title") if reader.metadata else None
    return clean_markdown("\n".join(pages)), title


def fence(text: str, lang: str = "") -> str:
    ticks = "```"
    while ticks in text:
        ticks += "`"
    return f"{ticks}{lang}\n{text.rstrip()}\n{ticks}\n"


def demote_headings(markdown: str, levels: int = 2) -> str:
    """Shift user-content headings below the raw file's own H1/H2 structure."""
    out = []
    in_fence = False
    for line in markdown.split("\n"):
        if re.match(r"^ {0,3}(```|~~~)", line):
            in_fence = not in_fence
        if not in_fence and re.match(r"^#{1,6} ", line):
            hashes = len(line) - len(line.lstrip("#"))
            line = "#" * min(6, hashes + levels) + line[hashes:]
        out.append(line)
    return "\n".join(out)


# ---------------------------------------------------------------- strategies


def detect_mode(url: str) -> str:
    p = urlparse(url)
    host = p.netloc.lower()
    parts = [x for x in p.path.split("/") if x]
    if host == "github.com":
        if len(parts) >= 4 and parts[2] == "blob":
            return "github-blob"
        if len(parts) >= 4 and parts[2] == "tree":
            return "github-tree"
        if len(parts) == 4 and parts[2] == "issues":
            return "github-issue"
        if len(parts) == 4 and parts[2] == "pull":
            return "github-pull"
        if len(parts) == 3 and parts[2] == "pulls":
            return "github-pulls"
        if len(parts) == 2:
            return "github-repo"
        return "html"
    if host == "gist.github.com":
        return "gist"
    if host.startswith("discourse.") and "/t/" in p.path:
        return "discourse"
    if host == "news.ycombinator.com":
        return "hn"
    if p.path.lower().endswith(".pdf"):
        return "pdf"
    return "html"


def repo_parts(url: str) -> list[str]:
    return [x for x in urlparse(url).path.split("/") if x]


def license_hint(owner: str, repo: str, archive: Archive) -> dict:
    try:
        lic = gh_get(f"repos/{owner}/{repo}/license", archive)
    except FetchError as exc:
        return {"repo": f"{owner}/{repo}", "spdx": None, "note": exc.reason}
    return {"repo": f"{owner}/{repo}", "spdx": (lic.get("license") or {}).get("spdx_id"),
            "path": lic.get("path"), "html_url": lic.get("html_url"), "download_url": lic.get("download_url")}


def commit_for(owner: str, repo: str, ref: str, path: str, archive: Archive) -> str | None:
    try:
        commits = gh_get(f"repos/{owner}/{repo}/commits?sha={ref}&path={path}&per_page=1", archive)
        return commits[0]["sha"] if commits else None
    except FetchError:
        return None


def strat_github_blob(url, archive):
    owner, repo, _, ref, *path = repo_parts(url)
    path_s = "/".join(path)
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path_s}"
    resp = http_get(raw_url, archive, ext=Path(path_s).suffix or ".txt")
    sha = commit_for(owner, repo, ref, path_s, archive)
    text = resp.content.decode("utf-8", "replace")
    ext = Path(path_s).suffix.lower()
    body = text if ext in (".md", ".markdown") else fence(text, FENCE_LANG.get(ext, ""))
    note = f"raw file at ref `{ref}`" + (f"; latest commit touching path: {sha}" if sha else "")
    return {"title": f"{owner}/{repo}: {path_s}", "body": body, "resolved": [raw_url],
            "status": resp.status_code, "extraction": f"Verbatim file content ({note})."}


def strat_github_tree(url, archive):
    owner, repo, _, ref, *path = repo_parts(url)
    path_s = "/".join(path)
    listing = gh_get(f"repos/{owner}/{repo}/contents/{path_s}?ref={ref}", archive)
    files = [e for e in listing if e["type"] == "file"]
    lines = [f"Directory listing of `{path_s}` at ref `{ref}`:", ""]
    lines += [f"- `{e['name']}` ({e['type']}, {e.get('size', 0)} bytes)" for e in listing]
    sections = ["\n".join(lines)]
    resolved = [f"https://api.github.com/repos/{owner}/{repo}/contents/{path_s}?ref={ref}"]
    text_files = [e for e in files if Path(e["name"]).suffix.lower() in TEXT_EXTS]
    if len(text_files) > TREE_FILE_CAP:
        raise FetchError("failed", f"directory has {len(text_files)} text files (> cap {TREE_FILE_CAP}); "
                         "refusing partial capture")
    for entry in text_files:
        raw_url = entry["download_url"]
        resp = http_get(raw_url, archive, ext=Path(entry["name"]).suffix)
        text = resp.content.decode("utf-8", "replace")
        ext = Path(entry["name"]).suffix.lower()
        content = demote_headings(text) if ext in (".md", ".markdown") else fence(text, FENCE_LANG.get(ext, ""))
        sections.append(f"## File: {entry['path']}\n\n{content}")
        resolved.append(raw_url)
    sha = commit_for(owner, repo, ref, path_s, archive)
    return {"title": f"{owner}/{repo}: {path_s}/", "body": "\n\n".join(sections), "resolved": resolved,
            "status": 200, "extraction": f"Directory listing plus every text file in it, verbatim "
            f"(ref `{ref}`" + (f"; latest commit touching path: {sha})." if sha else ").")}


def strat_github_repo(url, archive):
    owner, repo = repo_parts(url)[:2]
    meta = gh_get(f"repos/{owner}/{repo}", archive)
    lines = [
        "## Repository metadata (GitHub REST API)", "",
        f"- Full name: {meta.get('full_name')}",
        f"- Description: {meta.get('description')}",
        f"- Homepage: {meta.get('homepage') or 'none'}",
        f"- Default branch: {meta.get('default_branch')}",
        f"- License: {(meta.get('license') or {}).get('spdx_id') or 'none detected'}",
        f"- Primary language: {meta.get('language')}",
        f"- Topics: {', '.join(meta.get('topics') or []) or 'none'}",
        f"- Created: {meta.get('created_at')}",
        f"- Last pushed: {meta.get('pushed_at')}",
        f"- Stars at collection: {meta.get('stargazers_count')}",
        f"- Forks at collection: {meta.get('forks_count')}",
        f"- Open issues at collection: {meta.get('open_issues_count')}",
        f"- Archived: {meta.get('archived')}",
        f"- Fork: {meta.get('fork')}" + (f" of {meta['parent']['full_name']}" if meta.get("parent") else ""),
    ]
    resolved = [meta.get("url")]
    try:
        readme = gh_get(f"repos/{owner}/{repo}/readme", archive, accept="application/vnd.github.raw")
        lines += ["", "## README", "", demote_headings(readme)]
        resolved.append(f"https://api.github.com/repos/{owner}/{repo}/readme")
    except FetchError as exc:
        lines += ["", f"## README", "", f"(No README retrievable: {exc.reason})"]
    try:
        tree = gh_get(f"repos/{owner}/{repo}/contents/", archive)
        lines += ["", "## Top-level files", ""] + [f"- `{e['name']}` ({e['type']})" for e in tree]
    except FetchError:
        pass
    return {"title": f"{owner}/{repo}", "body": "\n".join(lines), "resolved": resolved, "status": 200,
            "extraction": "Repository metadata, README (verbatim) and top-level listing via read-only GitHub REST API."}


def render_comment(c: dict, label: str) -> str:
    user = (c.get("user") or {}).get("login", "unknown")
    stamp = c.get("submitted_at") or c.get("created_at")
    extra = f" [{c['state']}]" if c.get("state") and label == "Review" else ""
    body = (c.get("body") or "").strip() or "(no text)"
    return f"### {label} by @{user} at {stamp}{extra}\n\n{demote_headings(body, 3)}\n"


def strat_github_issue(url, archive, pull=False):
    owner, repo, _, number = repo_parts(url)[:4]
    issue = gh_get(f"repos/{owner}/{repo}/issues/{number}", archive)
    comments = gh_get(f"repos/{owner}/{repo}/issues/{number}/comments?per_page=100", archive, paginate=True)
    kind = "Pull request" if pull or issue.get("pull_request") else "Issue"
    head = [
        "## Metadata (GitHub REST API)", "",
        f"- {kind}: {owner}/{repo}#{number}",
        f"- Title: {issue.get('title')}",
        f"- Author: @{(issue.get('user') or {}).get('login')}",
        f"- State: {issue.get('state')}" + (f" ({issue.get('state_reason')})" if issue.get("state_reason") else ""),
        f"- Created: {issue.get('created_at')}",
        f"- Updated: {issue.get('updated_at')}",
        f"- Closed: {issue.get('closed_at')}",
        f"- Labels: {', '.join(l['name'] for l in issue.get('labels') or []) or 'none'}",
        f"- Comments: {len(comments)}",
    ]
    resolved = [issue.get("url")]
    sections = []
    if pull or issue.get("pull_request"):
        pr = gh_get(f"repos/{owner}/{repo}/pulls/{number}", archive)
        head += [f"- Merged: {pr.get('merged')} at {pr.get('merged_at')}",
                 f"- Base/head: {pr['base']['ref']} <- {pr['head']['label']}",
                 f"- Changed files: {pr.get('changed_files')}, +{pr.get('additions')}/-{pr.get('deletions')}"]
        files = gh_get(f"repos/{owner}/{repo}/pulls/{number}/files?per_page=100", archive, paginate=True)
        reviews = gh_get(f"repos/{owner}/{repo}/pulls/{number}/reviews?per_page=100", archive, paginate=True)
        sections.append("## Changed files\n\n" + "\n".join(
            f"- `{f['filename']}` ({f['status']}, +{f['additions']}/-{f['deletions']})" for f in files))
        if reviews:
            sections.append("## Reviews\n\n" + "\n".join(render_comment(r, "Review") for r in reviews))
        resolved.append(pr.get("url"))
    body = (issue.get("body") or "").strip() or "(no description)"
    parts = ["\n".join(head), f"## Description\n\n{demote_headings(body)}"] + sections
    if comments:
        parts.append("## Comments\n\n" + "\n".join(render_comment(c, "Comment") for c in comments))
    return {"title": f"{owner}/{repo}#{number}: {issue.get('title')}", "body": "\n\n".join(parts),
            "resolved": resolved, "status": 200,
            "extraction": f"{kind} body, metadata and all comments verbatim via read-only GitHub REST API.",
            "published": (issue.get("created_at") or "")[:10] or None,
            "published_evidence": "GitHub API created_at"}


def strat_github_pulls(url, archive):
    owner, repo = repo_parts(url)[:2]
    pulls = gh_get(f"repos/{owner}/{repo}/pulls?state=open&per_page=100", archive)
    lines = [f"Snapshot of the first page (up to 100) of open pull requests for {owner}/{repo} "
             f"at collection time; {len(pulls)} returned.", ""]
    lines += [f"- #{p['number']} {p['title']} (@{p['user']['login']}, created {p['created_at']}"
              f"{', draft' if p.get('draft') else ''})" for p in pulls]
    return {"title": f"{owner}/{repo}: open pull requests", "body": "\n".join(lines),
            "resolved": [f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open&per_page=100"],
            "status": 200, "extraction": "Open-PR list snapshot via read-only GitHub REST API (titles only; "
            "the original page is a moving listing)."}


def strat_gist(url, archive):
    gist_id = repo_parts(url)[-1]
    gist = gh_get(f"gists/{gist_id}", archive)
    parts = [f"- Owner: @{(gist.get('owner') or {}).get('login')}",
             f"- Description: {gist.get('description')}",
             f"- Created: {gist.get('created_at')}", f"- Updated: {gist.get('updated_at')}"]
    for name, f in (gist.get("files") or {}).items():
        content = f.get("content") or ""
        if f.get("truncated"):
            resp = http_get(f["raw_url"], archive, ext=Path(name).suffix or ".txt")
            content = resp.content.decode("utf-8", "replace")
        ext = Path(name).suffix.lower()
        rendered = demote_headings(content) if ext in (".md", ".markdown") else fence(content, FENCE_LANG.get(ext, ""))
        parts.append(f"\n## File: {name}\n\n{rendered}")
    return {"title": gist.get("description") or f"gist {gist_id}", "body": "\n".join(parts),
            "resolved": [gist.get("url")], "status": 200,
            "extraction": "All gist files verbatim via read-only GitHub REST API.",
            "published": (gist.get("created_at") or "")[:10] or None, "published_evidence": "gist created_at"}


def strat_discourse(url, archive):
    p = urlparse(url)
    m = re.search(r"/t/([^/]+)/(\d+)", p.path)
    if not m:
        raise FetchError("failed", "unrecognised Discourse topic URL")
    base = f"{p.scheme}://{p.netloc}"
    topic_url = f"{base}/t/{m.group(1)}/{m.group(2)}.json"
    topic = http_get(topic_url, archive, accept="application/json", ext=".json").json()
    posts = list(topic["post_stream"]["posts"])
    have = {post["id"] for post in posts}
    missing = [pid for pid in topic["post_stream"].get("stream", []) if pid not in have]
    resolved = [topic_url]
    for i in range(0, len(missing), 20):
        chunk = missing[i:i + 20]
        q = "&".join(f"post_ids[]={pid}" for pid in chunk)
        more_url = f"{base}/t/{m.group(2)}/posts.json?{q}"
        more = http_get(more_url, archive, accept="application/json", ext=".json").json()
        posts += more["post_stream"]["posts"]
        resolved.append(more_url)
        time.sleep(1)
    posts.sort(key=lambda post: post["post_number"])
    expected = topic.get("posts_count")
    if expected and len(posts) < expected:
        warn = f"retrieved {len(posts)} of posts_count {expected} (deleted/hidden posts are not public)"
    else:
        warn = None
    out = [f"- Forum: {p.netloc}", f"- Topic id: {topic['id']}", f"- Created: {topic.get('created_at')}",
           f"- Posts retrieved: {len(posts)}" + (f" (posts_count {expected})" if expected else "")]
    for post in posts:
        md, _, _ = html_to_markdown(f"<article>{post.get('cooked', '')}</article>")
        out.append(f"\n## Post {post['post_number']} by @{post.get('username')} at {post.get('created_at')}\n\n"
                   f"{demote_headings(md, 2)}")
    result = {"title": topic.get("title") or topic.get("fancy_title"), "body": "\n".join(out),
              "resolved": resolved, "status": 200,
              "extraction": "All public posts from Discourse topic JSON; post HTML converted with markdownify.",
              "published": (topic.get("created_at") or "")[:10] or None,
              "published_evidence": "Discourse topic created_at"}
    if warn:
        result["warnings"] = [warn]
    return result


def strat_hn(url, archive):
    item_id = re.search(r"id=(\d+)", url).group(1)
    api = f"https://hn.algolia.com/api/v1/items/{item_id}"
    resp = http_get(api, archive, accept="application/json", ext=".json", allow_404=True)
    if resp.status_code == 404:
        fb = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        resp2 = http_get(fb, archive, accept="application/json", ext=".json")
        if resp2.text.strip() in ("null", ""):
            raise FetchError("failed", f"HN item {item_id} does not exist (Algolia 404; Firebase null)",
                             404, api)
        raise FetchError("failed", f"HN item {item_id} not in Algolia index; Firebase returned data but "
                         "tree retrieval not supported", 404, api)
    item = resp.json()
    out = []

    def walk(node, depth):
        text = node.get("text") or ""
        md = clean_markdown(markdownify(text)) if text else ""
        author = node.get("author") or "[deleted]"
        if depth == 0:
            out.append(f"- Title: {node.get('title')}\n- URL: {node.get('url')}\n- By: {author}\n"
                       f"- Created: {node.get('created_at')}\n- Points: {node.get('points')}\n")
            if md:
                out.append(md)
        else:
            indent = "  " * (depth - 1)
            body = md.strip().replace("\n", f"\n{indent}  ") or "(deleted)"
            out.append(f"{indent}- **{author}** ({node.get('created_at')}): {body}")
        for child in node.get("children") or []:
            walk(child, depth + 1)

    walk(item, 0)
    return {"title": item.get("title") or f"HN item {item_id}", "body": "\n".join(out), "resolved": [api],
            "status": 200, "extraction": "Full item tree from the public Algolia HN API; comment HTML converted "
            "with markdownify.", "published": (item.get("created_at") or "")[:10] or None,
            "published_evidence": "HN created_at"}


def strat_html(url, archive, selector=None):
    resp = http_get(url, archive, accept="text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
                    ext=".html")
    ctype = resp.headers.get("Content-Type", "")
    if "pdf" in ctype or resp.content[:5] == b"%PDF-":
        text, title = pdf_to_text(resp.content)
        return {"title": title, "body": text, "resolved": [resp.url], "status": resp.status_code,
                "extraction": "PDF text extracted page by page with pypdf (layout may be imperfect)."}
    if "html" not in ctype and "xml" not in ctype:
        text = resp.content.decode(resp.encoding or "utf-8", "replace")
        return {"title": None, "body": text, "resolved": [resp.url], "status": resp.status_code,
                "extraction": f"Verbatim {ctype or 'unknown'} response body."}
    html = resp.content.decode(resp.encoding or resp.apparent_encoding or "utf-8", "replace")
    md, title, meta = html_to_markdown(html, selector)
    result = {"title": title, "body": md, "resolved": [resp.url], "status": resp.status_code,
              "extraction": "Main content extracted from HTML with BeautifulSoup + markdownify; scripts, "
              "navigation and footer chrome removed."}
    if meta.get("published_meta"):
        result["published_hint"] = meta["published_meta"]
    return result


STRATEGIES = {
    "github-blob": strat_github_blob, "github-tree": strat_github_tree, "github-repo": strat_github_repo,
    "github-issue": strat_github_issue, "github-pull": lambda u, a: strat_github_issue(u, a, pull=True),
    "github-pulls": strat_github_pulls, "gist": strat_gist, "discourse": strat_discourse, "hn": strat_hn,
    "html": strat_html, "pdf": strat_html, "text": strat_html,
}


# ---------------------------------------------------------------- output


def slugify(text: str, limit: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(slug) > limit:
        slug = slug[:limit].rsplit("-", 1)[0] or slug[:limit]
    return slug or "source"


def write_raw(topic: str, slug: str, published: str | None, content: str) -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", topic):
        raise FetchError("failed", f"invalid topic directory name: {topic}")
    directory = RAW_ROOT / topic
    directory.mkdir(parents=True, exist_ok=True)
    base = f"{published}-{slug}" if published else slug
    for n in range(1, 100):
        name = f"{base}.md" if n == 1 else f"{base}-{n}.md"
        path = directory / name
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        return path
    raise FetchError("failed", f"could not find a free filename for {base}")


def main(argv):
    ap = argparse.ArgumentParser(description="Fetch one ledger source into raw/.")
    ap.add_argument("--id", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--title")
    ap.add_argument("--slug")
    ap.add_argument("--published", help="YYYY-MM-DD, only when explicitly supported by the source")
    ap.add_argument("--mode", choices=sorted(STRATEGIES))
    ap.add_argument("--fetch-url", help="alternative public URL for the same resource (recorded as Resolved)")
    ap.add_argument("--selector", help="CSS selector for the main content (html mode)")
    ap.add_argument("--dry-run", action="store_true", help="fetch and report, but do not write raw")
    ap.add_argument("--representation", choices=("verbatim", "notes"), required=True)
    ap.add_argument("--license", required=True, help="SPDX id, or all-rights-reserved / unknown / terms-of-service")
    ap.add_argument("--license-evidence", required=True, help="where the license status was established")
    ap.add_argument("--attribution", help="required attribution, e.g. copyright holder")
    ap.add_argument("--notice-url", help="URL of the license/notice text to append verbatim (verbatim mode)")
    args = ap.parse_args(argv)

    if args.published and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.published):
        ap.error("--published must be YYYY-MM-DD")
    if args.representation == "verbatim":
        if args.license not in COPY_PERMITTED:
            print(json.dumps({"ok": False, "classification": "license", "reason":
                              f"license {args.license!r} does not permit verbatim export; use --representation notes"}))
            return 5
        if not args.attribution:
            ap.error("--attribution is required for verbatim export")
        if args.license in NOTICE_REQUIRED and not args.notice_url and not args.dry_run:
            ap.error(f"--notice-url is required: {args.license} requires its notice to accompany copies")
    archive = Archive(args.id)
    target = args.fetch_url or args.url
    mode = args.mode or detect_mode(target)
    try:
        if mode == "html" and args.selector:
            result = strat_html(target, archive, args.selector)
        else:
            result = STRATEGIES[mode](target, archive)
    except FetchError as exc:
        print(json.dumps({"ok": False, "id": args.id, "classification": exc.classification,
                          "reason": exc.reason, "http_status": exc.http_status,
                          "resolved_url": exc.resolved_url, "mode": mode,
                          "archived": [e["path"] for e in archive.entries]}, indent=2))
        return 3 if exc.classification == "blocked" else 4

    if urlparse(target).netloc in ("github.com", "gist.github.com") and mode != "gist":
        owner_repo = repo_parts(target)[:2]
        if len(owner_repo) == 2:
            result["license_hint"] = license_hint(*owner_repo, archive)
    title = (args.title or result.get("title") or args.url).strip()
    title = re.sub(r"\s+", " ", title)
    body = result["body"].strip() + "\n"
    warnings = list(result.get("warnings", []))
    visible = re.sub(r"\s+", " ", re.sub(r"[#>*`\-\[\]()|]", " ", body)).strip()
    if len(visible) < 400:
        warnings.append(f"thin content ({len(visible)} visible chars): possible JS shell or stub page")
    published = args.published
    resolved = [u for u in result.get("resolved", []) if u and u != args.url]
    if args.fetch_url and args.fetch_url != args.url and args.fetch_url not in resolved:
        resolved.insert(0, args.fetch_url)
    header = [f"# {title}", "", f"> Source: {args.url}"]
    if resolved:
        header.append(f"> Resolved: {'; '.join(resolved)}")
    header += [f"> Collected: {date.today().isoformat()}", f"> Published: {published or 'Unknown'}"]
    archived = [e for e in archive.entries]
    shas = ", ".join(f"{e['path']} (HTTP {e['status']}, sha256 {e['sha256'][:12]})" for e in archived[-6:])
    header.append(f"> Retrieval: HTTP GET, {date.today().isoformat()}; mode {mode}; "
                  f"{len(archived)} response(s) archived in build/reference-wiki/http/{args.id}/ (git-ignored)"
                  + (f": {shas}" if shas else ""))
    header.append(f"> Extraction: {result['extraction']}")
    hints = []
    if result.get("published"):
        hints.append(f"{result.get('published_evidence')}: {result['published']}")
    if result.get("published_hint"):
        hints.append(result["published_hint"])
    if hints and not published:
        header.append(f"> Date hints (not asserted as publication date): {'; '.join(hints)}")
    cache_header = header + [f"> Representation: Full verbatim extraction (cache only, git-ignored)",
                             f"> License: {args.license} ({args.license_evidence})"]
    slug = slugify(args.slug or title)
    report = {"id": args.id, "title": title, "slug": slug, "mode": mode, "http_status": result.get("status"),
              "resolved_url": resolved[0] if resolved else None, "chars": len(body), "warnings": warnings,
              "license_hint": result.get("license_hint"), "representation": args.representation}
    if args.dry_run:
        report.update({"ok": True, "dry_run": True, "preview": body[:1500]})
        print(json.dumps(report, indent=2))
        return 0
    cache_dir = FULLTEXT_ROOT / args.id
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{len(list(cache_dir.glob('*.md'))) + 1:03d}.md"
    cache_path.write_text("\n".join(cache_header) + "\n\n" + body, encoding="utf-8")
    report["fulltext"] = cache_path.relative_to(REPO_ROOT).as_posix()
    if args.representation == "notes":
        report.update({"ok": True, "raw": None,
                       "next": "write a notes raw with write_source_notes.py --fulltext " + report["fulltext"]})
        print(json.dumps(report, indent=2))
        return 0
    notice = ""
    if args.notice_url:
        try:
            resp = http_get(args.notice_url, archive, ext=".txt")
        except FetchError as exc:
            print(json.dumps({"ok": False, "classification": "license",
                              "reason": f"could not fetch license notice: {exc.reason}"}))
            return 5
        notice_text = resp.content.decode("utf-8", "replace")
        notice = (f"\n\n## License notice (verbatim, from {args.notice_url})\n\n" + fence(notice_text))
    header += [f"> Representation: Verbatim extraction of the source text (formatting noise removed)",
               f"> License: {args.license} — {args.license_evidence}",
               f"> Attribution: {args.attribution}"]
    content = "\n".join(header) + "\n\n" + body + notice
    try:
        path = write_raw(args.topic, slug, published, content)
    except FetchError as exc:
        print(json.dumps({"ok": False, "classification": exc.classification, "reason": exc.reason}))
        return 4
    report.update({"ok": True, "raw": path.relative_to(REPO_ROOT).as_posix()})
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
