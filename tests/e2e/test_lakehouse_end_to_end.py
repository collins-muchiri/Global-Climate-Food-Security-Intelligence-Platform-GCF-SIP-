import os
import pandas as pd
from pathlib import Path

def write_synthetic_interim():
    interim_dir = Path("data/interim/standardized")
    interim_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({
        "country_code": ["USA", "CAN"],
        "data_source": ["FAOSTAT", "FAOSTAT"],
        "data_version": ["V1", "V1"],
        "ingestion_timestamp": ["2025-01-01T00:00:00Z", "2025-01-02T00:00:00Z"],
        "year": [2020, 2021],
        "indicator_value": [1.23, 2.34],
        "indicator_name": ["Prevalence of undernourishment", "Prevalence of undernourishment"],
    })
    df.to_parquet(interim_dir / "faostat_food_security.parquet", index=False)

def test_end_to_end_lakehouse_end_to_end():
    write_synthetic_interim()
    import subprocess
    # Bronze
    subprocess.run(["python", "src/lakehouse/bronze_food_security.py"], check=True)
    # Silver
    subprocess.run(["python", "src/lakehouse/silver_food_security.py"], check=True)
    # Gold
    subprocess.run(["python", "src/lakehouse/gold_food_security.py"], check=True)
    # Quality governance
    subprocess.run(["python", "src/governance/data_quality.py"], check=True)
    # Assert final gold parity file exists
    gold_path = Path("data/gold/marts/food_security_country_year.parquet")
    assert gold_path.exists()
