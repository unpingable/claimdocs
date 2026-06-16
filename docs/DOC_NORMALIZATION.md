# Doc normalization (reserved design — NOT built)

A **later** surface, recorded now so the retrofit cost is visible. Sequenced *after* the
re-admission ceremony (see CHARTER §reserved) — normalization depends on it (below). This
is the law; there is no `doc_normalize.py` yet, on purpose.

The act is **mode-preserving documentary recomposition**, not "documentation improvement."
The latter is how a model starts writing architecture fanfic. Normalization may restructure
prose; it may not create authority.

```
Normalized(doc) ⊬ Strengthened(doc)
```

It is the same knife as everything else in claimdocs, at the prose layer:
`resolved ⊬ supported`, `signed ⊬ witnessed`, `rendered ⊬ true` — now `normalized ⊬ stronger`.

## The invariant

> Normalization may change form. It may not promote claim mode.

If old prose says *"AG uses Standing for spendability checks"* but the graph says that seam
is only `specified`, the normalized doc must say *"AG has a **specified** Standing
spendability seam"* — not "uses," "integrates with," or "depends on." Those are laundering
verbs.

## Where the teeth actually are (polarity matters)

The gate is **allowlist-shaped**, not a verb-blocklist:

> A strong architectural sentence is admissible only if it cites an admitted claim ID of
> sufficient mode. No citation, or insufficient mode → refuse or downgrade.

The laundering-verb list (`uses / integrates with / depends on / talks to / calls` applied
to a non-`wired` seam) is **testimony, not authority** — a heuristic that surfaces suspects
for review. It has graded coverage; you will always miss a phrasing. So it may *flag*, it
may not *admit*. Authority comes from the claim-ID-and-mode requirement. A blocklist over
English guarding an authority transition is the boundary drawn wrong (see zoning doctrine,
allowlist-vs-blocklist).

## Refusal set (the law is the refusals, not the writer)

```
1. prose upgrades candidate/specified/derived into wired (or any mode → stronger)
2. a strong architectural sentence cites no admitted claim ID    ← the allowlist gate
3. cited basis resolves but its adequacy is stale (body changed since admission)
4. claim references a vanished node/edge
5. a page embeds a claim mode its frontmatter disallows
6. a constellation seam is described as live-wired without a wired basis
7. the generated graph/table contradicts the authored prose
8. NON-CLAIMS section missing on a page with authority-upgrade risk
```

That is doc-lint with semantic teeth. The output is a **patch proposal, never a silent
mutation**, plus a receipt.

## Why re-admission must ship first

Refusal #3 keys on stale adequacy. Stale adequacy is only *resolvable* via the re-admission
ceremony — without it, normalization either ignores #3 (loses a refusal) or blocks on a
state nothing can clear. So: re-admission, then normalization. The dependency is real, not
ordering by taste.

## Receipt (generic — AG is a consumer, not the namespace)

```json
{
  "kind": "claimdocs.doc_normalization.v1",
  "source_docs": [{ "path": "...", "hash": "..." }],
  "target_docs": ["docs/man/..."],
  "graph_sha": "...",
  "policy_version": "...",
  "claims_extracted": 42,
  "claims_admitted": 19,
  "claims_rewritten": 13,
  "claims_refused": 10,
  "refusals": [{ "rule": 1, "span": "...", "found": "uses", "graph_mode": "specified" }]
}
```

## Four stages (when built)

1. **Intake** — source doc path + hash, target doc class, target case, graph sha, policy version.
2. **Claim extraction** — propose extracted claims, *every one starting weak* (`status:
   proposed`). Extraction is testimony, not admission. Each carries `source_span` +
   `referenced_claims`.
3. **Admission** — per claim, emit one of: `admit_as_written` / `rewrite_mode_preserving` /
   `downgrade_to_specified` / `move_to_candidate_page` / `move_to_non_claims` /
   `refuse_unsupported` / `delete_as_obsolete`.
4. **Propose patch** — write target pages (manpage shape, see `MANPAGE_STANDARD.md`) +
   emit the receipt. **No auto-apply.**

## First consuming slice (in governor-atlas, when thawed)

Don't normalize everything. One ugly-but-contained target: the **standing-spendability gate
chain** — it has real `wired` basis *and* known constellation caveats, so it exercises both
the admit path and the downgrade path. Build only:

```
doc_normalize --check <doc>          # report refusals, no output
doc_normalize --emit-proposal <doc>  # propose patch + receipt, no apply
```

Acceptance test (this is the test that matters, not whether the manpage is pretty):

> Given prose that says "AG uses Standing live", and claimdocs says only "specified seam",
> the normalizer rewrites it mode-preserving or refuses.

Target pages: `docs/man/ag-standing-spendability-gate.7.md`, `ag-origin-fence.7.md`,
`ag-recomposition-receipt.5.md`, `ag-constellation.7.md`.

---

> DocNormalization may change form. It may not create authority.
> The raccoon may format. The raccoon may not promote.
