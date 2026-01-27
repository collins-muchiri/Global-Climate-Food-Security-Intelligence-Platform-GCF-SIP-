"""FAOSTAT-like Food Security ingestion module with resilience."""

from __future__ import annotations

import os
import time
import urllib.request
import urllib.error


def ingest_food_security():
    """Ingest food-security data from a FAOSTAT-like API with retry/backoff.

    The API URL is read from the FAOSTAT_API_URL environment variable. A simple
    retry policy is supported via FAOSTAT_RETRIES and FAOSTAT_BACKOFF.
    """
    url = os.environ.get("FAOSTAT_API_URL")
    if not url:
        return {
            "status": "not_configured",
            "note": "FAOSTAT_API_URL environment variable is not set",
        }

    try:
        max_retries = int(os.environ.get("FAOSTAT_RETRIES", "3"))
    except ValueError:
        max_retries = 3
    try:
        backoff = float(os.environ.get("FAOSTAT_BACKOFF", "1.0"))
    except ValueError:
        backoff = 1.0

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = resp.read()
                preview = data[:200].decode("utf-8", errors="replace")
                return {
                    "status": "success",
                    "attempt": attempt,
                    "size_bytes": len(data),
                    "preview": preview,
                }
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            last_error = str(e)
        except Exception as e:  # pragma: no cover
            last_error = repr(e)
        time.sleep(backoff * attempt)

    return {"status": "failed", "attempts": max_retries, "last_error": last_error}
