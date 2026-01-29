"""
FAOSTAT Food Security Ingestion Pipeline
---------------------------------------

Purpose:
- Ingest food security indicators from FAOSTAT
- Persist immutable raw data
- Standardize schema for downstream analytics
- Attach metadata and data quality signals

Standards:
- No silent failures
- No transformations in raw layer
- ISO3 country codes enforced
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
import requests
from requests.exceptions import RequestException

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

FAOSTAT_BASE_URL = "https://fenixservices.fao.org/faostat/api/v1/en"
DOMAIN = "FS"  # Food Security domain (currently unstable upstream)

ITEM_CODES = [
    "21004",  # Prevalence of undernourishment
    "21030",  # Food insecurity experience scale (moderate or severe)
]

RAW_DATA_DIR = Path("data/raw/faostat")
INTERIM_DATA_DIR = Path("data/interim/standardized")

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DATA_DIR.mkdir(parents=True, exist_ok=True)

INGESTION_TIMESTAMP = datetime.utcnow().isoformat()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -------------------------------------------------------------------
# Health & Fetch Helpers
# -------------------------------------------------------------------


def check_domain_health(domain: str) -> bool:
    """Check whether FAOSTAT domain is reachable."""
    try:
        response = requests.get(
            f"{FAOSTAT_BASE_URL}/{domain}",
            timeout=10
        )
        return response.status_code == 200
    except RequestException:
        return False


def fetch_faostat_data(item_code: str, retries: int = 3) -> pd.DataFrame:
    """Fetch FAOSTAT data with retry and backoff."""
    url = f"{FAOSTAT_BASE_URL}/{DOMAIN}"
    params = {
        "item_code": item_code,
        "area_code": "all",
        "year": "all"
    }

    last_error = None

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=30)

            # Explicit upstream failure detection
            if response.status_code == 521:
                raise RuntimeError("FAOSTAT upstream unavailable (521)")

            response.raise_for_status()

            payload = response.json()
            if "data" not in payload:
                raise ValueError("FAOSTAT response missing 'data' field")

            df = pd.DataFrame(payload["data"])
            logging.info(
                f"Fetched {len(df)} rows for item_code={item_code}"
            )
            return df

        except Exception as e:
            last_error = e
            logging.warning(
                f"Attempt {attempt}/{retries} failed "
                f"for item_code={item_code}: {e}"
            )

            if attempt < retries:
                sleep_time = 2 ** attempt
                logging.info(f"Retrying in {sleep_time}s...")
                time.sleep(sleep_time)

    raise RuntimeError(
        f"FAOSTAT fetch failed after {retries} attempts: {last_error}"
    )

# -------------------------------------------------------------------
# Standardization & Quality
# -------------------------------------------------------------------


def standardize_schema(df: pd.DataFrame, item_code: str) -> pd.DataFrame:
    """Standardize FAOSTAT schema to canonical analytical spine."""
    required_columns = {
        "Area Code (ISO3)": "country_code",
        "Year": "year",
        "Value": "indicator_value",
        "Item": "indicator_name"
    }

    missing = set(required_columns.keys()) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    standardized = (
        df[list(required_columns.keys())]
        .rename(columns=required_columns)
        .assign(
            data_source="FAOSTAT",
            data_version=f"{DOMAIN}_{item_code}",
            ingestion_timestamp=INGESTION_TIMESTAMP
        )
    )

    standardized["year"] = standardized["year"].astype(int)
    standardized["indicator_value"] = pd.to_numeric(
        standardized["indicator_value"], errors="coerce"
    )

    return standardized


def compute_quality_score(df: pd.DataFrame) -> pd.Series:
    """Compute simple data quality score (0–1)."""
    completeness = 1.0 - df["indicator_value"].isna().mean()
    coverage = df["year"].nunique() / (
        df["year"].max() - df["year"].min() + 1
    )

    score = 0.7 * completeness + 0.3 * min(coverage, 1.0)
    return pd.Series(score, index=df.index)

# -------------------------------------------------------------------
# Pipeline
# -------------------------------------------------------------------


def ingest_faostat(item_codes: List[str]) -> None:
    """Main ingestion pipeline with resilience controls."""

    if not check_domain_health(DOMAIN):
        logging.error(
            f"FAOSTAT domain '{DOMAIN}' is DOWN (521). "
            "Ingestion skipped safely."
        )
        return

    all_standardized = []
    failed_items = []

    for code in item_codes:
        logging.info(f"Starting ingestion for FAOSTAT item_code={code}")

        try:
            df_raw = fetch_faostat_data(code)

            # Persist raw data (immutable)
            raw_path = RAW_DATA_DIR / f"faostat_{DOMAIN.lower()}_{code}.parquet"
            df_raw.to_parquet(raw_path, index=False)
            logging.info(f"Raw data written to {raw_path}")

            # Standardize
            df_std = standardize_schema(df_raw, code)

            # Quality score
            df_std["quality_score"] = compute_quality_score(df_std)

            all_standardized.append(df_std)

        except Exception as e:
            logging.error(
                f"Ingestion failed for item_code={code}: {e}"
            )
            failed_items.append(code)

    if not all_standardized:
        logging.error("No FAOSTAT data ingested — pipeline exiting")
        return

    final_df = pd.concat(all_standardized, ignore_index=True)

    interim_path = INTERIM_DATA_DIR / "faostat_food_security.parquet"
    final_df.to_parquet(interim_path, index=False)

    metadata = {
        "source": "FAOSTAT",
        "domain": DOMAIN,
        "items_requested": item_codes,
        "items_ingested": list(set(item_codes) - set(failed_items)),
        "items_failed": failed_items,
        "rows": len(final_df),
        "ingestion_timestamp": INGESTION_TIMESTAMP,
        "domain_health": "healthy"
    }

    with open(
        INTERIM_DATA_DIR / "faostat_food_security_metadata.json", "w"
    ) as f:
        json.dump(metadata, f, indent=2)

    logging.info("FAOSTAT ingestion completed successfully")

# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    ingest_faostat(ITEM_CODES)
