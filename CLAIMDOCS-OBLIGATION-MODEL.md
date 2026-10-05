# Proposed obligation semantics

**Design only.** Obligations fit naturally beside ClaimDocs claims/evidence as a separate typed object. They do not fit as another claim mode: `wired` is not `SATISFIED`, `candidate` is not backlog, and human admission of a relation is not closure of consequential work. This proposal introduces no runtime implementation or tracker authority.

## Identity and evidence

An owner-reviewed obligation carries stable identity, origin incident/campaign/claim/evidence, unfinished statement, affected domain/subjects, consequence, owner/project, authoritative tracker reference, semantic state, prerequisites/blockers, forcing conditions, closure criteria/evidence, explicit supersession/retirement and last meaningful review. Preserve versions and decisions; repository/branch moves change locators, not identity. Evidence needs exact identity/custody, source generation and scope; a hash identifies bytes, not authenticity or adequacy.

Three orthogonal axes must remain visible: **claim support**, **obligation semantic state**, and **external execution workflow**. Evidence age/applicability and coverage are additional qualifiers. A supported operational claim can coexist with unfinished improvement work. The design must not reduce these axes to one green status.

## Lifecycle

| State | Required meaning |
|---|---|
| `OPEN` | Consequential unfinished promise with identified owner/scope |
| `BLOCKED` | Named prerequisite prevents progress; retains the promise |
| `DEFERRED` | Explicit delay with rationale and revisit condition/horizon |
| `IN_PROGRESS` | Authoritative execution observation supports active work; no completion implied |
| `SATISFIED` | Exact closure criteria met by accepted evidence and attributable disposition |
| `SUPERSEDED` | Explicit successor/decision covers the residual promise; history retained |
| `RETIRED` | Owner explicitly withdraws obligation with rationale and accepted consequence |

Reopening/narrowing requires an attributable decision, not overwriting history. `SUPERSEDED` must name a valid successor or explicit replacement decision; reject cycles, dangling targets and duplicate stable IDs. Multiple active descendants of the same transferred scope are a visible conflict until reconciled. Distinct residual obligations may legitimately remain active; do not suppress them through a similarity heuristic.

Tracker closed + missing closure evidence yields an unresolved semantic obligation and projection mismatch. Missing evidence is unknown/unsupported, not false. An unavailable tracker does not retire an entry. A new claim of general health does not replace older stronger/narrower evidence or satisfy the obligation. Evidence conflicts require explicit reconciliation; recency alone is not ordering authority.

## Completeness and relevance

Enumeration accepts explicit subject/domain scope and an owner-declared finite source/inventory snapshot. Return every unresolved covered entry, including old blocked/deferred work, deterministic ordering and a coverage receipt: scope/version/time, included sources, expected vs loaded identities, unavailable/stale inputs and completion/pagination state. Invalid/duplicate/missing inventory entries must prevent a false complete/empty result. No promise of global completeness beyond enrolled sources; no semantic ranking or default-hidden modes may remove unresolved entries.

Forcing conditions are explicit predicates/review rules over named evidence contracts with required freshness, threshold/units and a match/nonmatch/unknown witness. Natural-language debt may need owner review rather than a invented machine predicate. A matched review condition does not admit a specific migration, grant effect authority or move work automatically to `IN_PROGRESS`. Keep the current state and **review due** separate. Ticket age alone does not page. Constellation's existing observation/evaluation owner evaluates runtime evidence; ClaimDocs preserves the rule, witness and consequence.

## Tracker and cache boundary

An authoritative tracker owns people, priority and sequencing. Start with reference + dated one-way imported projection; owner-authored obligation semantics own origin/closure and retain disagreements. Do not synchronize edits both ways. Imported status is an observation with source/time, never semantic satisfaction by fiat. The portable corpus contains no tracker token.

Continuity can cache explanations and bootstrap context. A missed cache entry cannot alter enumeration, closure or history. Future lane/incident/deployment hooks must invoke the bounded state projection as part of their enrolled workflow rather than opt-in recollection. No such automatic hook ships today.

## Minimal closure receipt and scope limits

A terminal decision binds obligation identity/version, disposition, exact closure/successor/retirement basis, reviewer/owner, time and scope. Retain the pre-decision obligation and origin evidence in immutable portable history; do not require the originating branch to survive. Unknown custody or unmet residual criteria refuse satisfaction. A completed review satisfies only a review obligation, not the implementation promise it considered.

Before implementation, model these transitions and incomplete-enumeration outputs with shared vectors. The owner/adequacy decision is an assumption, not cryptographic proof or automated truth. Current ClaimDocs cited-body checks cannot establish operational evidence currentness or full semantic support closure; proposed fields do not acquire those guarantees merely by existing.
