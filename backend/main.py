import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from backend.api import (
    dashboard,
    trends,
    search,
    regional,
    forecast,
    intelligence,
    sources,
    products,
    system
)
from backend.jobs.scheduler import scheduler
from backend.utils.logging import get_logger

logger = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting TrendLoom FastAPI Backend...")
    # Start the scheduled background data collection
    scheduler.start()
    yield
    logger.info("Shutting down TrendLoom background tasks...")
    scheduler.stop()

app = FastAPI(
    title="TrendLoom Intelligence API",
    description="Real-Time Fashion Trend Intelligence Engine powered by FastAPI, Supabase PostgreSQL, and Gemini AI.",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all API routers under /api
app.include_router(dashboard.router, prefix="/api")
app.include_router(trends.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(regional.router, prefix="/api")
app.include_router(forecast.router, prefix="/api")
app.include_router(intelligence.router, prefix="/api")
app.include_router(sources.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(system.router, prefix="/api")

# Mount frontend static directory if exists (for standalone execution)
frontend_dir = Path("frontend")
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    return {
        "app": "TrendLoom Fashion Intelligence Platform",
        "docs": "/api/docs",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("FASTAPI_PORT", 8002))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
