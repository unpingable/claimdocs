# claimdocs

**Write documentation claims as data. Refuse to render strong claims without declared
basis. Docs that fail closed.**

Most docs are text artifacts: someone writes prose, someone draws boxes, everyone slowly
lies by accident, and six months later the diagram is folklore with an SVG export.
claimdocs treats docs as **claims under custody** — every edge in your system graph
carries exactly one *claim mode* and cites a *basis*, and the linter refuses to render a
strong claim whose basis it cannot resolve.

The corporate move ("point an LLM at the repo, generate docs") produces plausible mulch.
The admissible move:

```
human or LLM proposes nodes / edges, marking weak ones as specified / candidate
  -> linter REJECTS any witnessing-mode edge that doesn't cite resolvable basis
  -> a human admits adequacy (does this basis actually support this edge?) at a pinned sha
  -> the site renders from the admitted graph, preserving claim mode
```

The model may propose the skeleton. It may not certify its own proposals as architecture.

## Two promises, kept separate

claimdocs verifies declared **bases**, not truth itself.

1. **Existence + cited-body freshness (mechanical).** `verify-basis` resolves a cited
   `file + symbol` against a source tree and confirms its **own body** is unchanged since
   admission. Rename a symbol and it screams; *hollow that symbol's body* to `assert True`
   and it screams too — the body hash moved. The honest limit: it catches basis
   disappearance and *cited-body* hollowing, **not** a hollowed *helper the basis calls*
   (different symbol, byte-identical cited body). That is transitive drift — `cited-fresh ≠
   closure-fresh` — named in the CHARTER, not built.
2. **Adequacy (human).** Whether a resolved basis actually *establishes* an edge is an
   admission, recorded on the edge with the reviewed sha. claimdocs surfaces it, pins its
   freshness, and **never claims to have proven it.** `resolved ≠ supported`. See
   [CHARTER.md](CHARTER.md).

## The vocabulary is yours

claimdocs core knows `node / edge / claim_mode / basis / adequacy / freshness` and nothing
else. Your project's `claimdocs.yml` declares the claim modes, node/edge kinds, basis
kinds, lanes, and colors. The engine never learns your domain's words.

```yaml
default_modes: [documented]
witnessing_basis_kinds: [code, test, receipt_hash]
claim_modes:
  documented: { color: "#4fc3f7", witnesses: true, help: "witnessed in running code" }
  specified:  { color: "#f5a623", style: dashed,   help: "named in a spec; not witnessed" }
  derived:    { color: "#c08bff", requires_derivation: true }
  candidate:  { excluded_from_default: true, max_per_case: 2 }
node_kinds: { module: {...}, gate: {...}, store: {...}, external: {...} }
edge_kinds: { calls: {...}, gates: { refusal_required: true }, requests: {...} }
```

## Use

```bash
pip install -e .                       # or: PYTHONPATH=src python -m claimdocs ...
claimdocs init                         # scaffold claimdocs.yml + cases/ + receipts/
claimdocs lint                         # citation-shape validation
claimdocs verify-basis --repo .        # resolve code/test bases + freshness against a tree
claimdocs report                       # the fail-closed instrument panel (mode/adequacy)
claimdocs render                       # emit docs/data/{graph,vocab}.json + the site
claimdocs serve                        # serve docs/ at localhost:8000
```

`--repo NAME=PATH` binds a named source tree (receipts carry a `repo:` field).

## Layout

```
claimdocs.yml          # your vocabulary pack — the ONLY domain-specific file the engine reads
cases/<case>.yaml      # nodes + edges
receipts/<id>.yaml     # one basis per file, shared across edges
docs/                  # generated readout (graph + vocab json + cytoscape site)

src/claimdocs/
  config.py            # load claimdocs.yml -> Vocabulary (the AG-firewall)
  verify.py            # basis resolution + Python symbol body-hash (existence + freshness)
  linter.py            # the gate: citation-shape + basis resolution, fully config-driven
  builder.py           # render the admitted graph to graph.json + vocab.json
  cli.py               # lint / verify-basis / render / report / serve / init
  renderer/            # generic, config-driven site (reads vocab.json; zero hardcoded vocab)
```

## First serious specimen

[**governor-atlas**](../governor-atlas) — the Agent Governor architecture and its
constellation seams, as a claimdocs case. AG's whole thesis is "language is a proposal,
not an authority"; claimdocs is that thesis pointed at AG's own documentation. The
specimen proves the engine is serious; it must not contaminate the primitive (claimdocs
knows nothing about "standing" or "spend walls").

Apache 2.0.
