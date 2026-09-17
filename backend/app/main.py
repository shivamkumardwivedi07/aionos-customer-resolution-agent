"""FastAPI Application Entrypoint for Customer Resolution Agent."""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from app.api.routes import router
from app.config import HOST, PORT

app = FastAPI(
    title="AIONOS Airline Customer Resolution Agent",
    description="Deterministic & Grounded Customer-Facing Disruption Resolution Agent",
    version="1.0.0"
)

# Enable CORS for local Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router, prefix="/api")

# Serve built frontend static assets if present
STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/")
    async def serve_index():
        return FileResponse(STATIC_DIR / "index.html")
else:
    @app.get("/")
    async def root():
        return {
            "message": "AIONOS Customer Resolution Agent API is Online",
            "docs": "/docs",
            "health": "/api/health",
            "scenarios": "/api/scenarios"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
