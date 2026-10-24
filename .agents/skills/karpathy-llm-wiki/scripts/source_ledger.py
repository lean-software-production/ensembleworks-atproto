#!/usr/bin/env python3
"""Concurrency-safe ingestion ledger for docs/research/sources.yaml.

Local extension to the upstream karpathy-llm-wiki skill (see UPSTREAM.md).
Every agent, coordinator included, changes the ledger only through this
script. Each command is one transaction: take an exclusive fcntl.flock on a
single lock file, read and parse the ledger, check preconditions, write a
temporary file in the ledger's directory, re-parse it, fsync, os.replace it
over the ledger, then release the lock. Readers never see a partial file.

Source entries keep their original id, url and references untouched. This
script only adds and edits each entry's `ingestion` mapping:

    ingestion:
      status: pending | claimed | fetched | compiled | no_material | blocked | failed
      attempts: <number of claims taken>
      claimed_by / claimed_at / lease_expires_at: live claim (claimed only)
      raw: [repository-relative raw files]          (set by `fetched`)
      representation: verbatim | notes              (set by `fetched`)
      license: license status + evidence            (set by `fetched`)
      resolved_url: URL actually fetched, if it differs
      http_status: last relevant HTTP status code, if any
      reason: why the source is blocked / failed / no_material
      articles: [repository-relative wiki articles] (set by `compiled`)
      history: [{at, event, by, ...}]               (append-only)

Lifecycle:
    pending -> claimed            claim (worker)
    claimed -> fetched            fetched (claim holder)
    claimed -> blocked | failed   fail (claim holder)
    claimed -> pending            release (claim holder) or recover (lease expired)
    fetched -> compiled           compiled (coordinator)
    fetched -> no_material        no-material (coordinator)
    blocked | failed -> pending   reset (coordinator, explicit retry)

`claim` never takes an entry whose lease is unexpired. An entry whose lease
has expired is recovered back to pending with a `lease_expired` history event
(by `recover`, or automatically inside `claim`) before anyone may claim it.

Commands (run with $REFERENCE_WIKI_PYTHON):
    init                      add a pending ingestion mapping where missing
    claim --worker W [--limit N] [--lease-minutes M] [--ids ID ...]
    renew --worker W --id ID [--lease-minutes M]
    fetched --worker W --id ID --raw PATH [--raw PATH ...] --representation verbatim|notes
            --license TEXT [--resolved-url U] [--http-status N] [--note TEXT]
    fail --worker W --id ID --status blocked|failed --reason TEXT [--http-status N]
            [--resolved-url U]
    release --worker W --id ID [--note TEXT]
    compiled --id ID --article PATH [--article PATH ...] [--note TEXT]
    no-material --id ID --reason TEXT
    reset --id ID --reason TEXT
    recover                   return expired claims to pending
    status                    counts by status (+ live claims), always JSON
    show --id ID | list [--status S]
    verify --baseline FILE [--require-terminal]

Global options: --ledger PATH (default docs/research/sources.yaml),
--lock PATH (default build/reference-wiki/sources.lock), --repo-root PATH.
Paths in ledger metadata are stored repository-relative; absolute paths
inside the repository are converted, anything outside is rejected.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import fcntl
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_LEDGER = "docs/research/sources.yaml"
DEFAULT_LOCK = "build/reference-wiki/sources.lock"
DEFAULT_RAW_PREFIX = "docs/reference/raw/"
DEFAULT_WIKI_PREFIX = "docs/reference/wiki/"

STATUSES = ("pending", "claimed", "fetched", "compiled", "no_material", "blocked", "failed")
TERMINAL = ("compiled", "no_material", "blocked", "failed")
DEFAULT_LEASE_MINUTES = 45


class LedgerError(Exception):
    pass


# ---------------------------------------------------------------- yaml i/o


class _Dumper(yaml.SafeDumper):
    pass


def _represent_list(dumper, data):
    flow = bool(data) and all(isinstance(x, int) and not isinstance(x, bool) for x in data)
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=flow)


_Dumper.add_representer(list, _represent_list)


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def leading_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith("#"):
            lines.append(line)
        else:
            break
    return "\n".join(lines) + ("\n" if lines else "")


def dump(data: dict) -> str:
    return yaml.dump(data, Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=4096)


class Ledger:
    def __init__(self, path: Path, lock: Path):
        self.path = path
        self.lock = lock

    @contextlib.contextmanager
    def transaction(self, write: bool = True):
        self.lock.parent.mkdir(parents=True, exist_ok=True)
        with open(self.lock, "a+") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            try:
                text = self.path.read_text(encoding="utf-8")
                data = yaml.safe_load(text)
                if not isinstance(data, dict) or not isinstance(data.get("sources"), list):
                    raise LedgerError(f"{self.path} is not a sources ledger")
                before = copy.deepcopy(data)
                yield data
                if write and data != before:
                    self._replace(leading_comments(text) + dump(data), data)
            finally:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)

    def _replace(self, text: str, expected: dict) -> None:
        fd, tmp = tempfile.mkstemp(prefix=f".{self.path.name}.", suffix=".tmp", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            if yaml.safe_load(Path(tmp).read_text(encoding="utf-8")) != expected:
                raise LedgerError("serialised ledger does not round-trip; aborting write")
            os.replace(tmp, self.path)
            dir_fd = os.open(self.path.parent, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except BaseException:
            with contextlib.suppress(FileNotFoundError):
                os.unlink(tmp)
            raise


# ---------------------------------------------------------------- helpers


def blank_ingestion() -> dict:
    return {
        "status": "pending",
        "attempts": 0,
        "claimed_by": None,
        "claimed_at": None,
        "lease_expires_at": None,
        "raw": [],
        "representation": None,
        "license": None,
        "resolved_url": None,
        "http_status": None,
        "reason": None,
        "articles": [],
        "history": [],
    }


def find(data: dict, source_id: str) -> dict:
    for source in data["sources"]:
        if source.get("id") == source_id:
            if "ingestion" not in source:
                raise LedgerError(f"{source_id} has no ingestion mapping; run init")
            return source
    raise LedgerError(f"unknown source id: {source_id}")


def event(ing: dict, name: str, by: str, at: datetime, **detail) -> None:
    entry = {"at": iso(at), "event": name, "by": by}
    entry.update({k: v for k, v in detail.items() if v is not None})
    ing["history"].append(entry)


def clear_claim(ing: dict) -> None:
    ing["claimed_by"] = None
    ing["claimed_at"] = None
    ing["lease_expires_at"] = None


def is_expired(ing: dict, at: datetime) -> bool:
    expiry = ing.get("lease_expires_at")
    return ing["status"] == "claimed" and (expiry is None or parse_iso(expiry) <= at)


def recover_expired(data: dict, at: datetime, by: str) -> list[str]:
    recovered = []
    for source in data["sources"]:
        ing = source.get("ingestion")
        if ing and is_expired(ing, at):
            event(ing, "lease_expired", by, at, previous_holder=ing["claimed_by"],
                  lease_expires_at=ing["lease_expires_at"])
            ing["status"] = "pending"
            clear_claim(ing)
            recovered.append(source["id"])
    return recovered


def require_holder(source: dict, worker: str, at: datetime) -> dict:
    ing = source["ingestion"]
    if ing["status"] != "claimed":
        raise LedgerError(f"{source['id']} is {ing['status']}, not claimed")
    if ing["claimed_by"] != worker:
        raise LedgerError(f"{source['id']} is claimed by {ing['claimed_by']}, not {worker}")
    if is_expired(ing, at):
        raise LedgerError(f"{source['id']}: lease held by {worker} expired at {ing['lease_expires_at']}")
    return ing


def repo_relative(value: str, repo_root: Path, prefix: str) -> str:
    path = Path(value)
    if path.is_absolute():
        try:
            path = path.resolve().relative_to(repo_root.resolve())
        except ValueError as exc:
            raise LedgerError(f"path outside repository: {value}") from exc
    rel = path.as_posix()
    if rel.startswith("./"):
        rel = rel[2:]
    if ".." in Path(rel).parts:
        raise LedgerError(f"path must not contain '..': {value}")
    if not rel.startswith(prefix):
        raise LedgerError(f"path must be under {prefix}: {value}")
    if not (repo_root / rel).is_file():
        raise LedgerError(f"file does not exist: {rel}")
    return rel


# ---------------------------------------------------------------- commands


def cmd_init(ledger: Ledger, args) -> dict:
    added = 0
    with ledger.transaction() as data:
        at = now_utc()
        for source in data["sources"]:
            if "ingestion" not in source:
                source["ingestion"] = blank_ingestion()
                event(source["ingestion"], "initialised", args.by, at)
                added += 1
    return {"initialised": added}


def cmd_claim(ledger: Ledger, args) -> dict:
    if args.limit < 1 or args.limit > 10:
        raise LedgerError("--limit must be between 1 and 10")
    with ledger.transaction() as data:
        at = now_utc()
        recovered = recover_expired(data, at, args.worker)
        wanted = set(args.ids or [])
        claimed = []
        for source in data["sources"]:
            if len(claimed) >= args.limit:
                break
            if wanted and source["id"] not in wanted:
                continue
            ing = source.get("ingestion")
            if not ing or ing["status"] != "pending":
                continue
            ing["status"] = "claimed"
            ing["attempts"] += 1
            ing["claimed_by"] = args.worker
            ing["claimed_at"] = iso(at)
            ing["lease_expires_at"] = iso(at + timedelta(minutes=args.lease_minutes))
            event(ing, "claimed", args.worker, at, attempt=ing["attempts"],
                  lease_expires_at=ing["lease_expires_at"])
            claimed.append({"id": source["id"], "url": source["url"],
                            "lease_expires_at": ing["lease_expires_at"]})
    return {"worker": args.worker, "claimed": claimed, "recovered": recovered}


def cmd_renew(ledger: Ledger, args) -> dict:
    with ledger.transaction() as data:
        at = now_utc()
        ing = require_holder(find(data, args.id), args.worker, at)
        ing["lease_expires_at"] = iso(at + timedelta(minutes=args.lease_minutes))
        event(ing, "renewed", args.worker, at, lease_expires_at=ing["lease_expires_at"])
    return {"id": args.id, "lease_expires_at": ing["lease_expires_at"]}


def cmd_fetched(ledger: Ledger, args) -> dict:
    raws = [repo_relative(r, args.repo_root, args.raw_prefix) for r in args.raw]
    with ledger.transaction() as data:
        at = now_utc()
        ing = require_holder(find(data, args.id), args.worker, at)
        ing["status"] = "fetched"
        ing["raw"] = sorted(set(ing["raw"]) | set(raws))
        ing["representation"] = args.representation
        ing["license"] = args.license
        ing["resolved_url"] = args.resolved_url or ing["resolved_url"]
        ing["http_status"] = args.http_status if args.http_status is not None else ing["http_status"]
        ing["reason"] = None
        clear_claim(ing)
        event(ing, "fetched", args.worker, at, raw=raws, representation=args.representation,
              license=args.license, resolved_url=args.resolved_url,
              http_status=args.http_status, note=args.note)
    return {"id": args.id, "status": "fetched", "raw": ing["raw"]}


def cmd_fail(ledger: Ledger, args) -> dict:
    with ledger.transaction() as data:
        at = now_utc()
        ing = require_holder(find(data, args.id), args.worker, at)
        ing["status"] = args.status
        ing["reason"] = args.reason
        ing["http_status"] = args.http_status
        ing["resolved_url"] = args.resolved_url or ing["resolved_url"]
        clear_claim(ing)
        event(ing, args.status, args.worker, at, reason=args.reason,
              http_status=args.http_status, resolved_url=args.resolved_url)
    return {"id": args.id, "status": args.status, "attempts": ing["attempts"]}


def cmd_release(ledger: Ledger, args) -> dict:
    with ledger.transaction() as data:
        at = now_utc()
        ing = require_holder(find(data, args.id), args.worker, at)
        ing["status"] = "pending"
        clear_claim(ing)
        event(ing, "released", args.worker, at, note=args.note)
    return {"id": args.id, "status": "pending"}


def _coordinator_transition(ledger: Ledger, args, target: str, articles=None) -> dict:
    with ledger.transaction() as data:
        at = now_utc()
        source = find(data, args.id)
        ing = source["ingestion"]
        if ing["status"] not in ("fetched", target):
            raise LedgerError(f"{args.id} is {ing['status']}; only fetched sources can become {target}")
        if not ing["raw"]:
            raise LedgerError(f"{args.id} has no raw file recorded")
        ing["status"] = target
        if articles is not None:
            ing["articles"] = sorted(set(ing["articles"]) | set(articles))
        if target == "no_material":
            ing["reason"] = args.reason
        event(ing, target, args.by, at, articles=articles, reason=getattr(args, "reason", None),
              note=getattr(args, "note", None))
    return {"id": args.id, "status": target, "articles": ing["articles"]}


def cmd_compiled(ledger: Ledger, args) -> dict:
    articles = [repo_relative(a, args.repo_root, args.wiki_prefix) for a in args.article]
    return _coordinator_transition(ledger, args, "compiled", articles)


def cmd_no_material(ledger: Ledger, args) -> dict:
    return _coordinator_transition(ledger, args, "no_material")


def cmd_reset(ledger: Ledger, args) -> dict:
    with ledger.transaction() as data:
        at = now_utc()
        ing = find(data, args.id)["ingestion"]
        if ing["status"] not in ("blocked", "failed"):
            raise LedgerError(f"{args.id} is {ing['status']}; only blocked/failed can be reset")
        event(ing, "reset", args.by, at, previous_status=ing["status"],
              previous_reason=ing["reason"], reason=args.reason)
        ing["status"] = "pending"
    return {"id": args.id, "status": "pending"}


def cmd_recover(ledger: Ledger, args) -> dict:
    with ledger.transaction() as data:
        recovered = recover_expired(data, now_utc(), args.by)
    return {"recovered": recovered}


def counts(data: dict) -> dict:
    result = {status: 0 for status in STATUSES}
    result["uninitialised"] = 0
    for source in data["sources"]:
        ing = source.get("ingestion")
        if ing:
            result[ing["status"]] += 1
        else:
            result["uninitialised"] += 1
    return result


def cmd_status(ledger: Ledger, args) -> dict:
    with ledger.transaction(write=False) as data:
        at = now_utc()
        live = [
            {"id": s["id"], "claimed_by": s["ingestion"]["claimed_by"],
             "lease_expires_at": s["ingestion"]["lease_expires_at"],
             "expired": is_expired(s["ingestion"], at)}
            for s in data["sources"]
            if s.get("ingestion") and s["ingestion"]["status"] == "claimed"
        ]
        return {"total": len(data["sources"]), "counts": counts(data), "claims": live}


def cmd_show(ledger: Ledger, args) -> dict:
    with ledger.transaction(write=False) as data:
        return find(data, args.id)


def cmd_list(ledger: Ledger, args) -> dict:
    with ledger.transaction(write=False) as data:
        return {"sources": [
            {"id": s["id"], "url": s["url"], "status": s.get("ingestion", {}).get("status"),
             "raw": s.get("ingestion", {}).get("raw"), "reason": s.get("ingestion", {}).get("reason")}
            for s in data["sources"]
            if not args.status or s.get("ingestion", {}).get("status") == args.status
        ]}


def cmd_verify(ledger: Ledger, args) -> dict:
    baseline = yaml.safe_load(Path(args.baseline).read_text(encoding="utf-8"))
    problems = []
    with ledger.transaction(write=False) as data:
        current = {s["id"]: s for s in data["sources"]}
        if len(current) != len(data["sources"]):
            problems.append("duplicate ids in ledger")
        base_ids = [s["id"] for s in baseline["sources"]]
        if [s["id"] for s in data["sources"]][: len(base_ids)] != base_ids:
            problems.append("original id order changed")
        for original in baseline["sources"]:
            entry = current.get(original["id"])
            if entry is None:
                problems.append(f"{original['id']}: missing")
                continue
            for key, value in original.items():
                if entry.get(key) != value:
                    problems.append(f"{original['id']}: {key} changed")
            ing = entry.get("ingestion")
            if not ing:
                problems.append(f"{original['id']}: no ingestion mapping")
                continue
            if ing["status"] not in STATUSES:
                problems.append(f"{original['id']}: invalid status {ing['status']}")
            if args.require_terminal and ing["status"] not in TERMINAL:
                problems.append(f"{original['id']}: not terminal ({ing['status']})")
            if ing["status"] in ("blocked", "failed") and not ing.get("reason"):
                problems.append(f"{original['id']}: {ing['status']} without reason")
            if ing["status"] == "compiled" and not ing.get("articles"):
                problems.append(f"{original['id']}: compiled without articles")
            if ing["status"] in ("fetched", "compiled", "no_material"):
                if not ing.get("raw"):
                    problems.append(f"{original['id']}: {ing['status']} without raw")
                if ing.get("representation") not in ("verbatim", "notes") or not ing.get("license"):
                    problems.append(f"{original['id']}: {ing['status']} without representation/license")
            for rel in (ing.get("raw") or []) + (ing.get("articles") or []):
                if Path(rel).is_absolute() or ".." in Path(rel).parts:
                    problems.append(f"{original['id']}: non-relative path {rel}")
                elif not (args.repo_root / rel).is_file():
                    problems.append(f"{original['id']}: path missing on disk {rel}")
        return {"baseline": len(base_ids), "ledger": len(data["sources"]),
                "counts": counts(data), "ok": not problems, "problems": problems}


# ---------------------------------------------------------------- cli


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--ledger", default=None)
    parser.add_argument("--lock", default=None)
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--raw-prefix", default=DEFAULT_RAW_PREFIX)
    parser.add_argument("--wiki-prefix", default=DEFAULT_WIKI_PREFIX)
    parser.add_argument("--by", default="coordinator", help="actor name for coordinator commands")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init").set_defaults(func=cmd_init)

    p = sub.add_parser("claim")
    p.add_argument("--worker", required=True)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--lease-minutes", type=float, default=DEFAULT_LEASE_MINUTES)
    p.add_argument("--ids", nargs="*")
    p.set_defaults(func=cmd_claim)

    p = sub.add_parser("renew")
    p.add_argument("--worker", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--lease-minutes", type=float, default=DEFAULT_LEASE_MINUTES)
    p.set_defaults(func=cmd_renew)

    p = sub.add_parser("fetched")
    p.add_argument("--worker", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--raw", action="append", required=True)
    p.add_argument("--representation", choices=("verbatim", "notes"), required=True)
    p.add_argument("--license", required=True)
    p.add_argument("--resolved-url")
    p.add_argument("--http-status", type=int)
    p.add_argument("--note")
    p.set_defaults(func=cmd_fetched)

    p = sub.add_parser("fail")
    p.add_argument("--worker", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--status", choices=("blocked", "failed"), required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--http-status", type=int)
    p.add_argument("--resolved-url")
    p.set_defaults(func=cmd_fail)

    p = sub.add_parser("release")
    p.add_argument("--worker", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--note")
    p.set_defaults(func=cmd_release)

    p = sub.add_parser("compiled")
    p.add_argument("--id", required=True)
    p.add_argument("--article", action="append", required=True)
    p.add_argument("--note")
    p.set_defaults(func=cmd_compiled)

    p = sub.add_parser("no-material")
    p.add_argument("--id", required=True)
    p.add_argument("--reason", required=True)
    p.set_defaults(func=cmd_no_material)

    p = sub.add_parser("reset")
    p.add_argument("--id", required=True)
    p.add_argument("--reason", required=True)
    p.set_defaults(func=cmd_reset)

    sub.add_parser("recover").set_defaults(func=cmd_recover)

    p = sub.add_parser("status")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("show")
    p.add_argument("--id", required=True)
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("list")
    p.add_argument("--status", choices=STATUSES)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("verify")
    p.add_argument("--baseline", required=True)
    p.add_argument("--require-terminal", action="store_true")
    p.set_defaults(func=cmd_verify)
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    args.repo_root = Path(args.repo_root).resolve()
    ledger_path = Path(args.ledger) if args.ledger else args.repo_root / DEFAULT_LEDGER
    lock_path = Path(args.lock) if args.lock else args.repo_root / DEFAULT_LOCK
    try:
        result = args.func(Ledger(ledger_path, lock_path), args)
    except LedgerError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, default=str))
    if args.command == "verify" and not result["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
