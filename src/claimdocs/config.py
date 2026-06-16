"""claimdocs configuration — the vocabulary pack.

claimdocs core knows `node / edge / claim_mode / basis / adequacy / freshness`.
It knows NOTHING about any particular system. Everything domain-specific — the names
of your claim modes, node kinds, edge kinds, basis kinds, the lane layout, the colors —
lives in a project's `claimdocs.yml` and is loaded here. The first serious specimen
(governor-atlas) must not contaminate the primitive; this module is the firewall.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("claimdocs requires PyYAML (pip install pyyaml)") from exc

CONFIG_NAME = "claimdocs.yml"

# The canonical mode spine. The core speaks these boring, portable nouns; a project may
# name its modes whatever its dialect wants and alias them here (AG says `wired`, the
# spine says `documented`). The `wording` is the mode-preserving phrase a readout MUST use
# so prose cannot quietly upgrade a claim. Semantics flags (witnesses/derivation) stay
# explicit in each project's config — the spine only normalizes naming + wording.
CANONICAL_MODES = {
    "documented":   {"wording": "is witnessed as"},
    "specified":    {"wording": "is specified as"},
    "derived":      {"wording": "is derived from"},
    "candidate":    {"wording": "is a candidate relation"},
    "deprecated":   {"wording": "was formerly"},
    "contradicted": {"wording": "is disputed by"},
}


@dataclass(frozen=True)
class ClaimMode:
    name: str
    color: str = "#888888"
    style: str = "solid"            # solid | dashed | dotted
    witnesses: bool = False         # does this mode assert "witnessed in the live system"?
    requires_derivation: bool = False
    excluded_from_default: bool = False
    max_per_case: int | None = None
    help: str = ""
    canonical: str | None = None    # which CANONICAL_MODES spine member this aliases
    wording: str = ""               # mode-preserving phrase; derived from canonical if unset


@dataclass(frozen=True)
class NodeKind:
    name: str
    color: str = "#888888"
    lane: str = "logic"
    label: str = ""
    shape: str = "round-rectangle"
    what: str = ""
    why: str = ""


@dataclass(frozen=True)
class EdgeKind:
    name: str
    role: str = "flow"              # flow | gate | emit | request | derive
    verb: str = ""
    refusal_required: bool = False  # must carry a refusal block (authority boundary)


@dataclass(frozen=True)
class BasisKind:
    name: str
    resolvable: bool = False        # can a verifier resolve this against a source tree?
    executable: bool = False        # (reserved) can it be run? not built yet — see CHARTER
    help: str = ""


@dataclass(frozen=True)
class Vocabulary:
    project: str
    title: str
    claim_modes: dict[str, ClaimMode]
    node_kinds: dict[str, NodeKind]
    edge_kinds: dict[str, EdgeKind]
    basis_kinds: dict[str, BasisKind]
    lanes: list[str]
    witnessing_basis_kinds: set[str]   # basis kinds that satisfy a witnessing mode
    default_modes: set[str]            # modes shown in the default render
    staleness_days: int = 365

    # --- derived convenience views -----------------------------------------
    @property
    def witnessing_modes(self) -> set[str]:
        return {m.name for m in self.claim_modes.values() if m.witnesses}

    @property
    def derivation_modes(self) -> set[str]:
        return {m.name for m in self.claim_modes.values() if m.requires_derivation}

    @property
    def refusal_edge_kinds(self) -> set[str]:
        return {e.name for e in self.edge_kinds.values() if e.refusal_required}

    @property
    def lane_index(self) -> dict[str, int]:
        return {lane: i for i, lane in enumerate(self.lanes)}


def find_config(start: str) -> str:
    """Walk up from `start` to find a claimdocs.yml."""
    cur = os.path.abspath(start)
    while True:
        candidate = os.path.join(cur, CONFIG_NAME)
        if os.path.isfile(candidate):
            return candidate
        parent = os.path.dirname(cur)
        if parent == cur:
            raise FileNotFoundError(f"no {CONFIG_NAME} found at or above {start}")
        cur = parent


def load_vocabulary(config_path: str) -> Vocabulary:
    with open(config_path) as fh:
        raw = yaml.safe_load(fh) or {}

    modes = {}
    for name, d in (raw.get("claim_modes") or {}).items():
        d = d or {}
        canonical = d.get("canonical") or (name if name in CANONICAL_MODES else None)
        wording = d.get("wording") or (CANONICAL_MODES.get(canonical, {}).get("wording", "")
                                       if canonical else f"({name})")
        modes[name] = ClaimMode(
            name=name, color=d.get("color", "#888888"), style=d.get("style", "solid"),
            witnesses=bool(d.get("witnesses", False)),
            requires_derivation=bool(d.get("requires_derivation", False)),
            excluded_from_default=bool(d.get("excluded_from_default", False)),
            max_per_case=d.get("max_per_case"), help=d.get("help", ""),
            canonical=canonical, wording=wording,
        )

    nodes = {}
    for name, d in (raw.get("node_kinds") or {}).items():
        d = d or {}
        nodes[name] = NodeKind(
            name=name, color=d.get("color", "#888888"), lane=d.get("lane", "logic"),
            label=d.get("label", name.title()), shape=d.get("shape", "round-rectangle"),
            what=d.get("what", ""), why=d.get("why", ""),
        )

    edges = {}
    for name, d in (raw.get("edge_kinds") or {}).items():
        d = d or {}
        edges[name] = EdgeKind(
            name=name, role=d.get("role", "flow"), verb=d.get("verb", name.replace("_", " ")),
            refusal_required=bool(d.get("refusal_required", False)),
        )

    bases = {}
    for name, d in (raw.get("basis_kinds") or {}).items():
        d = d or {}
        bases[name] = BasisKind(
            name=name, resolvable=bool(d.get("resolvable", False)),
            executable=bool(d.get("executable", False)), help=d.get("help", ""),
        )

    default_modes = set(raw.get("default_modes") or
                        [m.name for m in modes.values() if not m.excluded_from_default])
    witnessing_basis = set(raw.get("witnessing_basis_kinds") or [])

    return Vocabulary(
        project=raw.get("project", "claimdocs-project"),
        title=raw.get("title", raw.get("project", "claimdocs")),
        claim_modes=modes, node_kinds=nodes, edge_kinds=edges, basis_kinds=bases,
        lanes=list(raw.get("lanes") or ["logic"]),
        witnessing_basis_kinds=witnessing_basis,
        default_modes=default_modes,
        staleness_days=int(raw.get("staleness_days", 365)),
    )
