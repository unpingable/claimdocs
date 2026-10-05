# ClaimDocs current state — 2026-10-05

This inventory distinguishes implemented behavior from reserved design. The canonical public repository is [unpingable/claimdocs](https://github.com/unpingable/claimdocs), repository root, branch `main`. Published source inspected: `8d21b8a352f98c4f681f7b53fc407c5c2840d8d1`. The initially inspected clean local `main` was `c95ea82a43aa01e8b557d45fab300642360ef9cc`, one documentation commit behind; it was fast-forwarded before adding this assessment. Engine and test bytes are identical across those revisions. This assessment does not select a new runtime generation.

GitHub readback found one branch, no tags/releases/issues, no Pages deployment and an unarchived public repository. No local-only engine implementation was found. One stale detached-worktree registration is a custody/cleanup observation, not evidence of another live engine. No operational service deployment or published binary/package registry distribution was established.

## Actual implementation

Python >=3.10, package `claimdocs` version `0.0.1`, PyYAML >=6.0, setuptools build backend, Apache-2.0 LICENSE plus NOTICE/PROVENANCE. Core modules are `config.py`, `linter.py`, `verify.py`, `builder.py` and `cli.py`; the UI is generated static HTML/JS/JSON. Core imports no model provider, Constellation runtime, AG vocabulary or tracker client.

Authored data is `claimdocs.yml` vocabulary, `cases/*.yaml` typed nodes/edges and `receipts/*.yaml` declared bases. Generated `docs/` is a readout, not authoritative source. There is no versioned normative portable schema or obligation object. Six implemented verbs are `init`, `lint`, `verify-basis`, `report`, `render`, `serve`; `--project` and `--today` precede the verb, while `verify-basis --repo` follows it. See [HOWTO](HOWTO.md).

| Surface | Implemented | Important boundary |
|---|---|---|
| Vocabulary/lint | Configured modes, node/edge/basis types, references, witnessing basis kinds, refusal shapes, derivation depth and adequacy shape | Citation shape does not prove the claimed relation |
| Verification | Local path/symbol resolution, Python cited-body hash comparison, optional source-repository bindings | No execution, dependency closure, source-checkout SHA attestation or adequacy proof; unsupported symbols may use substring matching |
| Retrieval age | Warning beyond configured age, explicit inspection date | Receipt age is not operational currentness/boot identity; warning is not a publication prohibition |
| Human adequacy | Recorded `status: admitted` and `admitted_at`, enforced by strict lint/verify | Reviewer identity/revision applicability are not authenticated; admission ceremony is unbuilt |
| Render | Shape lint, recorded mode preservation, graph/vocabulary JSON and static renderer | Does not run verification or strict adequacy, or carry their result into the graph |
| Report | Declared edges, mode, receipt count and recorded adequacy | Does not validate independently; not current truth or complete obligation enumeration |
| Serve | Ordinary Python HTTP server | Binds all interfaces despite localhost wording; not a qualified production service |

The graph UI uses Cytoscape 3.30.2 from a CDN. CLI/JSON operation does not need it; a self-contained offline UI is not presently established.

## Named consumers and historical material

The generic `examples/toy-webapp` exercises non-AG configuration. The serious specimen is [governor-atlas](https://github.com/unpingable/governor-atlas): vocabulary, cases, receipts and generated readout. Its published `main` inspected was `11a7f00eb76eeb0892311da19cd4a82ce017773a`; local source was `7ec649db24b98b6c50f9804d000994116f47b1a6`. Current published documentation identifies its Classic Python AG case as historical and the newer Constellation AG as successor. Atlas CI parses YAML only; no engine verification/publication gate or Pages deployment was established. Retaining a historical specimen does not create a current Classic runtime obligation.

Cartography has proposed ClaimDocs reuse and a separate design-only semantic registry/custom validator. No current ClaimDocs import/configuration was found there. Canonical Constellation spine runtime manifests and imports contain no ClaimDocs dependency. Public users must not inherit the private corpus or tracker conventions to use this generic engine.

[CHARTER](CHARTER.md), `NEXT.md`, doc-normalization and manpage plans reserve admission, declared dependency-closure freshness, normalized hashes, execution/language plugins, authored page embeds, richer tombstones and corpus query behavior. They are not implemented. The reserved `admitted_at_sha` sketch differs from actual `admitted_at`; a future repair must reconcile this without pretending the sketch ships. The older governed corpus-query reservation is not an implemented policy and needs an explicit bounded decision before adding ordinary owner-scoped obligation enumeration.

## Checks and demonstrated limits

Existing local Python/PyYAML, no dependency installation, provider or service launch:

- Standalone engine checks, toy verification and local atlas shape lint passed within their documented scope.
- Toy verification resolved four cited bodies and three recorded admissions; fixed-input/date rendering repeated the same graph/vocabulary bytes.
- Deleted cited source: `verify-basis` refused; independent `render` still succeeded.
- Removed adequacy: strict lint refused; independent `render` still succeeded.
- Phase-J controls found duplicate receipt IDs silently replace a prior basis by file ordering, duplicate edge IDs render twice, `supersedes` is ignored and an unavailable admission revision label still verifies cited bytes.

These are limits of the current command composition/identity model, not a claim that ordinary rendering proves freshness. Obligation lifecycle, complete unresolved enumeration, tracker closure, forcing predicates, automatic startup projection and current/historical supersession have no implementation. [Assessment](CLAIMDOCS-PUBLIC-BETA-ASSESSMENT.md) and [proposed beta slice](CLAIMDOCS-BETA-SLICE.md) keep those gaps explicit.

Exact isolated test inputs, logs, source hashes and immutable scout notices are retained in the owning architecture-spike custody. Public docs use source identities and generic findings rather than private artifact locators. No product integration, runtime repair or new deployment occurred.
