# Working in claimdocs

Read [CHARTER.md](CHARTER.md) before changing behavior or public documentation.
claimdocs is a generic, vocabulary-driven documentation engine; do not add
Governor-specific terms or assumptions to its core.

- Keep recorded claim mode, basis existence, cited-body freshness, human
  adequacy, runtime execution, and operational authority distinct.
- Never describe `verify-basis` as executing tests, checking dependency closure,
  or proving that a basis establishes an edge.
- Put global CLI options (`--project`, `--today`) before the subcommand. Put
  command-specific options such as `verify-basis --repo` after the subcommand.
- Treat `render` as a content mutation of generated `docs/`; inspect its full
  output diff. `lint`, `report`, and `verify-basis` are the read-only inspection
  commands for an existing case.
- Use substitution fixtures and deterministic negative controls for validation.
  Do not include private paths, campaign notes, credentials, or provider calls.

Run the standalone engine check with:

```sh
python tests/test_claimdocs.py
```
