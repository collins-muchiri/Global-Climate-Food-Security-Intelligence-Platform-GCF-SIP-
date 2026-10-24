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
