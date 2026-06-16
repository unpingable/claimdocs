"""claimdocs CLI — write documentation claims as data; refuse to render strong claims
without declared basis.

    claimdocs lint                       # citation-shape validation
    claimdocs verify-basis --repo .      # resolve code/test bases against a source tree
    claimdocs render                     # emit docs/data/{graph,vocab}.json (refuses on lint error)
    claimdocs report                     # the fail-closed instrument panel (mode/basis/adequacy)
    claimdocs serve                      # serve docs/ locally
    claimdocs init                       # scaffold a new project

Run inside a project (a dir with claimdocs.yml) or pass --project DIR.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import glob
import os
import shutil
import sys

import yaml

from .builder import build
from .config import CONFIG_NAME, find_config, load_vocabulary
from .linter import Report, lint, load_cases

HERE = os.path.dirname(os.path.abspath(__file__))
RENDERER = os.path.join(HERE, "renderer")
TEMPLATE = os.path.join(HERE, "template")


def _today():
    # Deterministic default for CI; override with --today.
    return _dt.date.today().isoformat()


def _project(args):
    root = os.path.abspath(args.project)
    cfg = find_config(root)
    return os.path.dirname(cfg), load_vocabulary(cfg)


def _repos(args, default_root):
    repos = {"default": default_root}
    for spec in (args.repo or []):
        if "=" in spec:
            name, path = spec.split("=", 1)
            repos[name] = os.path.expanduser(path)
        else:
            repos["default"] = os.path.expanduser(spec)
    return repos


def cmd_lint(args):
    root, vocab = _project(args)
    report = Report()
    lint(root, vocab, report, args.today or _today(), strict_adequacy=args.strict_adequacy)
    return 0 if report.print() else 1


def cmd_verify(args):
    root, vocab = _project(args)
    report = Report()
    lint(root, vocab, report, args.today or _today(),
         verify=True, repos=_repos(args, root))
    return 0 if report.print() else 1


def cmd_render(args):
    root, vocab = _project(args)
    out = os.path.join(root, "docs", "data")
    rc = build(root, vocab, out, args.today or _today(), include_excluded=args.include_excluded)
    # copy the generic renderer into docs/ unless the project overrides it
    if rc == 0:
        for name in ("index.html", "graph.html"):
            dst = os.path.join(root, "docs", name)
            if not os.path.exists(dst) or args.force_renderer:
                shutil.copy(os.path.join(RENDERER, name), dst)
        open(os.path.join(root, "docs", ".nojekyll"), "a").close()
    return rc


def cmd_report(args):
    """Fail-closed instrument panel: every edge with its mode and basis posture.
    This is the readout that does NOT flatten — unlike the graph, mode is a column
    you cannot not see."""
    root, vocab = _project(args)
    rows = []
    for _, case in load_cases(root):
        for e in case.get("edges", []) or []:
            m = vocab.claim_modes.get(e.get("claim"))
            adq = (e.get("adequacy") or {}).get("status", "—") if m and m.witnesses else "n/a"
            rows.append((e.get("claim", "?"), e.get("id", "?"),
                         f"{e.get('from')}→{e.get('to')}", len(e.get("receipts") or []), adq))
    rows.sort()
    print(f"{'MODE':<11} {'EDGE':<22} {'RELATION':<40} {'RCPT':>4} {'ADEQUACY':<10}")
    print("-" * 92)
    for mode, eid, rel, nr, adq in rows:
        print(f"{mode:<11} {eid:<22} {rel[:40]:<40} {nr:>4} {adq:<10}")
    print(f"\n{len(rows)} edge(s). 'adequacy' is a recorded human admission, not a proof.")
    return 0


def cmd_serve(args):
    import http.server
    import socketserver
    root, _ = _project(args)
    os.chdir(os.path.join(root, "docs"))
    with socketserver.TCPServer(("", args.port), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"serving {root}/docs at http://localhost:{args.port}  (ctrl-c to stop)")
        httpd.serve_forever()


def cmd_init(args):
    root = os.path.abspath(args.project)
    if os.path.exists(os.path.join(root, CONFIG_NAME)) and not args.force:
        print(f"{CONFIG_NAME} already exists in {root} (use --force to overwrite)")
        return 1
    os.makedirs(os.path.join(root, "cases"), exist_ok=True)
    os.makedirs(os.path.join(root, "receipts"), exist_ok=True)
    if os.path.isdir(TEMPLATE):
        for p in glob.glob(os.path.join(TEMPLATE, "*")):
            shutil.copy(p, root)
    print(f"initialized claimdocs project in {root}. Edit {CONFIG_NAME}, then `claimdocs lint`.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="claimdocs", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", "-C", default=".", help="project dir (with claimdocs.yml)")
    ap.add_argument("--today", default=None, help="date for staleness checks (YYYY-MM-DD)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("lint").add_argument("--strict-adequacy", action="store_true",
                                        help="treat unadmitted witnessing edges as errors")
    v = sub.add_parser("verify-basis")
    v.add_argument("--repo", action="append", help="source tree: PATH or NAME=PATH (repeatable)")
    r = sub.add_parser("render")
    r.add_argument("--include-excluded", action="store_true")
    r.add_argument("--force-renderer", action="store_true", help="overwrite docs/*.html from template")
    sub.add_parser("report")
    s = sub.add_parser("serve"); s.add_argument("--port", type=int, default=8000)
    i = sub.add_parser("init"); i.add_argument("--force", action="store_true")

    args = ap.parse_args(argv)
    return {
        "lint": cmd_lint, "verify-basis": cmd_verify, "render": cmd_render,
        "report": cmd_report, "serve": cmd_serve, "init": cmd_init,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
