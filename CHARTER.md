# claimdocs charter

The founding constraints. Short on purpose. The README explains; this governs.

```
claimdocs is a receipt-gated documentation system.

It admits typed documentation claims only with declared basis.
It renders admitted claims without strengthening their mode.
It may expose gaps, stale edges, contradictions, and speculative regions.
It does not authorize architecture, discharge implementation claims,
  or convert prose into proof.
```

## The line that keeps the tool from laundering itself

> A resolved receipt witnesses that the cited basis **exists** at the checked revision,
> and (for hashable bases) that it is **unchanged** since admission. It does **not**
> witness that the basis **establishes** the edge. Edge adequacy is a human admission,
> recorded separately, and is not re-checked — unless the basis kind has a specific
> mechanical verifier for the claimed relation.

This exists because the first version of this idea overclaimed. Its verifier resolved a
symbol and called the edge "verified." But *symbol-resolves is not relation-holds*:
rename a symbol and resolution screams; **hollow** a function's body to `assert True` and
resolution stays green while the edge it backs goes false. That is "signed is not
witnessed" reappearing one level up, inside the tool built to refuse it.

So claimdocs separates the layers and never conflates them:

| Layer | Question | Mechanical? | Where |
|---|---|---|---|
| **existence** | does the cited path/symbol still resolve? | yes | `verify-basis` |
| **freshness (cited body)** | is the cited symbol's **own body** unchanged since admission? | yes (hashable bases) | `verify-basis` (`body_sha256`) |
| **freshness (closure)** | are the basis's callees / fixtures / deps unchanged? | reserved — see *Transitive drift* | not built |
| **execution** | does the cited test/probe pass? | yes | reserved — not built (plugin seam) |
| **adequacy** | does this basis actually establish this edge? | **no** | a human admission on the edge |
| **admission** | under what mode may this edge render? | human/policy | the claim mode |

`verify-basis` reports each honest layer and says, out loud, what it proves and what it
does not. It proves **cited-body** existence and freshness — not closure freshness, not
adequacy. So the report word is `cited_body_fresh`, never a bare `fresh`: a function is not
its bytes when its bytes call out. Freshness narrows the *cited-body* hollow-test gap; it
does not touch transitive drift (below), and re-admission cannot close that gap while its
trigger is a cited-body-hash delta — because the delta never fires.

## Freshness scope — transitive drift

Freshness is presently freshness of the **cited basis artifact**, not freshness of the
full semantic support closure. A cited function, theorem, test, or document may remain
byte-fresh while a callee, fixture, dependency, dataset, or external assumption changes
underneath it. claimdocs treats this as **transitive drift**: fresh cited bytes do not
imply the basis still establishes the edge.

```
fresh cited bytes ≠ still-establishing claim
```

Concretely: a cited test body is unchanged, but the helper it calls gets hollowed to
`return True`. The cited symbol is byte-identical, so freshness stays green; execution
isn't built; and adequacy re-admission is *triggered by* `body_sha256` deltas, which don't
fire — so the human is never summoned. The backstop inherits the front line's blind spot.

So the honest doctrine stack is:

```
Resolved      ⊬ supported      (a symbol resolving is not the relation holding)
Cited-fresh   ⊬ closure-fresh  (unchanged bytes are not an unchanged support closure)
Closure-fresh ⊬ adequate       (an unchanged closure is not a sufficient one)
Rendered      ⊬ true           (a drawn edge is not a fact)
```

claimdocs catches **basis disappearance and cited-body hollowing**. It does **not** catch
helper/callee/fixture hollowing — that is transitive drift, named here, not built.

## spec_is_not_wired

A *witnessing* mode (one with `witnesses: true` in `claimdocs.yml`) must cite at least
one basis of a `witnessing_basis_kind`. A doc/spec proposes an edge; it does not witness
one. An edge backed only by a spec is downgraded — the engine refuses to let a stub file's
mere existence become a wiring claim. This is the portable form of the rule; a case may
name it whatever its vocabulary calls the strong mode.

## No mode upgrade in rendering

> Pages explain the graph. They do not outrank it.

Every readout — graph, table, report, and (reserved) manpages — preserves claim mode.
The renderer uses **mode-preserving wording** so prose cannot quietly promote a claim:

```
wired / documented  -> "is witnessed as"
specified           -> "is specified as"
derived / inferred  -> "is derived from"
candidate           -> "is a candidate relation"
deprecated          -> "was formerly"
contradicted        -> "is disputed by"
```

A `specified` edge may not be described as "implemented." A `candidate` edge may not be
called "planned" without an authorizing basis. A `derived` edge must show its parents.

## The artifact is the graph, not the site

`cases/` + `receipts/` is the source of truth. Generated output (`docs/`) is a readout.
Delete it and re-render — nothing of value is lost. A diagram that can't cite its basis is
folklore with an SVG export; this one fails closed instead.

## Reserved — named, not built

Per name-early / ratify-lazily: these are recorded so the retrofit cost is visible, not
authorized. Build each only when a case forces it.

- **The page layer (manpage readouts).** The next readout: authored Markdown pages with
  `{{ edge(id) }}` / `{{ node(id) }}` embeds whose facts are imported from the graph, and
  generated per-entity pages in a BSD-manpage skeleton (`NAME / CLAIM STATUS / DESCRIPTION
  / RECEIPTS / FAILURE MODES / NON-CLAIMS / SEE ALSO`). The load-bearing addition is the
  **NON-CLAIMS** section — the anti-laundering block ordinary manpages lack. Page-linter
  rules: embeds must resolve; a page may cap allowed modes; an embedded stale/changed
  basis makes the page stale; a default-hidden mode must be labeled. *Already dogfooded at
  the graph layer:* the edge panel renders a per-edge "Does not claim" line off the mode.
  The manpage layer is the same field in a different decoder. Do not build the Jinja engine
  before the graph layer is solid and a case asks for prose.
- **Re-admission ceremony (the next mutating surface).** Body hashes change for harmless
  reasons (a refactor that preserves the relation), so stale detection needs a deliberate
  re-admit, or it becomes noise that gets bypassed — the raccoon attacks through ergonomics.
  Doctrine: *`claimdocs admit` does not make a claim true; it records that a reviewer
  accepts a basis as adequate for an edge at a specific revision and body hash.* Shape:
  `claimdocs admit <edge> --basis <id> --reviewed-at HEAD --reason "..."`, requiring a
  clean tree or explicit override (do not admit against soup). Writes `adequacy.status /
  admitted_by / admitted_at_sha / basis_body_sha256 / rationale`. `admitted_by` is a plain
  string for now — do not summon the signature goblin yet. This is a *mutating governance
  operation inside the doc engine* and gets its own pass, not a bolt-on. **Its trigger
  cannot be a cited-body-hash delta alone** — that delta is blind to transitive drift, so a
  ceremony keyed on it is never summoned when a helper gets hollowed (it inherits the
  freshness blind spot). The trigger must eventually include closure deltas (below).
- **Normalized freshness hash (ergonomic, design only).** Raw `body_sha256` false-positives
  on a `ruff format` pass — every hashable basis invalidates at once for zero semantic
  change, demanding a mass re-admit (friction that gets deferred). Fix: split the receipt
  into `raw_body_sha256` (forensic, exact bytes) and a `normalized_body_sha256` (the
  freshness trigger) computed over an AST dump with location metadata stripped. Then
  reformatting moves `raw` but not `normalized`, while `assert True` moves both. This is
  *not* an adequacy probe — it only lowers false-positive churn. Build against the settled
  freshness-scope model, not in isolation.
- **Declared-closure freshness (`depends_on`, the middle rung).** The cheap, honest,
  non-inferred answer to transitive drift: a basis may declare `depends_on: [{path, symbol},
  …]`, and `verify-basis` hashes those *explicitly declared* dependencies and reports a
  `closure` status alongside `cited_body`. The author declares what the basis rests on;
  claimdocs checks whether the declared closure moved. Conservative (misses undeclared
  deps), but it gives a real `closure: fresh|changed|unchecked` instead of one smug `fresh`.
  **Do not build inferred call graphs** — transitive-closure hashing is expensive,
  approximate, and blind to dynamic dispatch; that is a later/plugin goblin, distinct from
  this declared rung.
- **`deprecated` / `contradicted` modes.** Tombstones. `deprecated` (was true, retired)
  has obvious demand; `contradicted` (an edge refuted by a stronger basis elsewhere) needs
  conflicting-claim machinery and no case yet.
- **Basis `execution` and structural probes.** Running a cited test, or an AST/mutation
  probe that checks the *relation* (not just the symbol). A passing test named
  `test_X_delegates` proves something passed, not that X delegates — so execution narrows
  adequacy, it does not close it. Plugin seam, not core.
- **Language/source plugins.** Python symbol resolution is the one built-in resolver. Other
  languages, `lake build`, URL receipts, git-sha pinning are a plugin seam (`basis_kinds`
  carries `resolvable`); the seam is designed, the plugins are not built.
