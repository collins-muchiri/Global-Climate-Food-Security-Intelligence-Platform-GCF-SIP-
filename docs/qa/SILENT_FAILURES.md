# SILENT_FAILURES.md - sweep dispositions (2026-10-25)

| Pattern class | Disposition |
|---|---|
| stage scripts exiting 0 with no output on missing/invalid input | FIXED (D-G4): bronze/silver/gold/governance raise SystemExit(1); e2e asserts non-zero on missing input |
| NameError on the success path (governance logging import) | FIXED: caught by e2e the first time the pipeline ever ran to completion in a verified environment |
| bare `python` in subprocess (e2e) | FIXED: sys.executable |
| tests writing into the repo data/ tree | FIXED: e2e runs in tmp_path cwd; CI drift guard enforces (worktree + untracked data/) |
| pytest.skip when pandera absent | REMOVED: pandera declared in [test] extra; the skip made the validation gate vacuous in every environment |
| except-pass / bare except / suppress / soft_fail | 0 hits in src (rg sweep; ingestion retry loop logs failures into a failed_items list and reports it) |
| broad except at boundaries | src/api/routes/ingest.py delegates to orchestrator; FastAPI returns 5xx on unhandled (no 500->200 conversion found) |
| randomness/seeds | no seed-dependent logic in gated paths (rg seed/random_state: model scaffolding only, untested surface - modernisation issue) |
