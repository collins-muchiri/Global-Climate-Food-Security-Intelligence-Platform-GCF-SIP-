# STATUS.md

Last updated: 2026-10-24 (UTC) by Phase 0 audit session.

## Where this repo stands

- Phase 0 (forensic audit): COMPLETE. See `AUDIT.md`, `docs/PROVENANCE.md`, verbatim evidence in `docs/evidence/audit-phase0/`.
- Phases P1-P8: NOT STARTED.
- Honest completion vs Definition of Done: ~15%. This is the least mature of the five repos: 679 LOC of Python, 19 placeholder directories, 4 test files of which 1 fails, 1 is unfailable, 1 skips, and 1 is never collected. CI has failed on the last 5 runs.

## What actually runs right now (verified this session)

| Command | Result |
|---|---|
| `uv venv --python 3.11` + subset install (pandas, pyarrow, scikit-learn, fastapi, pydantic<2, pandera, xgboost, pytest, uvicorn) | PASS |
| `pytest tests/ -v` | 3 passed, 1 FAILED (e2e shells out to bare `python`; ImportError pyarrow verbatim in tests.log) |
| `python src/lakehouse/bronze_food_security.py` (venv interpreter) | PASS exit 0 |
| `uvicorn src.api.main:app` + GET /health,/docs,/openapi.json | 200/200/200 (openapi.json is 470 bytes: health-only API) |
| `slice/ingest.py` | NOT RUNNABLE clean: requires `SLICE_SOURCE_URL` env var, no committed example |

## Known-broken / not real

1. README "Data Ingestion ✅ Operational" is not backed: FAOSTAT test never collected, CI red.
2. 19 `.gitkeep`-only directories (notebooks, airflow/spark/streaming pipelines, k8s/terraform infra, model dirs) - theatre per D14; deletion scheduled P1.
3. `tests/unit/test_sanity.py` (`assert 1==1`) - forbidden unfailable test.
4. Poetry pyproject with obsolete pins (langchain 0.0.208, pydantic v1), no lockfile.
5. No data manifest, no licences recorded for any planned source.

## Exact next commands for the next operator

```bash
git clone https://github.com/collins-muchiri/Global-Climate-Food-Security-Intelligence-Platform-GCF-SIP-
cd Global-Climate-Food-Security-Intelligence-Platform-GCF-SIP-
uv venv --python 3.11
uv pip install pandas numpy pyarrow scipy scikit-learn fastapi 'pydantic<2' httpx pytest pandera xgboost uvicorn
uv run pytest tests/ -v      # reproduce: 3 passed, 1 failed
# then start P1 per AUDIT.md section 7 (delete placeholders, fix e2e sys.executable, CI rewrite)
```

## Checkpoint log

- 2026-10-24 Phase 0: install/tests/bronze/API executed and captured verbatim; AUDIT.md + PROVENANCE.md + STATUS.md + DECISIONS.md committed on `audit/phase-0`; PR opened. CI on main is red for pre-existing reasons; PR merge waits for green per rule 0.8.
