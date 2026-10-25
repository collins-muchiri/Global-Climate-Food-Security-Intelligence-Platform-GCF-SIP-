"""Data ingestion orchestration (Step 2 scaffolding).

This module calls the existing ingestion stubs from Step 1 and aggregates their
status. It is intentionally lightweight to provide a deterministic, auditable
entry point for orchestration in Step 2.
"""

from typing import Dict

# Direct package imports (the project is installable since the packaging fix).
# The former try/except flat-import fallback silently set ALL THREE functions
# to None whenever any single name failed to import - and
# `ingest_food_security` never existed (the module exposes
# `ingest_faostat(item_codes)`), so every orchestration call quietly returned
# "not_implemented" while the API looked healthy. Imports are now unconditional
# and the missing zero-arg wrapper is explicit below.
from src.ingestion.climate_ingest import ingest_climate
from src.ingestion.economics_ingest import ingest_economics


def ingest_food_security():
    """Explicit placeholder: food-security ingestion requires item codes.

    Call src.ingestion.food_security_ingest.ingest_faostat(item_codes) directly;
    returning a labelled status beats a silent None from a swallowed ImportError.
    """
    return {"status": "not_implemented", "reason": "call ingest_faostat(item_codes)"}


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
