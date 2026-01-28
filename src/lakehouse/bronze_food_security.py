from pathlib import Path
import pandas as pd
import logging

INTERIM_DIR = Path("data/interim/standardized")
BRONZE_DIR = Path("data/bronze/faostat")
BRONZE_DIR.mkdir(parents=True, exist_ok=True)


def build_bronze_food_security():
    input_path = INTERIM_DIR / "faostat_food_security.parquet"
    if not input_path.exists():
        logging.error(f"Interim input not found: {input_path}")
        return

    df = pd.read_parquet(input_path)

    # Minimal normalization
    if "country_code" in df.columns:
        df["country_code"] = df["country_code"].astype(str).str.upper()
    if "data_source" in df.columns and "data_version" in df.columns:
        df["indicator_id"] = df["data_source"] + "_" + df["data_version"]
    else:
        df["indicator_id"] = df.get("indicator_id", "unknown")

    bronze_path = BRONZE_DIR / "food_security_bronze.parquet"
    df.to_parquet(bronze_path, index=False)

    logging.info(f"Bronze layer written: {bronze_path}")


if __name__ == "__main__":
    build_bronze_food_security()
