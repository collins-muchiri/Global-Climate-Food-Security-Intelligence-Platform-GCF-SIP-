"""API entrypoint for GCF-SIP.
Minimal FastAPI app with health endpoint for Step 1 foundation.
"""

from fastapi import FastAPI
from .routes import ingest as ingest_routes

app = FastAPI(title="GCF-SIP API")


@app.get("/health")
async def health():
    return {"status": "ok"}

# Ingest routes
app.include_router(ingest_routes.router, prefix="/ingest")


if __name__ == "__main__":  # pragma: no cover
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
