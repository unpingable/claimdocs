# claimdocs manpage standard

The law for the page layer. **No renderer exists yet** — this is written first, on
purpose, so that when a renderer is built it has a fixed target and cannot drift into
template theater. Holding the Jinja engine was deliberate; writing the standard is not the
same as building it.

A claimdocs manpage is a **mode-preserving readout over the claim graph.** It explains the
graph; it does not outrank it. Facts come from claim IDs; prose is glue.

## Page identity (BSD section vibes, adapted)

```
foo-overview(7)       doctrine / conceptual overview
foo-architecture(7)   system-level map
foo-receiver-gate(5)  interface / schema / contract / receipt format
foo-spend-wall(7)     policy / gate semantics
foo-orchestrator(8)   operational behavior
```

| Section | Meaning |
|---|---|
| (1) | CLI commands |
| (3) | library / API surfaces |
| (5) | formats, schemas, receipts |
| (7) | doctrine, architecture, semantics |
| (8) | operational / admin behavior |
| (9) | kernel / internal mechanics |

Not POSIX-pure. Good.

## Required sections

Every page MUST carry these. If a misreading would upgrade authority, NON-CLAIMS is not
optional.

```
NAME          one line: <id> - <terse purpose>
CLAIM STATUS  mode / basis (existence,freshness) / adequacy / reviewed sha — imported, not typed
DESCRIPTION   what it is, in mode-preserving prose
CLAIMS        the claim IDs this page imports (edge:..., node:...)
NON-CLAIMS    what this page must NOT be read as saying  ← the anti-laundering section
SEE ALSO      related pages / edges / specs
```

## Optional sections

```
SYNOPSIS  FAILURE MODES  RECEIPTS  INTERACTIONS  EXAMPLES
```

If every page needs fourteen headers, Future You will commit tax fraud against the
documentation. Four-to-six is the target.

## The one rule that matters

> No doc page gets to strengthen a claim mode.

Use the mode-preserving wording from the canonical spine (`CANONICAL_MODES` in
`config.py`), never a stronger verb:

```
documented   -> "is witnessed as"
specified    -> "is specified as"
derived      -> "is derived from"
candidate    -> "is a candidate relation"
deprecated   -> "was formerly"
contradicted -> "is disputed by"
```

A `specified` edge may not be written as "implemented." A `candidate` edge may not be
called "planned" without an authorizing basis. A `derived` edge must show its parents.

## Page-linter rules (for the future renderer — written as obligations now)

```
1. Every {{ edge(id) }} / {{ node(id) }} embed must resolve to an admitted claim.
2. A page may declare allowed_modes; embedding a disallowed mode fails the page.
3. If an embedded basis is stale (body changed since admission), the page is stale.
4. If an embedded mode is hidden-by-default, the page must label it.
5. A strong architectural sentence in prose must be followed by, or reference, a claim ID.
```

## Skeleton (illustrative — not a rendered artifact)

```
NAME
    standing-spendability-gate - admits spend only from standing-backed authority

CLAIM STATUS
    mode: wired (documented)   basis: resolved + fresh   adequacy: admitted @ <sha>

DESCRIPTION
    The standing-spendability gate is witnessed as refusing a spend whose standing
    observation lapsed past its horizon by exercise time.

CLAIMS
    edge:e-standing   edge:e-clock

NON-CLAIMS
    Does not claim all standing semantics are implemented locally.
    Does not claim Wicket or Standing are wired as live external services
      (those edges are `specified`, not `wired`).

SEE ALSO
    origin-fence(7), orchestrator(8), receipt-store(5)
```

That is the move: **manpages, but epistemically typed** — `man 5 passwd` bitten by a
formal-methods goblin. Build the renderer only when a case asks for prose; until then this
file is the contract.
