# AUDIT.md - Phase 0 Forensic Audit

Repo: Global-Climate-Food-Security-Intelligence-Platform-GCF-SIP-
Audit date: 2026-10-24 (UTC, execution-environment clock)
Auditor: autonomous agent session (principal-engineer mission), account collins-muchiri
Status: Phase 0 complete for this repo. No production code changed during the audit.

## 1. Method

Clean clone at `/home/user/audit_ws/Global-Climate-Food-Security-Intelligence-Platform-GCF-SIP-` (main @ d2e3b28). Raw outputs committed verbatim under `docs/evidence/audit-phase0/`:

| Evidence file | Command | Result |
|---|---|---|
| `2026-10-24-install.log` | `uv venv --python 3.11` + `uv pip install pandas numpy pyarrow scipy scikit-learn fastapi 'pydantic<2' httpx pytest pandera xgboost uvicorn` | SUCCESS |
| `2026-10-24-tests.log` | `python -m pytest tests/ -v` | 3 passed, 1 failed; `tests/Ingest/` collected 0 tests |
| `2026-10-24-api-run.log` | direct bronze script run + `uvicorn src.api.main:app --port 8601` + GET /health,/docs,/openapi.json | bronze exit 0; API 200/200/200 |

GitHub Actions state at audit time (`gh run list`, 2026-10-24): all five most recent CI runs on main FAILED. CI installs only pytest, while `tests/unit/test_health.py` imports fastapi - CI cannot pass as written.

Environment limits disclosed: no Docker daemon, no macOS runner, no dbt/Airflow/Spark execution attempted locally.

## 2. Inventory

- Python 679 LOC across 36 files (`src/`, `slice/`, `tests/`, `pipelines/` are mostly empty dirs).
- 19 `.gitkeep` placeholder directories: `notebooks/01-04`, `pipelines/{airflow,spark,streaming}`, `src/models/{baseline,classical_ml,deep_learning}`, `infra/{terraform,monitoring,kubernetes}`, `dashboards/{streamlit,superset}`, `data/{external,raw,interim,processed}`, etc. Direct violation of mission rule 0.4 (.gitkeep-only directories forbidden).
- Tests: 4 files. `tests/unit/test_sanity.py` is `assert 1 == 1` - a forbidden unfailable test (rule 0.3). `tests/Ingest/test_faostat_ingest.py` is never collected (capitalised dir, no `__init__.py`) - dead test.
- CI: 1 workflow, py3.11 ubuntu-only, pytest-only install.
- pyproject is Poetry-style (`[tool.poetry]`), python ^3.11, pins pydantic v1, langchain 0.0.208, transformers, optional pyspark. Mission stack requires uv + PEP 621 pyproject + Pydantic v2.
- Branches: main + 4 stale step branches (`step-01-foundation`, `step-02-data-ingestion`, `step-02-faostat-ingestion`, `step-03-platform-health`). Tags: v0.2.0 only.
- Licence: LICENSE file present (see PROVENANCE).
- Authorship: 11 x `83084745+bucky-ops@users.noreply.github.com` (former account name), 6 x `83084745+collins-muchiri@users.noreply.github.com`.

## 3. Run results

### 3.1 Install - PASS (with substitution)
Poetry lockfile absent; installed a working dependency subset via uv per the command above. `environment.yml` and `[tool.poetry]` disagree with what is installable today; full declared stack (pyspark, transformers, langchain 0.0.208) NOT installed - langchain 0.0.208 is an obsolete pinned version and a supply-chain concern.

### 3.2 Tests - FAIL (1 of 4 collected) and 2 of 4 collected tests are theatre
- `test_end_to_end_lakehouse_end_to_end` FAILED: the test shells out to bare `python src/lakehouse/bronze_food_security.py` with `check=True`. In any environment where `python` is not the venv interpreter, the subprocess raises `ImportError: Unable to find a usable engine; tried using: 'pyarrow', 'fastparquet'` (captured verbatim in tests.log). Environment-dependent test: must use `sys.executable`.
- `test_sanity` (`assert 1 == 1`) and the pandera-skip pattern in `test_validation` (`pytest.skip` when pandera missing) violate rules 0.3/0.4 as written.
- `tests/Ingest/test_faostat_ingest.py`: 0 collected. The FAOSTAT ingestion "✅ Operational" claim has never been exercised by CI.

### 3.3 Lakehouse scripts - PASS locally
`bronze_food_security.py` run with the venv interpreter exits 0 and writes `data/bronze/`, `data/interim/standardized/` (untracked outputs cleaned after the audit).

### 3.4 API - PASS (minimal)
`uvicorn src.api.main:app`: `/health` 200 (15 bytes), `/docs` 200, `/openapi.json` 200 but only 470 bytes - the API is essentially a health endpoint. No /healthz /readyz /livez split, no dependency checks, no domain routes.

### 3.5 Vertical slice - CONDITIONAL
`slice/ingest.py` hard-exits unless `SLICE_SOURCE_URL` is set; no committed example URL/cache, so a clean clone cannot run the slice as-is. Release v0.2.0's "one working vertical slice" is conditional on operator-supplied env config.

## 4. Gap matrix vs Definition of Done

| DoD | State | Evidence | Fix cost |
|---|---|---|---|
| D1 clean-clone ubuntu+macos, zero secrets | ABSENT | slice needs env URL; CI red; macOS never run | M |
| D2 CI green + all gates | ABSENT | 5/5 recent runs failed; only pytest step exists | L |
| D3 coverage 85/75 | ABSENT | no coverage config; most src dirs empty | L |
| D4 mypy --strict, ruff | ABSENT | ruff declared, never gated | M |
| D5 claims -> docs/evidence | PARTIAL | COMPLETION_MATRIX.md is tree-derived (honest); README "✅ Operational" rows not backed | M |
| D6 docs set | PARTIAL | docs/architecture (3 files), docs/governance (3 files), CONTRIBUTING exist; no DATA.md/MODEL_CARD/EVALUATION/THREAT_MODEL/RUNBOOK/ADR/CHANGELOG/STATUS (STATUS added by this audit) | L |
| D7 adversarial QA | ABSENT | none | L |
| D8 self-review | ABSENT | none this mission | M |
| D9 release + GHCR + SBOM | PARTIAL | v0.2.0 pre-release exists; no image/SBOM | M |
| D10 metadata/topics/CODEOWNERS/dependabot/protection | ABSENT-PARTIAL | to set in P1 | S |
| D11 live demo | ABSENT | no deployed instance | L |
| D12 STATUS/lie detector | PARTIAL | this audit | S |
| D13 15-min evaluator path | ABSENT | README quickstart references unrunnable slice | S |
| D14 no theatre | FAIL | 19 .gitkeep dirs, sanity test, dead Ingest test, "Operational" claims, empty notebooks/pipelines/infra trees | M (delete-heavy) |

## 5. Risk register

| ID | Risk | Class | Sev | Remediation |
|---|---|---|---|---|
| R1 | README claims "✅ Operational" for FAOSTAT ingestion while its only test is never collected | integrity (0.1) | P0 | Fix collection, run in CI, or downgrade claim to "code present, unverified" |
| R2 | e2e test env-dependent (`python` vs `sys.executable`) | correctness | P0 | P1 one-line fix + CI dependency install |
| R3 | 19 .gitkeep placeholder trees imply capability that does not exist (Spark/Airflow/k8s/Terraform/notebooks) | theatre (D14) | P0 | Delete empties; recreate only when implemented |
| R4 | langchain==0.0.208 + pydantic v1 pinned: obsolete, known-vuln surface | security | P1 | Migrate to pydantic v2; drop or modernise langchain in P3 LLM work |
| R5 | No data manifest/licences/checksums for any claimed source (FAOSTAT, World Bank, OECD DAC, CHIRPS...) | data governance | P1 | P2 manifest.yaml |
| R6 | CI installs only pytest; every future gate absent | correctness | P1 | P1 CI rewrite |
| R7 | Unfailable/skipping tests (sanity, pandera-skip) | integrity (0.3) | P1 | Replace with real assertions in P1/P2 |
| R8 | Stale step branches suggest abandoned workflow | hygiene | P3 | Leave intact (rule 0.8: no remote branch deletion by agent); flag to owner |

## 6. Lie detector

| CLAIM | EVIDENCE | VERDICT |
|---|---|---|
| "Data Ingestion ✅ Operational - FAOSTAT integration with fail-safe handling" (README) | Ingest test never collected; CI red; slice requires env URL | NOT BACKED |
| "API Layer ✅ Operational - FastAPI with health endpoints" (README) | /health 200 this session (api-run.log) | SUPPORTED (health only; no domain endpoints exist) |
| "one working vertical slice" (release v0.2.0 notes) | slice/ingest.py exists; exits non-zero without SLICE_SOURCE_URL; never run end-to-end in CI | PARTIAL |
| COMPLETION_MATRIX.md status grid | tree-derived per its own header (remediation commit d2e3b28) | SUPPORTED as tree evidence, not as functional evidence |
| Lakehouse bronze/silver/gold pipeline | bronze exits 0 locally with synthetic interim input; silver/gold not run this session | PARTIAL |
| Architecture docs (dbt semantic layer, Iceberg, Dagster/Prefect, PyMC, Sobol, MILP per mission spec) | no dbt project, no orchestrator config, no PyMC/PuLP code anywhere in tree | ABSENT - docs describe aspiration |

## 7. Sequenced work plan

1. P1 Foundations (M): delete .gitkeep theatre (R3), fix R2, convert pyproject to uv/PEP621 + pydantic v2, Makefile contract, CI rewrite (3.11+3.12 x ubuntu+macos; install real deps; coverage; ruff; mypy start), remove sanity test, fix Ingest collection, repo metadata. PR.
2. P2 Data layer (L): `data/manifest.yaml` (FAOSTAT API, World Bank, CHIRPS, SPEI, EM-DAT, ACLED with licences/retrieval dates/checksums); committed offline sample cache so `make data` runs with zero network and zero secrets; pandera contracts + DQ report artefacts. PR.
3. P3 Core engine (L): risk model (boosted trees first, hierarchical Bayes after), held-out-country + held-out-time splits, climatology benchmark; LLM briefing via RAG on computed tables only with citation guardrail + deterministic fallback. PR.
4. P4 Service/API + UI (L): real domain routes, /healthz /readyz /livez, OpenAPI export gate, typed TS client, minimal dashboard. PR.
5. P5 Evaluation (M-L): calibration/discrimination/skill vs climatology, scenario Monte Carlo + Sobol where implemented, metrics JSON under docs/evidence/metrics/, model-eval + reproducibility gates, EVALUATION.md. PR.
6. P6 Hardening (M): security scanners, QA suite, THREAT_MODEL, governance docs ("no expert review obtained" caveat per spec 3.2). PR.
7. P7 Presentation (M): market pack, 15-min path, release/GHCR/SBOM. PR.
8. P8 Self-review (S-M). Final PR.
