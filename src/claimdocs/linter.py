"""claimdocs linter — the gate.

Generic over a Vocabulary (claimdocs.yml). Every rule is the machine-checkable form of
a doctrine statement in CHARTER.md. The linter is the reason claimdocs is a typed graph
and not a corkboard: an edge that cannot cite its basis does not ship.

Two layers, kept honest and separate:

  citation-shape (always): receipts present + resolve, modes valid, refusal blocks on
    authority edges, derivation well-formed, caps respected.
  basis resolution (--verify, repo-dependent): cited code/test symbols still resolve
    (existence) and are unchanged since admission (freshness). NEVER adequacy — that is
    a human admission recorded on the edge, surfaced but not proven.
"""
from __future__ import annotations

import datetime as _dt
import glob
import os

import yaml

from .config import Vocabulary
from .verify import resolve_basis


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.notes = []     # informational lines for --verify summaries

    def error(self, code, loc, msg): self.errors.append((code, loc, msg))
    def warn(self, code, loc, msg): self.warnings.append((code, loc, msg))
    def note(self, msg): self.notes.append(msg)

    def print(self):
        for code, loc, msg in self.warnings:
            print(f"  warn  [{code}] {loc}: {msg}")
        for code, loc, msg in self.errors:
            print(f"  ERROR [{code}] {loc}: {msg}")
        for line in self.notes:
            print(f"  {line}")
        print(f"\n{len(self.errors)} error(s), {len(self.warnings)} warning(s).")
        return not self.errors


def _load(path):
    with open(path) as fh:
        return yaml.safe_load(fh)


def load_receipts(root):
    receipts = {}
    rdir = os.path.join(root, "receipts")
    if os.path.isdir(rdir):
        for p in sorted(glob.glob(os.path.join(rdir, "*.yaml")) + glob.glob(os.path.join(rdir, "*.yml"))):
            rec = _load(p)
            if isinstance(rec, dict) and "id" in rec:
                receipts[rec["id"]] = rec
    return receipts


def load_cases(root):
    cases = []
    if os.path.isfile(root):
        return [(root, _load(root))]
    cdir = os.path.join(root, "cases") if os.path.isdir(os.path.join(root, "cases")) else root
    for p in sorted(glob.glob(os.path.join(cdir, "*.yaml")) + glob.glob(os.path.join(cdir, "*.yml"))):
        cases.append((p, _load(p)))
    return cases


def _date(s):
    return s if isinstance(s, _dt.date) else _dt.date.fromisoformat(str(s))


def lint(root, vocab: Vocabulary, report: Report, today: str,
         verify: bool = False, repos: dict | None = None, strict_adequacy: bool = False):
    today = _date(today)
    repos = repos or {}
    receipts = load_receipts(root)
    cases = load_cases(root)

    NODE_KINDS = set(vocab.node_kinds)
    EDGE_KINDS = set(vocab.edge_kinds)
    MODES = set(vocab.claim_modes)
    BASIS_KINDS = set(vocab.basis_kinds)

    n_resolved = n_unresolved = n_fresh = n_changed = n_unhashable = 0
    n_admitted = n_unadmitted = 0

    for path, case in cases:
        loc0 = os.path.basename(path)
        if not isinstance(case, dict):
            report.error("CASE_MALFORMED", loc0, "case file is not a mapping"); continue

        local = dict(receipts)
        for rec in case.get("receipts_inline", []) or []:
            if isinstance(rec, dict) and "id" in rec:
                local[rec["id"]] = rec

        nodes = case.get("nodes", []) or []
        node_ids = set()
        for n in nodes:
            nid = n.get("id")
            if not nid:
                report.error("NODE_NO_ID", loc0, f"node missing id: {n}"); continue
            if n.get("type") not in NODE_KINDS:
                report.error("NODE_BAD_TYPE", f"{loc0}:{nid}", f"unknown node kind {n.get('type')!r}")
            node_ids.add(nid)

        edges = case.get("edges", []) or []
        caps = {}  # mode -> count, for max_per_case

        for rid, rec in local.items():
            rloc = f"{loc0}:{rid}"
            kind = rec.get("kind")
            if kind not in BASIS_KINDS:
                report.error("RECEIPT_BAD_KIND", rloc, f"unknown basis kind {kind!r}")
            if not rec.get("retrieved"):
                report.error("RECEIPT_NO_DATE", rloc, "receipt missing `retrieved` date")
            else:
                try:
                    age = (today - _date(rec["retrieved"])).days
                    if age > vocab.staleness_days:
                        report.warn("RECEIPT_STALE", rloc, f"retrieved {age}d ago (> {vocab.staleness_days}d)")
                except ValueError:
                    report.error("RECEIPT_BAD_DATE", rloc, f"unparseable date {rec['retrieved']!r}")

            # --- basis resolution (existence + freshness), --verify only ---
            if verify and kind in BASIS_KINDS and vocab.basis_kinds[kind].resolvable:
                repo_root = repos.get(rec.get("repo", "default"))
                if not repo_root:
                    report.warn("BASIS_REPO_ABSENT", rloc,
                                f"repo {rec.get('repo','default')!r} unavailable to --verify")
                    continue
                if not rec.get("path"):
                    report.error("BASIS_NO_PATH", rloc, f"{kind} receipt needs a `path` to resolve")
                    continue
                st = resolve_basis(repo_root, rec["path"], rec.get("symbol"))
                if not st.resolved:
                    n_unresolved += 1
                    report.error("BASIS_MISSING", rloc, st.detail)  # fail closed
                    continue
                n_resolved += 1
                admitted = rec.get("body_sha256")
                if st.body_hash is None:
                    n_unhashable += 1
                elif admitted is None:
                    n_unhashable += 1
                    report.warn("BASIS_UNADMITTED_BODY", rloc,
                                "resolvable body present but no `body_sha256` recorded at admission")
                elif admitted != st.body_hash:
                    n_changed += 1
                    # The hollow-test vector: still resolves, body changed since admission.
                    report.error("BASIS_BODY_CHANGED", rloc,
                                 "symbol resolves but its body changed since admission "
                                 "(adequacy STALE — re-admit after confirming it still supports the edge)")
                else:
                    n_fresh += 1

        for e in edges:
            eid = e.get("id", "<no-id>")
            eloc = f"{loc0}:{eid}"
            etype = e.get("type")
            claim = e.get("claim")
            if etype not in EDGE_KINDS:
                report.error("EDGE_BAD_TYPE", eloc, f"unknown edge kind {etype!r}")
            if claim not in MODES:
                report.error("EDGE_BAD_CLAIM", eloc, f"unknown claim mode {claim!r}");
            for end in ("from", "to"):
                if e.get(end) not in node_ids:
                    report.error("EDGE_DANGLING_REF", eloc, f"`{end}` -> {e.get(end)!r} resolves to no node")

            recs = e.get("receipts") or []
            if not recs:
                report.error("EDGE_NO_RECEIPT", eloc, "edge has no receipts (>=1 required)")
            for rid in recs:
                if rid not in local:
                    report.error("EDGE_RECEIPT_UNRESOLVED", eloc, f"receipt {rid!r} not found")
            kinds = {local[r]["kind"] for r in recs if r in local}

            mode = vocab.claim_modes.get(claim)
            if mode:
                # witnessing mode (e.g. wired/documented) needs a witnessing basis.
                if mode.witnesses and kinds and not (kinds & vocab.witnessing_basis_kinds):
                    report.error("MODE_NEEDS_WITNESS", eloc,
                                 f"claim={claim} asserts a witnessed edge but receipts are only "
                                 f"{sorted(kinds)} — a doc proposes an edge, it does not witness one. "
                                 f"Downgrade to a non-witnessing mode.")
                # derivation modes need parents (depth-1).
                if mode.requires_derivation:
                    deriv = e.get("derivation") or []
                    if not deriv:
                        report.error("DERIVATION_MISSING", eloc, f"claim={claim} requires non-empty derivation")
                    for pid in deriv:
                        parent = next((x for x in edges if x.get("id") == pid), None)
                        if parent is None:
                            report.error("DERIVATION_PARENT_MISSING", eloc, f"parent {pid!r} not in case")
                        elif parent.get("claim") in vocab.derivation_modes:
                            report.error("DERIVATION_TOWER", eloc,
                                         f"parent {pid!r} is itself a derivation mode (depth-1 cap)")
                if mode.max_per_case is not None:
                    caps[claim] = caps.get(claim, 0) + 1

                # adequacy: witnessing edges must RECORD an admission. claimdocs can never
                # prove adequacy; it can require that a human said "this basis supports this
                # edge" and pinned the revision. Surfaced always; enforced under --verify.
                if mode.witnesses:
                    adq = e.get("adequacy") or {}
                    if adq.get("status") == "admitted" and adq.get("admitted_at"):
                        n_admitted += 1
                    else:
                        n_unadmitted += 1
                        msg = ("witnessing edge has no recorded adequacy admission "
                               "(status: admitted + admitted_at). Resolved != supported.")
                        if verify or strict_adequacy:
                            report.error("ADEQUACY_UNADMITTED", eloc, msg)
                        else:
                            report.warn("ADEQUACY_UNADMITTED", eloc, msg)

            # refusal block on authority-boundary edges.
            if etype in vocab.refusal_edge_kinds:
                r = e.get("refusal")
                if not isinstance(r, dict) or "refuses" not in r or "kind" not in r:
                    report.error("REFUSAL_MISSING", eloc,
                                 f"`{etype}` edge requires a refusal block with `refuses` + `kind`")

        for claim, count in caps.items():
            cap = vocab.claim_modes[claim].max_per_case
            if cap is not None and count > cap:
                report.error("MODE_OVER_CAP", loc0, f"{count} {claim} edges (max {cap} per case)")

        touched = set()
        for e in edges:
            touched.add(e.get("from")); touched.add(e.get("to"))
        for n in nodes:
            kind = vocab.node_kinds.get(n.get("type"))
            # nodes whose kind sits in the last lane (constellation/external) may be edgeless by design.
            exempt = kind and kind.lane == (vocab.lanes[-1] if vocab.lanes else "")
            if n.get("id") not in touched and not exempt:
                report.warn("NODE_ORPHAN", f"{loc0}:{n.get('id')}",
                            f"node {n.get('id')!r} ({n.get('type')}) is touched by no edge")

    if verify:
        report.note("")
        report.note(f"basis existence:  {n_resolved} resolved, {n_unresolved} missing")
        report.note(f"basis freshness:  {n_fresh} fresh, {n_changed} changed-since-admission, "
                    f"{n_unhashable} not body-hashable (existence-only)")
        report.note(f"edge adequacy:    {n_admitted} admitted, {n_unadmitted} unadmitted "
                    f"— ADMISSION is human; claimdocs proves existence/freshness, NOT adequacy")
    return report
