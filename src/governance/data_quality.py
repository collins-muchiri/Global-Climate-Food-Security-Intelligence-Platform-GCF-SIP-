from pathlib import Path
import logging

import pandas as pd

SILVER_DIR = Path("data/silver/facts")
META_DIR = Path("data/metadata")
META_DIR.mkdir(parents=True, exist_ok=True)


def compute_quality_metrics():
    silver_path = SILVER_DIR / "food_security_fact.parquet"
    if not silver_path.exists():
        print(f"Silver input not found: {silver_path}")
        raise SystemExit(1)

    df = pd.read_parquet(silver_path)

    metrics = (
        df.groupby("indicator_name")
        .agg(
            completeness=("indicator_value", lambda x: 1 - x.isna().mean()),
            avg_quality_score=("quality_score", "mean"),
            countries=("country_code", "nunique"),
            years=("year", "nunique"),
        )
        .reset_index()
    )

    metrics_path = META_DIR / "data_quality_metrics.parquet"
    metrics.to_parquet(metrics_path, index=False)

    # Also create a simple lineage placeholder
    lineage_path = META_DIR / "lineage.json"
    lineage_path.write_text("{\"source\": \"FAOSTAT\", \"version\": 1}")

    logging.getLogger(__name__).info(f"Data quality metrics written: {metrics_path}")


if __name__ == "__main__":
    compute_quality_metrics()
