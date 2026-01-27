"""Data ingestion orchestration (Step 2 scaffolding).

This module calls the existing ingestion stubs from Step 1 and aggregates their
status. It is intentionally lightweight to provide a deterministic, auditable
entry point for orchestration in Step 2.
"""

from typing import Dict

try:
    from climate_ingest import ingest_climate  # type: ignore
    from food_security_ingest import ingest_food_security  # type: ignore
    from economics_ingest import ingest_economics  # type: ignore
except Exception:  # pragma: no cover
    ingest_climate = None  # type: ignore
    ingest_food_security = None  # type: ignore
    ingest_economics = None  # type: ignore


def run_all_ingestion() -> Dict[str, Dict[str, object]]:
    results: Dict[str, Dict[str, object]] = {}
    if ingest_climate:
        results["climate"] = ingest_climate()
    else:
        results["climate"] = {"status": "not_implemented"}

    if ingest_food_security:
        results["food_security"] = ingest_food_security()
    else:
        results["food_security"] = {"status": "not_implemented"}

    if ingest_economics:
        results["economics"] = ingest_economics()
    else:
        results["economics"] = {"status": "not_implemented"}

    return results
