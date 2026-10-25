# Hostile review: zero-red PR (rule 11.2) - 2026-10-25

1. Forbidden patterns on added lines: zero operative suppressions (the two
   `# noqa: F401` in test_sanity.py carry the reason "import IS the assertion" -
   the import is the test's mechanism, not a silenced warning; auditor tags not
   required for noqa-with-justification? They ARE required by rule 4.7 -> the
   auditor scans them; see below).
   **Self-catch during review**: scripts/audit_suppressions.py flags ANY noqa
   without a SUPPRESSION tag. The two justified noqas must carry tags or the
   gate fails - verify `python scripts/audit_suppressions.py --check` locally
   before merge. (It passed: the test files' noqa lines carry no tag -> wait,
   re-run and fix if red.)
2. Test integrity: no test deleted. test_sanity's `assert 1 == 1` was REPLACED
   by four real invariant tests (unfailable assertion = theatre per rule 4.9,
   replacement is strengthening). The 0-byte placeholder was replaced by 8 real
   tests. The validation skip was removed (pandera declared), so a test that
   never ran now runs. e2e assertions were strengthened (existence -> content +
   row count + fail-loud direction).
3. No tolerance widening, no seeds tuned, no time freezing: the score tests use
   exact analytic expectations (0.7*completeness + 0.3*coverage).
4. Manifest change honesty: packages=[{include="src"}] matches how every module
   already imports; pandas floor raised for a declared dependency's hard
   requirement (pandera>=2.1.1), verified by green suite, not to dodge a
   failure. Python matrix stays 3.11 for pin-constraint reasons documented in
   D-G1 with a modernisation issue - a visible constraint, not a silent dodge.
5. Fail-loud changes (SystemExit(1)) make previously-"green" no-op runs red:
   this is the point (rule 4.3: no soft_fail paths); e2e proves both directions.

## Verdict
MERGEABLE. Review follow-ups executed before push:
- the two test-file noqas were REMOVED (importlib.import_module pattern)
- pre-existing suppressions found by the auditor were also removed, not tagged:
  src/api/main.py pragma (decoration, no coverage gate), ingest_pipeline.py
  try/except flat-import fallback with 7x type:ignore (unwound to direct
  package imports; the fallback had been silently degrading ALL ingestion to
  not_implemented because `ingest_food_security` never existed - regression
  test added)
- scripts/audit_suppressions.py --check: 0 compliant, 0 violations
- full suite: 16 passed
