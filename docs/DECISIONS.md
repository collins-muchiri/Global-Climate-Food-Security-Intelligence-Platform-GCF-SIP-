# DECISIONS.md

Zero-Red Mandate decisions (mission rule 11.6).

## D-G1 (2026-10-25) CI matrix pinned to Python 3.11 only

pydantic ^1.10 and langchain 0.0.208 (declared pins) do not support Python 3.12+.
Widening the matrix would require the pydantic-v2/langchain modernisation - an
API-breaking, feature-scale change outside a reliability pass (rule 11.1).
The constraint is now VISIBLE (matrix comment + this file) and tracked in the
modernisation issue instead of silently limiting the project.

## D-G2 (2026-10-25) pandas floor raised ^1.5 -> ^2.1.1

pandera (validation schemas, now a declared test dependency) requires pandas
>=2.1.1; pandas 1.5.3 is from 2022. Source scan for pandas-2-removed APIs
(DataFrame.append, iteritems, .ix): only list.append hits (not the removed
DataFrame API). Suite green on pandas 2.x after the bump.

## D-G3 (2026-10-25) Poetry packaging declares the real src/ layout

`pip install -e .` NEVER worked: Poetry searched for a `gcf-sip` package and
died with ModuleOrPackageNotFoundError. CI masked this by installing only
pytest. Fix matches reality (every module imports `src.*`): `packages =
[{include = "src"}]`. Restructuring to a proper `gcf_sip` namespace is the
right long-term shape and is tracked in the modernisation issue - it renames
every import in the codebase, which is a refactor, not a repair.

## D-G4 (2026-10-25) Pipeline scripts fail loud on missing/invalid input

bronze/silver/gold/governance previously logged (or printed) and exited 0 when
inputs were missing or schema-invalid: a stage could "succeed" having produced
nothing, starving downstream stages silently. All four now exit non-zero. The
e2e test asserts both directions (full run green; missing input red).

---

# Phase-0 audit decisions (2026-10-24, preserved verbatim)

# DECISIONS.md

Stop-and-log register (mission rule 0.11).

## D-001 Audit ran a dependency SUBSET, not the declared Poetry stack

- Assumption: `[tool.poetry]` block has no lockfile and pins obsolete versions (langchain 0.0.208, pydantic ^1.10); pyspark/transformers are optional and not needed to execute existing tests.
- Rationale: the goal of Phase 0 is "does what exists run", not "can the aspirational stack install". The subset (pandas, numpy, pyarrow, scipy, scikit-learn, fastapi, pydantic<2, httpx, pytest, pandera, xgboost, uvicorn) is exactly what the collected tests import. Command recorded in `docs/evidence/audit-phase0/2026-10-24-install.log`.
- Reversibility: full - P1 replaces Poetry with uv/PEP621 + committed lockfile.

## D-002 e2e failure root-caused, not fixed, in Phase 0

- Assumption: Phase 0 writes no production code.
- Rationale: reproduced the failure by running the exact subprocess command with the system interpreter (ImportError pyarrow, verbatim in tests.log). Fix is one line (`sys.executable`) in P1.
- Reversibility: full.

## D-003 Stale `step-*` branches left on origin

- Assumption: rule 0.8 forbids deleting remote branches.
- Rationale: disclosed in PROVENANCE.md instead.
- Reversibility: owner can delete at will.

## D-004 Transient pipeline outputs removed after audit

- Assumption: `bronze_food_security.py` writes `data/bronze/` and `data/interim/standardized/`; these are generated artefacts, not evidence.
- Rationale: keeping the tree clean for the audit commit; the command+exit status is the evidence (api-run.log).
- Reversibility: re-run the script.

## D-005 Audit PR not merged while CI is red

- Assumption: rule 0.8 - merge only on green CI. CI on main fails for pre-existing reasons (pytest-only install; failing e2e).
- Rationale: the audit PR adds docs/evidence only and cannot itself turn a broken build green; merging over red CI would violate 0.8. PR stays open; P1 branch will fix CI and the audit PR can merge immediately after, or P1 supersedes it.
- Reversibility: full.
