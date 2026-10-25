from pathlib import Path
import pandas as pd
import logging

BRONZE_DIR = Path("data/bronze/faostat")
SILVER_DIR = Path("data/silver/facts")
SILVER_DIR.mkdir(parents=True, exist_ok=True)


def build_food_security_fact():
    bronze_path = BRONZE_DIR / "food_security_bronze.parquet"
    if not bronze_path.exists():
        logging.error(f"Bronze input not found: {bronze_path}")
        raise SystemExit(1)

    df = pd.read_parquet(bronze_path)

    cols = [
        "country_code",
        "year",
        "indicator_id",
        "indicator_name",
        "indicator_value",
        "quality_score",
        "data_source",
        "ingestion_timestamp",
    ]
    missing = [c for c in cols if c not in df.columns]
    if missing:
        # Fail loud: this branch previously logged and returned 0 WITHOUT
        # writing the fact table - a schema violation disguised as success
        # (caught live by tests/e2e, which then starved the gold stage).
        logging.error(f"Bronze input missing required columns: {missing}")
        raise SystemExit(1)

    fact = df[cols].dropna(subset=["country_code", "year"])

    silver_path = SILVER_DIR / "food_security_fact.parquet"
    fact.to_parquet(silver_path, index=False)

    logging.info(f"Silver fact table written: {silver_path}")


if __name__ == "__main__":
    build_food_security_fact()
