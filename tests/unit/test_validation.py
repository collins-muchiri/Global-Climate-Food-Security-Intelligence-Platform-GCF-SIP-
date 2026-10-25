import pandas as pd
import pytest

def test_validation_pass_or_skip():
    # The former try/pytest.skip guard made this test vacuous: pandera was not
    # a declared dependency anywhere, so the suite silently skipped in every
    # environment (a test that can never run certifies nothing). pandera is
    # now declared in the `test` extra and the import is unconditional.
    from src.validation.pandera_schemas import faostat_schema
    df = pd.DataFrame({
        "country_code": ["USA", "CAN"],
        "year": [2020, 2021],
        "indicator_id": ["FAOSTAT_21004", "FAOSTAT_21004"],
        "indicator_name": ["Prevalence of undernourishment", "Prevalence of undernourishment"],
        "indicator_value": [1.0, 2.0],
        "quality_score": [0.9, 0.95],
        "data_source": ["FAOSTAT", "FAOSTAT"],
        "ingestion_timestamp": ["2025-01-01T00:00:00Z", "2025-01-02T00:00:00Z"],
    })
    schema = faostat_schema()
    assert schema.validate(df, lazy=True).shape[0] == df.shape[0]
