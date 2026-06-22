#!/usr/bin/env python3
"""Self-test for the claimdocs engine.

A linter is only as good as its discrimination: each failure fixture is paired with the
rule it must trip. If a fixture starts failing for a different rule, that's a regression.

Run: python tests/test_claimdocs.py   (exit 0 iff every assertion holds)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))

from claimdocs.config import load_vocabulary  # noqa: E402
from claimdocs.linter import Report, lint  # noqa: E402
from claimdocs.verify import extract_symbol_body, hash_body  # noqa: E402

FIX = os.path.join(ROOT, "fixtures")
TODAY = "2026-06-16"

FAIL = {
    "no-receipt": "EDGE_NO_RECEIPT",
    "wired-no-witness": "MODE_NEEDS_WITNESS",
    "gate-no-refusal": "REFUSAL_MISSING",
    "derived-tower": "DERIVATION_TOWER",
}


def codes(root):
    vocab = load_vocabulary(os.path.join(root, "claimdocs.yml"))
    rep = Report()
    lint(root, vocab, rep, TODAY)
    return {c for c, _, _ in rep.errors}


def main():
    ok = True

    # pass fixture lints clean
    pc = codes(os.path.join(FIX, "pass"))
    if pc:
        ok = False; print(f"FAIL: pass fixture errored: {sorted(pc)}")
    else:
        print("ok: pass fixture lints clean")

    # each failure fixture trips its designated rule
    for name, rule in FAIL.items():
        c = codes(os.path.join(FIX, "fail", name))
        if rule in c:
            print(f"ok: {name} -> {rule}")
        else:
            ok = False; print(f"FAIL: {name} expected {rule}, got {sorted(c)}")

    # body-hash is sensitive to body change, tolerant of trailing-whitespace reflow
    src_a = "def f(x):\n    return policy.verdict(x)\n"
    src_b = "def f(x):\n    return policy.verdict(x)   \n"   # cosmetic
    src_c = "def f(x):\n    return True\n"                   # hollowed
    ha = hash_body(extract_symbol_body(src_a, "def f"))
    hb = hash_body(extract_symbol_body(src_b, "def f"))
    hc = hash_body(extract_symbol_body(src_c, "def f"))
    if ha == hb and ha != hc:
        print("ok: body-hash forgives reflow, catches hollowing")
    else:
        ok = False; print(f"FAIL: body-hash semantics wrong (a==b:{ha==hb}, a!=c:{ha!=hc})")

    # firewall (behavioral): a vocab pack is DATA, never code. config.py calls itself
    # "the firewall"; this pins it. Under yaml.load the tag below would execute os.system
    # and drop the sentinel; under yaml.safe_load it must refuse before any execution.
    # This is the real firebreak — stronger than grepping the engine for domain words,
    # because data cannot import. (The core/vocab boundary the engine was designed around.)
    import tempfile
    sentinel = os.path.join(tempfile.gettempdir(), f"claimdocs_firewall_breach_{os.getpid()}")
    if os.path.exists(sentinel):
        os.unlink(sentinel)
    poison = f'modes:\n  evil: !!python/object/apply:os.system ["touch {sentinel}"]\n'
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as fh:
        fh.write(poison); ppath = fh.name
    try:
        load_vocabulary(ppath)
    except Exception:
        pass  # refusing to parse is fine; executing is not
    finally:
        os.unlink(ppath)
    if not os.path.exists(sentinel):
        print("ok: vocab firewall holds (code in a pack is refused, not executed)")
    else:
        ok = False; os.unlink(sentinel)
        print("FAIL: a vocab pack executed code — firewall breached (yaml.load?)")

    # firewall (lexical smoke alarm): no ENGINE module may hardcode a specimen's domain
    # vocabulary. Weaker than the data-firewall above (the dialogue's point: bind on
    # structure, not a wordlist) — kept only to catch a dev wiring a domain term into core.
    DOMAIN = ("spendability", "spend_wall", "standing_class", "blast_radius", "desync")
    eng = os.path.join(ROOT, "src", "claimdocs")
    leaks = [f"{fn}:{t}" for fn in sorted(os.listdir(eng)) if fn.endswith(".py")
             for t in DOMAIN if t in open(os.path.join(eng, fn)).read().lower()]
    if not leaks:
        print("ok: engine carries no specimen domain vocabulary")
    else:
        ok = False; print(f"FAIL: engine contaminated by domain vocab: {leaks}")

    print("\nPASS" if ok else "\nFAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
