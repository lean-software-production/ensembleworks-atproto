#!/usr/bin/env python3
"""Tests for source_ledger.py against a disposable copy of the ledger.

Never touches the real ledger: everything runs in a fresh directory under
build/reference-wiki/ledger-tests/ with its own lock file and repo root.

Usage: $REFERENCE_WIKI_PYTHON -I .agents/skills/karpathy-llm-wiki/scripts/test_source_ledger.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().with_name("source_ledger.py")
REPO_ROOT = Path(__file__).resolve().parents[4]
REAL_LEDGER = REPO_ROOT / "docs/reference/source-ledger-baseline.yaml"  # published pre-ingestion copy


class Sandbox:
    def __init__(self, name: str):
        self.root = REPO_ROOT / "build/reference-wiki/ledger-tests" / name
        shutil.rmtree(self.root, ignore_errors=True)
        (self.root / "docs/reference/raw/t").mkdir(parents=True)
        (self.root / "docs/reference/wiki/t").mkdir(parents=True)
        self.ledger = self.root / "sources.yaml"
        self.baseline = self.root / "baseline.yaml"
        shutil.copyfile(REAL_LEDGER, self.ledger)
        shutil.copyfile(REAL_LEDGER, self.baseline)
        self.lock = self.root / "sources.lock"

    def argv(self, *args: str) -> list[str]:
        return [sys.executable, "-I", str(SCRIPT), "--ledger", str(self.ledger), "--lock",
                str(self.lock), "--repo-root", str(self.root), *args]

    def run(self, *args: str, ok: bool = True) -> dict:
        proc = subprocess.run(self.argv(*args), capture_output=True, text=True, timeout=60)
        if ok and proc.returncode != 0:
            raise AssertionError(f"{args} failed: {proc.stderr}")
        if not ok:
            assert proc.returncode != 0, f"{args} unexpectedly succeeded: {proc.stdout}"
            return json.loads(proc.stderr or "{}")
        return json.loads(proc.stdout)


def test_concurrent_claims_are_distinct_and_atomic() -> None:
    box = Sandbox("concurrent")
    box.run("init")
    original = yaml.safe_load(box.baseline.read_text())
    total = len(original["sources"])

    parse_failures = []
    reads = 0
    stop = threading.Event()

    def reader():
        nonlocal reads
        while not stop.is_set():
            try:
                data = yaml.safe_load(box.ledger.read_text())
                assert len(data["sources"]) == total
                reads += 1
            except Exception as exc:  # noqa: BLE001 - any failure is a test failure
                parse_failures.append(repr(exc))

    thread = threading.Thread(target=reader)
    thread.start()
    claimants = 16  # 16 x 10 > total, so some claimants must come up short
    procs = [subprocess.Popen(box.argv("claim", "--worker", f"w{i:02d}", "--limit", "10"),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
             for i in range(claimants)]
    results = []
    for proc in procs:
        out, err = proc.communicate(timeout=120)
        assert proc.returncode == 0, err
        results.append(json.loads(out))
    stop.set()
    thread.join()

    claimed = [c["id"] for r in results for c in r["claimed"]]
    assert len(claimed) == len(set(claimed)), "a source was claimed twice"
    assert len(claimed) == total, f"expected {total} claims, got {len(claimed)}"
    assert all(len(r["claimed"]) <= 10 for r in results)
    assert not parse_failures, parse_failures[:3]
    assert reads > 0

    data = yaml.safe_load(box.ledger.read_text())
    holders = {s["id"]: s["ingestion"]["claimed_by"] for s in data["sources"]}
    for r in results:
        for c in r["claimed"]:
            assert holders[c["id"]] == r["worker"]

    # Nobody can steal a live claim: a late claimant gets nothing, and a
    # non-holder cannot complete, fail or release someone else's entry.
    late = box.run("claim", "--worker", "thief", "--limit", "10")
    assert late["claimed"] == [], late
    victim = next(c["id"] for result in results for c in result["claimed"])
    raw = box.root / "docs/reference/raw/t/x.md"
    raw.write_text("# x\n")
    box.run("fetched", "--worker", "thief", "--id", victim, "--raw", "docs/reference/raw/t/x.md",
            "--representation", "notes", "--license", "unknown", ok=False)
    box.run("fail", "--worker", "thief", "--id", victim, "--status", "failed", "--reason", "x", ok=False)
    box.run("release", "--worker", "thief", "--id", victim, ok=False)
    box.run("claim", "--worker", "thief", "--ids", victim, ok=True)
    assert holders[victim] == yaml.safe_load(box.ledger.read_text())["sources"][
        [s["id"] for s in data["sources"]].index(victim)]["ingestion"]["claimed_by"]

    verify = box.run("verify", "--baseline", str(box.baseline))
    assert verify["ok"], verify["problems"]
    print(f"ok concurrent: {claimants} claimants, {len(claimed)} distinct claims, {reads} clean reads")


def test_expired_lease_recovery_and_lifecycle() -> None:
    box = Sandbox("lease")
    box.run("init")
    first = box.run("claim", "--worker", "slow", "--limit", "2", "--lease-minutes", "0.05")
    ids = [c["id"] for c in first["claimed"]]
    assert len(ids) == 2
    # Still live: cannot be taken.
    assert box.run("claim", "--worker", "fast", "--ids", *ids)["claimed"] == []
    time.sleep(4.0)
    second = box.run("claim", "--worker", "fast", "--ids", *ids)
    assert sorted(second["recovered"]) == sorted(ids), second
    assert sorted(c["id"] for c in second["claimed"]) == sorted(ids)

    data = yaml.safe_load(box.ledger.read_text())
    entry = next(s for s in data["sources"] if s["id"] == ids[0])
    events = [h["event"] for h in entry["ingestion"]["history"]]
    assert events == ["initialised", "claimed", "lease_expired", "claimed"], events
    assert entry["ingestion"]["history"][2]["previous_holder"] == "slow"
    assert entry["ingestion"]["attempts"] == 2

    # The previous holder can no longer act on it.
    raw = box.root / "docs/reference/raw/t/a.md"
    raw.write_text("# a\n")
    box.run("fetched", "--worker", "slow", "--id", ids[0], "--raw", str(raw), "--representation", "notes",
            "--license", "unknown", ok=False)

    # Absolute in-repo path is stored repository-relative; outside paths rejected.
    box.run("fetched", "--worker", "fast", "--id", ids[0], "--raw", "/etc/hosts", "--representation", "notes",
            "--license", "unknown", ok=False)
    box.run("fetched", "--worker", "fast", "--id", ids[0], "--raw", str(raw), "--http-status", "200",
            "--representation", "verbatim", "--license", "MIT")
    shown = box.run("show", "--id", ids[0])
    assert shown["ingestion"]["raw"] == ["docs/reference/raw/t/a.md"], shown["ingestion"]["raw"]
    assert (shown["ingestion"]["representation"], shown["ingestion"]["license"]) == ("verbatim", "MIT")

    # Terminal failure keeps reason, status code and attempts.
    box.run("fail", "--worker", "fast", "--id", ids[1], "--status", "blocked",
            "--reason", "HTTP 403 from origin", "--http-status", "403")
    failed = box.run("show", "--id", ids[1])["ingestion"]
    assert (failed["status"], failed["http_status"], failed["attempts"]) == ("blocked", 403, 2)
    assert failed["reason"] == "HTTP 403 from origin"

    # Coordinator transitions: only fetched can be compiled.
    article = box.root / "docs/reference/wiki/t/concept.md"
    article.write_text("# c\n")
    box.run("compiled", "--id", ids[1], "--article", "docs/reference/wiki/t/concept.md", ok=False)
    box.run("compiled", "--id", ids[0], "--article", "docs/reference/wiki/t/concept.md")
    assert box.run("show", "--id", ids[0])["ingestion"]["status"] == "compiled"

    # Explicit retry of a blocked source keeps its history.
    box.run("reset", "--id", ids[1], "--reason", "retry after rate limit window")
    again = box.run("show", "--id", ids[1])["ingestion"]
    assert again["status"] == "pending" and again["history"][-1]["previous_reason"] == "HTTP 403 from origin"

    verify = box.run("verify", "--baseline", str(box.baseline))
    assert verify["ok"], verify["problems"]
    print("ok lease: expiry recovery, no-steal after expiry, relative paths, terminal metadata")


if __name__ == "__main__":
    test_concurrent_claims_are_distinct_and_atomic()
    test_expired_lease_recovery_and_lifecycle()
    print("all ledger tests passed")
