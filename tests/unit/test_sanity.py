"""Replaces the former `assert 1 == 1` sanity test (rule-4.9 theatre: it could
never fail, so it certified nothing). These assert real project invariants."""
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_src_package_imports():
    import importlib

    # importlib keeps "the import is the assertion" without noqa suppressions
    importlib.import_module("src")
    importlib.import_module("src.utils.config")


def test_fastapi_app_registers_the_health_route():
    from src.api.main import app

    paths = {getattr(r, "path", None) for r in app.routes}
    assert "/health" in paths, f"health route missing from app: {sorted(p for p in paths if p)}"
    assert any(p and p.startswith("/ingest") for p in paths), "ingest router not mounted"


def test_pyproject_declares_an_installable_package_layout():
    # Regression for the defect that made `pip install -e .` impossible:
    # Poetry requires an explicit packages declaration for the src/ layout.
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    packages = data["tool"]["poetry"].get("packages")
    assert packages, "poetry packages declaration missing again"
    assert any(pkg.get("include") == "src" for pkg in packages)


def test_lakehouse_layout_constants_are_relative_data_paths():
    from src.lakehouse import bronze_food_security as bronze

    assert bronze.INTERIM_DIR == Path("data/interim/standardized")
    assert bronze.BRONZE_DIR == Path("data/bronze/faostat")


def test_ingestion_orchestrator_reports_every_stream_explicitly():
    # Regression for the swallowed-ImportError defect: the orchestrator must
    # return a labelled status for ALL THREE streams (never silently None).
    from src.ingestion.ingest_pipeline import run_all_ingestion

    results = run_all_ingestion()
    assert set(results) == {"climate", "food_security", "economics"}
    for stream, res in results.items():
        assert isinstance(res, dict), f"{stream} result must be a dict, got {res!r}"
        assert "status" in res, f"{stream} result must carry an explicit status"
