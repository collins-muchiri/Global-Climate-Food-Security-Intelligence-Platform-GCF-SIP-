from pathlib import Path
import pandas as pd
import logging

SILVER_DIR = Path("data/silver/facts")
GOLD_DIR = Path("data/gold/marts")
GOLD_DIR.mkdir(parents=True, exist_ok=True)


def build_food_security_country_year():
    silver_path = SILVER_DIR / "food_security_fact.parquet"
    if not silver_path.exists():
        logging.error(f"Silver input not found: {silver_path}")
        raise SystemExit(1)

    df = pd.read_parquet(silver_path)

    try:
        gold = (
            df.groupby(["country_code", "year", "indicator_name"], as_index=False)
            .agg(
                indicator_value=("indicator_value", "mean"),
                avg_quality_score=("quality_score", "mean"),
            )
        )
    except Exception as e:
        logging.error(f"Failed to compute gold: {e}")
        return

    gold_path = GOLD_DIR / "food_security_country_year.parquet"
    gold.to_parquet(gold_path, index=False)

    logging.info(f"Gold mart written: {gold_path}")


if __name__ == "__main__":
    build_food_security_country_year()
