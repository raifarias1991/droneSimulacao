from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from app.main import router as ai_router


def create_app() -> FastAPI:
    app = FastAPI(title="Drone Simulation AI API")
    app.include_router(ai_router)
    return app


app = create_app()
