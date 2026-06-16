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

    print("\nPASS" if ok else "\nFAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
