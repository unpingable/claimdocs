"""claimdocs builder — render the admitted claim graph to site data.

Emits two files the (generic, config-driven) renderer reads:

    docs/data/graph.json   # cytoscape elements: nodes + edges
    docs/data/vocab.json   # the vocabulary pack: mode colors/styles, node labels, lanes

The renderer therefore knows nothing hard-coded about any project. Build REFUSES on any
lint error — fail closed. The site is a readout; the claim graph is the artifact.
"""
from __future__ import annotations

import glob
import json
import os

import yaml

from .config import Vocabulary
from .linter import Report, lint


def _load(path):
    with open(path) as fh:
        return yaml.safe_load(fh)


def _short(n):
    if n.get("short_label"):
        return n["short_label"]
    lab = n.get("label", n["id"]).split("(")[0].split("—")[0].strip()
    return lab if len(lab) <= 26 else " ".join(lab.split()[:3]) + "…"


def to_elements(root, vocab: Vocabulary, include_excluded: bool):
    receipts = {}
    rdir = os.path.join(root, "receipts")
    if os.path.isdir(rdir):
        for p in sorted(glob.glob(os.path.join(rdir, "*.y*ml"))):
            r = _load(p)
            if isinstance(r, dict) and "id" in r:
                receipts[r["id"]] = r
    nodes, edges, cases, seen = [], [], [], set()
    for p in sorted(glob.glob(os.path.join(root, "cases", "*.y*ml"))):
        case = _load(p)
        cid = case.get("case_id")
        cases.append({k: case.get(k) for k in ("case_id", "title", "status", "headline", "dek", "why")})
        for n in case.get("nodes", []) or []:
            if n["id"] in seen:
                continue
            seen.add(n["id"])
            lane = n.get("lane") or (vocab.node_kinds.get(n.get("type")).lane
                                     if n.get("type") in vocab.node_kinds else vocab.lanes[0])
            nodes.append({"data": {
                "id": n["id"], "type": n.get("type"), "label": n.get("label", n["id"]),
                "short_label": _short(n), "lane": lane,
                "rank": vocab.lane_index.get(lane, 0), "case": cid}})
        for e in case.get("edges", []) or []:
            m = vocab.claim_modes.get(e.get("claim"))
            if m and m.excluded_from_default and not include_excluded:
                continue
            role = vocab.edge_kinds.get(e.get("type")).role if e.get("type") in vocab.edge_kinds else "flow"
            data = {
                "id": e["id"], "source": e.get("from"), "target": e.get("to"),
                "type": e.get("type"), "claim": e.get("claim"), "case": cid, "role": role,
                "receipts": [receipts.get(r, {"id": r}) for r in (e.get("receipts") or [])],
                "derivation": e.get("derivation", []),
            }
            if "refusal" in e:
                data["refusal"] = e["refusal"]
            if "adequacy" in e:
                data["adequacy"] = e["adequacy"]
            edges.append({"data": data, "classes": f"{e.get('claim','')} {role}".strip()})
    return {"nodes": nodes, "edges": edges, "cases": cases}


def vocab_json(vocab: Vocabulary):
    return {
        "project": vocab.project, "title": vocab.title,
        "lanes": [{"id": l, "label": l.replace("_", " ").title()} for l in vocab.lanes],
        "default_modes": sorted(vocab.default_modes),
        "claim_modes": {m.name: {"color": m.color, "style": m.style, "witnesses": m.witnesses,
                                 "excluded_from_default": m.excluded_from_default, "help": m.help,
                                 "canonical": m.canonical, "wording": m.wording}
                        for m in vocab.claim_modes.values()},
        "node_kinds": {n.name: {"color": n.color, "label": n.label, "shape": n.shape,
                                "lane": n.lane, "what": n.what, "why": n.why}
                       for n in vocab.node_kinds.values()},
        "edge_kinds": {e.name: {"role": e.role, "verb": e.verb} for e in vocab.edge_kinds.values()},
    }


def build(root, vocab: Vocabulary, out_dir, today, include_excluded=False) -> int:
    report = Report()
    lint(root, vocab, report, today)
    if report.errors:
        report.print()
        print("build refused: fix lint errors first.")
        return 1
    elements = to_elements(root, vocab, include_excluded)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "graph.json"), "w") as fh:
        json.dump(elements, fh, indent=2, default=str)
    with open(os.path.join(out_dir, "vocab.json"), "w") as fh:
        json.dump(vocab_json(vocab), fh, indent=2)
    excluded = sum(1 for c in glob.glob(os.path.join(root, "cases", "*.y*ml"))
                   for e in (_load(c).get("edges", []) or [])
                   if (vocab.claim_modes.get(e.get("claim")) or None)
                   and vocab.claim_modes[e["claim"]].excluded_from_default)
    print(f"built {len(elements['nodes'])} nodes, {len(elements['edges'])} edges "
          f"from {len(elements['cases'])} case(s) -> {out_dir}")
    if excluded and not include_excluded:
        print(f"note: {excluded} excluded-mode edge(s) hidden from default output.")
    return 0
