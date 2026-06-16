# Provenance

This project is human-directed and AI-assisted. Final design authority,
acceptance criteria, and editorial control rest with the human author.
AI contributions were material and are categorized below by function.

## Human authorship

The author defined the project direction, requirements, and design intent.
The core recognition — *documentation as a typed claim graph where every edge
must carry admissible basis* — is the author's, applied here as the first
generic instance of a pattern also expressed in sibling atlas projects. AI
systems contributed proposals, drafts, implementation, and critique under
author supervision; they did not independently determine project goals or
deployment decisions. The author reviewed, revised, or rejected AI-generated
output throughout development.

## AI-assisted collaboration

### Architecture, constraint model, and adversarial critique

Lead collaboration: ChatGPT (OpenAI). Drove the engine/case split (a generic
`claimdocs` core vs. `governor-atlas` as first specimen), the canonical claim-mode
spine with per-project aliases, the mode-preserving rendering rule, the manpage
readout standard, and the doc-normalization design — including the framing that
kept the tool from becoming "documentation generation" rather than receipt-gated
admission.

### Implementation, tests, and integration

Lead collaboration: Claude (Anthropic) via Claude Code. Heavy contributions to
source code (config/linter/verifier/builder/CLI/renderer), the test suites,
the body-hash freshness mechanism, the toy genericity witness, and build
configuration, including assembly of architectural decisions into working code
and the reflexive discipline of verifying claims against the live tree.

### Validation and adversarial review

A separate Claude (Anthropic) session served as adversarial reviewer and found
the load-bearing flaw: that resolving a cited symbol witnesses its *existence*,
not its *adequacy* — the "hollow-test" infection vector. That critique produced
the `resolved ⊬ supported` correction and the existence/freshness/adequacy split
now central to the engine.

## Provenance basis and limits

This document is a functional attribution record based on commit history,
co-author trailers (where present), project notes, and documented working
sessions. It is not a complete forensic account of all contributions.

Some AI contributions (especially design critique, rejected alternatives,
and footguns avoided) may not appear in repository artifacts or commit
metadata.

Model names/tools are recorded at the platform level (e.g., ChatGPT,
Claude Code); exact model versions may vary across sessions and are not
exhaustively reconstructed here.

## What this document does not claim

- No exact proportional attribution. Contributions are categorized by
  function, not quantified by token count or lines of code.
- Design and implementation were not cleanly sequential. Architecture
  informed code, code revealed design gaps, and the feedback loop was
  continuous.
- "Footguns avoided" and "ideas that didn't ship" are real contributions
  that leave no artifact. This document cannot fully account for them.

---

This document reflects the project state as of 2026-06-16 and may be revised.
