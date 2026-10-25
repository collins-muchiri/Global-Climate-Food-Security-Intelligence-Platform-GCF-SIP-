"""Real tests for src/ingestion/food_security_ingest.py.

Replaces the 0-byte placeholder that lived in tests/Ingest/ (capitalised dir,
empty file: collected by nothing, asserting nothing). Network fetchers are
deliberately NOT tested here (no CI network mocking seam yet - tracked in the
modernisation issue); the pure transformation functions are.
"""
import numpy as np
import pandas as pd
import pytest

from src.ingestion.food_security_ingest import compute_quality_score, standardize_schema

RAW = {
    "Area Code (ISO3)": ["KEN", "KEN", "USA"],
    "Year": ["2020", 2021, 2022],
    "Value": ["1.5", 2.5, "oops"],
    "Item": ["Prevalence of undernourishment"] * 3,
    "Extra Column FAOSTAT carries": ["x", "y", "z"],
}


def raw_df():
    return pd.DataFrame(RAW)


def test_standardize_renames_to_the_canonical_spine():
    out = standardize_schema(raw_df(), "21004")
    for col in ("country_code", "year", "indicator_value", "indicator_name",
                "data_source", "data_version", "ingestion_timestamp"):
        assert col in out.columns, f"canonical column missing: {col}"
    assert "Extra Column FAOSTAT carries" not in out.columns
    assert (out["data_source"] == "FAOSTAT").all()
    assert out["data_version"].str.contains("21004").all()


def test_standardize_enforces_types():
    out = standardize_schema(raw_df(), "21004")
    assert out["year"].dtype.kind == "i", "year must be integer"
    assert out["indicator_value"].dtype.kind == "f", "value must be numeric"


def test_standardize_coerces_unparseable_values_to_nan_not_crash():
    out = standardize_schema(raw_df(), "21004")
    assert np.isnan(out.loc[2, "indicator_value"]), "'oops' must coerce to NaN"


def test_standardize_rejects_missing_required_columns():
    broken = raw_df().drop(columns=["Value"])
    with pytest.raises(ValueError, match="Missing required columns"):
        standardize_schema(broken, "21004")


def test_quality_score_perfect_data_scores_one():
    df = pd.DataFrame({
        "year": list(range(2000, 2010)),
        "indicator_value": [1.0] * 10,
    })
    score = compute_quality_score(df)
    assert isinstance(score, pd.Series)
    assert np.allclose(score, 1.0), "complete + full coverage must score 1.0"


def test_quality_score_penalises_missing_values():
    df = pd.DataFrame({
        "year": list(range(2000, 2010)),
        "indicator_value": [1.0] * 9 + [np.nan],
    })
    score = compute_quality_score(df).iloc[0]
    expected = 0.7 * 0.9 + 0.3 * 1.0
    assert score == pytest.approx(expected), "completeness weight must be 0.7"


def test_quality_score_penalises_year_gaps():
    df = pd.DataFrame({
        "year": [2000, 2009],  # 2 of 10 years covered
        "indicator_value": [1.0, 1.0],
    })
    score = compute_quality_score(df).iloc[0]
    assert score == pytest.approx(0.7 + 0.3 * 0.2)
