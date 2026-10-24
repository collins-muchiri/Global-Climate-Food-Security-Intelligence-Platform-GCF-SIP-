"""Pinned, dated ingestion for the vertical slice.

Retrieval date is an explicit argument and is written into the output manifest, because undated
climate and agricultural data is unfalsifiable. Caches raw payloads so re-runs are reproducible
offline.
"""
import argparse, hashlib, json, os, urllib.request
from pathlib import Path

HERE = Path(__file__).parent
CACHE = HERE / "cache"


def fetch(url: str) -> bytes:
    CACHE.mkdir(exist_ok=True)
    key = hashlib.sha256(url.encode()).hexdigest()[:16]
    path = CACHE / key
    if path.exists():
        return path.read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": "gcf-sip-slice/0.1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    path.write_bytes(data)
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--retrieval-date", required=True, help="ISO date this retrieval was performed")
    ap.add_argument("--country", default="Kenya")
    ap.add_argument("--indicator", default="food-supply-per-capita")
    a = ap.parse_args()
    # FAOSTAT or climate endpoint URL assembled here; keep the query explicit and versioned.
    url = os.environ.get("SLICE_SOURCE_URL", "")
    if not url:
        raise SystemExit("Set SLICE_SOURCE_URL to the exact FAOSTAT or climate API query for this slice.")
    raw = fetch(url)
    manifest = {"retrieval_date": a.retrieval_date, "country": a.country, "indicator": a.indicator,
                "source_url": url, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    (HERE / "raw_manifest.json").write_text(json.dumps(manifest, indent=2))
    (HERE / "raw_payload.bin").write_bytes(raw)
    print("ingested", manifest["sha256"][:12], manifest["bytes"], "bytes on", a.retrieval_date)


if __name__ == "__main__":
    main()
