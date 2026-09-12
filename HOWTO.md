# Use claimdocs without strengthening its claims

Install the package, select a project, and keep global options before the command:

```sh
python -m pip install -e /path/to/claimdocs
claimdocs --project /path/to/case --today YYYY-MM-DD lint
claimdocs --project /path/to/case --today YYYY-MM-DD report
claimdocs --project /path/to/case --today YYYY-MM-DD \
  verify-basis --repo NAME=/path/to/source
```

The same ordering applies to `python -m claimdocs`. `--project` and `--today`
are global. `--repo` is an option of `verify-basis` and may be repeated for
receipts naming multiple repositories.

Read the outputs as four distinct statements:

1. A graph edge is a recorded claim in its configured mode, not runtime state.
2. Basis resolution says the cited path or Python symbol exists.
3. Cited-body freshness says only that the cited body matches its admitted hash.
   It does not cover helpers, fixtures, dependencies, datasets, or execution.
4. Adequacy is a recorded human admission. claimdocs does not mechanically prove
   that the basis establishes the edge, and no result grants operational authority.

`lint` checks configured case, receipt, refusal, derivation, and adequacy shapes.
`report` is a tabular readout. `verify-basis` adds the mechanical existence and
cited-body checks above. It does not execute cited tests. The built-in source
resolver supports Python symbols; other language and execution plugins are not
implemented.

`render` is intentionally mutating: it writes `docs/data`, may install renderer
files when absent, and creates `docs/.nojekyll`. Run it only when you intend to
review and publish a generated readout. Rendering preserves claim modes and does
not turn a recorded claim into verified runtime behavior.
