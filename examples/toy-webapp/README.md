# toy-webapp — the genericity proof

A deliberately boring, **non-AG** claimdocs case: `frontend → api → sqlite`, with an async
worker. It exists to falsify one claim — *"claimdocs is generic."* If the engine can
document this with no Agent Governor vocabulary leaking into the config, the abstraction is
real. It uses the canonical mode spine (`documented / specified / derived / candidate`)
directly, no aliases.

```bash
PYTHONPATH=../../src python -m claimdocs -C . lint
PYTHONPATH=../../src python -m claimdocs -C . verify-basis --repo default=.
PYTHONPATH=../../src python -m claimdocs -C . report
```

The graph: 3 `documented` edges (each cites a real symbol in `src/api.py` + a test, pinned
by body hash), 1 `specified` edge (the worker, designed not built), 1 `derived` edge (user
data reaches sqlite, from frontend→api + api→db), 1 `candidate` edge (a proposed retry
path, hidden by default).

## Reproduce stale detection (the hollow-test defense)

`verify-basis` proves a cited symbol still resolves *and* that its body is unchanged since
admission. Hollow a body without renaming it and freshness fails closed:

```bash
# break save_user's body but keep its name + signature
sed -i 's/DB.execute(.*/return None  # hollowed/' src/api.py
PYTHONPATH=../../src python -m claimdocs -C . verify-basis --repo default=.
#   -> ERROR [BASIS_BODY_CHANGED] ... r-save-user: symbol resolves but its body
#      changed since admission (adequacy STALE — re-admit ...)
git checkout src/api.py   # or undo the edit; freshness goes green again
```

The symbol still resolves — `grep save_user` is happy — but the edge's adequacy admission
no longer applies. Resolved is not supported.
