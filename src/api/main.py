"""API entrypoint for GCF-SIP.
Minimal FastAPI app with health endpoint for Step 1 foundation.
"""

from fastapi import FastAPI

app = FastAPI(title="GCF-SIP API")


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":  # pragma: no cover
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
