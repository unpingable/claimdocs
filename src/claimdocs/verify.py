"""Basis resolution — the mechanical layer, and its honest boundary.

THE CHARTER LINE, in code:

    A resolved receipt witnesses that the cited basis EXISTS at the checked revision.
    It does not witness that the basis ESTABLISHES the edge. Edge adequacy is an
    admission decision, recorded separately, and is NOT re-checked here.

This module answers three mechanical questions and refuses the fourth:

    existence  — does the cited path (+ symbol) still resolve?            -> yes
    freshness  — is the cited symbol's BODY unchanged since admission?    -> yes (Python)
    execution  — does the cited test/probe pass?                          -> reserved (CHARTER)
    adequacy   — does this basis actually establish this edge?            -> NO. human admission.

The freshness check is the anti-rot move web-claude's hollow-test critique demands:
renaming a symbol trips existence; *hollowing* a symbol's body to `assert True` leaves
existence green but trips freshness. Symbol-resolves is not relation-holds; freshness
narrows the gap, it does not close it. Only re-admission closes it.

Python symbol extraction is the one built-in resolver. Other languages are a plugin
seam (see CHARTER) — deliberately not built.
"""
from __future__ import annotations

import ast
import hashlib
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class BasisStatus:
    resolved: bool                 # path (+ symbol) exists
    body_hash: str | None          # sha256 of the cited symbol body, if extractable
    detail: str = ""


def _parse_symbol(symbol: str) -> tuple[str | None, str]:
    """'def foo' -> ('function', 'foo'); 'class Bar' -> ('class', 'Bar').
    A bare/substring symbol (no def/class prefix) is not a structured Python symbol."""
    s = symbol.strip()
    if s.startswith("def "):
        return "function", s[4:].split("(")[0].strip()
    if s.startswith("class "):
        return "class", s[6:].split("(")[0].split(":")[0].strip()
    return None, s


def extract_symbol_body(source: str, symbol: str) -> str | None:
    """Return the exact source segment of a top-level (or nested) def/class named in
    `symbol`, or None if `symbol` is not a structured Python symbol or isn't found.
    The body hash is taken over this segment, so a rewrite of the function/class body
    changes the hash even though the name still resolves."""
    kind, name = _parse_symbol(symbol)
    if kind is None:
        return None
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    want = (ast.FunctionDef, ast.AsyncFunctionDef) if kind == "function" else (ast.ClassDef,)
    for node in ast.walk(tree):
        if isinstance(node, want) and node.name == name:
            seg = ast.get_source_segment(source, node)
            if seg is not None:
                return seg
    return None


def hash_body(body: str) -> str:
    # Normalize trailing whitespace per line so cosmetic reformatting alone is forgiven;
    # any change to tokens/structure still changes the hash.
    norm = "\n".join(line.rstrip() for line in body.splitlines())
    return "sha256:" + hashlib.sha256(norm.encode("utf-8")).hexdigest()


def resolve_basis(repo_root: str, path: str, symbol: str | None) -> BasisStatus:
    """Mechanical existence + (where possible) body extraction. No adequacy judgment."""
    full = os.path.join(repo_root, path)
    if not os.path.isfile(full):
        return BasisStatus(resolved=False, body_hash=None,
                           detail=f"path {path!r} does not exist under {repo_root}")
    if not symbol:
        return BasisStatus(resolved=True, body_hash=None, detail="path exists (no symbol pinned)")
    try:
        with open(full, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        return BasisStatus(resolved=False, body_hash=None, detail=f"unreadable: {exc}")
    if symbol not in text:
        return BasisStatus(resolved=False, body_hash=None,
                           detail=f"symbol {symbol!r} not found in {path!r} (moved or renamed?)")
    body = extract_symbol_body(text, symbol)
    bh = hash_body(body) if body is not None else None
    return BasisStatus(resolved=True, body_hash=bh,
                       detail="resolved" + ("" if bh else " (substring match; body not hashable)"))
