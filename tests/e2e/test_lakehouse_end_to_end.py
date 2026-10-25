"""End-to-end lakehouse pipeline test.

Fixes vs the original:
- `python` (absent on ubuntu runners / foreign interpreters) -> sys.executable
- runs in a tmp cwd so the repo tree is never dirtied (the pipeline modules
  resolve data/ relative to CWD; a drift guard in CI now enforces this)
- asserts gold CONTENT (a pipeline that 'succeeds' having produced 0 rows is a
  failure, per mission data-pipeline rules)
- asserts the scripts fail loudly when inputs are missing (they previously
  logged/printed and exited 0 - silent success)
"""
import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = [
    "src/lakehouse/bronze_food_security.py",
    "src/lakehouse/silver_food_security.py",
    "src/lakehouse/gold_food_security.py",
    "src/governance/data_quality.py",
]


def write_synthetic_interim(cwd: Path):
    interim = cwd / "data" / "interim" / "standardized"
    interim.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({
        "country_code": ["USA", "CAN", "KEN"],
        "data_source": ["FAOSTAT"] * 3,
        "data_version": ["V1"] * 3,
        "ingestion_timestamp": ["2025-01-01T00:00:00Z"] * 3,
        "year": [2020, 2021, 2022],
        "indicator_value": [1.23, 2.34, 3.45],
        "indicator_name": ["Prevalence of undernourishment"] * 3,
        "quality_score": [0.95, 0.95, 0.95],
    }).to_parquet(interim / "faostat_food_security.parquet", index=False)


def run_script(script: str, cwd: Path):
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / script)],
        cwd=cwd, capture_output=True, text=True, timeout=180,
    )


def test_end_to_end_lakehouse(tmp_path):
    write_synthetic_interim(tmp_path)
    for script in SCRIPTS:
        proc = run_script(script, tmp_path)
        assert proc.returncode == 0, (
            f"{script} failed (rc={proc.returncode}):\nSTDOUT:{proc.stdout}\nSTDERR:{proc.stderr}"
        )

    gold_path = tmp_path / "data" / "gold" / "marts" / "food_security_country_year.parquet"
    assert gold_path.exists(), "gold mart was not produced"

    gold = pd.read_parquet(gold_path)
    # A pipeline that 'succeeds' with 0 rows is a failure, not a pass.
    assert len(gold) > 0, "gold mart is empty - silent zero-row success"
    assert {"country_code", "year"} <= set(gold.columns), f"gold mart missing keys: {gold.columns}"


def test_scripts_fail_loudly_when_inputs_are_missing(tmp_path):
    # Empty cwd: no data/interim at all. Bronze must exit non-zero (it used to
    # log an error and exit 0 - silent success that made e2e 'pass' vacuously).
    proc = run_script("src/lakehouse/bronze_food_security.py", tmp_path)
    assert proc.returncode != 0, "bronze must fail loudly when its input is missing"
