# Next — claimdocs (the engine)

Prioritized. Each item names its gate; nothing jumps its dependency.

## 1. Re-admission ceremony — the next mutating surface
The immediate next build. `claimdocs admit <edge> --basis <id> --reviewed-at HEAD
--reason "..."` — records that a reviewer accepts a basis as adequate at a revision +
body hash; requires a clean tree (don't admit against soup). Writes `adequacy.status /
admitted_by / admitted_at_sha / basis_body_sha256 / rationale`. Doctrine already in
`CHARTER.md` §reserved. Without it, `BASIS_BODY_CHANGED` is either noise or gets bypassed —
the raccoon attacks through ergonomics. **Blocks on: nothing. This is next.**

## 2. Doc normalization — mode-preserving recomposition
Design recorded in `docs/DOC_NORMALIZATION.md`. The `--check` / `--emit-proposal`
prose-recomposition pass. **Blocks on: re-admission** (refusal rule #3, stale adequacy, is
unactionable without a ceremony to clear it).

## 3. The page / manpage renderer
Law written in `docs/MANPAGE_STANDARD.md`; renderer deliberately unbuilt. **Blocks on: a
case actually asking for prose** (don't build the Jinja engine on spec).

## Lower priority / opportunistic
- **Packaging.** Console entry point + editable install verified in a clean venv. Publish
  to PyPI (or settle a git-install story) when there's an external consumer.
- **Plugin seam, not plugins.** The Python symbol resolver is built in; `basis_kinds`
  carries `resolvable`. Design — don't build — the seam for other languages, `lake build`,
  URL receipts, git-sha pinning. Build a resolver only when a case needs that basis kind.
- **`deprecated` then `contradicted` modes.** Tombstones (canonical spine already reserves
  the names). `deprecated` (retired edges) has demand; `contradicted` needs
  conflicting-claim machinery and no case yet.
- **`examples/stale-basis-demo/`.** A *labeled* failing specimen so stale detection has a
  teaching home without a red mark in the green genericity proof (`toy-webapp`).

## The standing invariant for all of the above
Every new verb still ends in "…but may not promote." `resolved ⊬ supported`,
`rendered ⊬ true`, `normalized ⊬ stronger`. Nothing earns authority by existing.
