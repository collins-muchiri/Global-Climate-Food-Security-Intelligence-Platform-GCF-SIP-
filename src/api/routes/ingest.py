"""Ingestion API routes (Step 2).

Exposes a minimal endpoint to trigger ingestion via the orchestrator.
"""

from fastapi import APIRouter

from src.ingestion.ingest_pipeline import run_all_ingestion

router = APIRouter()


@router.post("/trigger")
def trigger_ingestion():
    return run_all_ingestion()
