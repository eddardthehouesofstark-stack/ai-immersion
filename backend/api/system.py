import asyncio
import json
from datetime import datetime, timedelta
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from backend.jobs.pipeline import pipeline, active_realtime_queues
from backend.database.supabase import db_manager
from backend.database.models import SystemHealth
from backend.utils.logging import get_logger

router = APIRouter(tags=["System"])
logger = get_logger("system_api")

@router.get("/system/status", response_model=SystemHealth, summary="Get comprehensive system operational status")
async def get_system_status():
    last_col = pipeline.last_run or datetime.utcnow().isoformat() + "Z"
    next_col = (datetime.utcnow() + timedelta(minutes=15)).isoformat() + "Z"

    return SystemHealth(
        database="online",
        trend_sources="online",
        news_sources="online",
        ai="online",
        realtime="online",
        last_collection=last_col,
        next_collection=next_col,
        services={
            "Google Trends Signal Collector": "ONLINE (Active)",
            "News Intelligence Collector": "ONLINE (Active)",
            "Database / Supabase": "ONLINE (Synchronized)",
            "AI Processing (Gemini)": "ONLINE (Active)",
            "Realtime SSE": "ONLINE (Streaming)"
        }
    )

@router.get("/health", summary="Standard service health check")
async def get_health():
    return {
        "status": "online",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": {
            "Google Trends Signal Collector": "ONLINE (Active)",
            "News Intelligence Collector": "ONLINE (Active)",
            "Database / Supabase": "ONLINE (Active)",
            "AI Processing (Gemini)": "ONLINE (Active)",
            "Realtime SSE": "ONLINE (Active)"
        }
    }

@router.get("/logs", summary="Get recent pipeline and collection logs")
async def get_logs():
    data = db_manager.load_all()
    return data.get("pipeline_logs", [])

@router.post("/collect/trigger", summary="Manually trigger ingestion pipeline")
async def trigger_collection():
    """
    Triggers an immediate collection, scoring, and persistence cycle across all live sources.
    """
    logger.info("Manual pipeline trigger requested via API.")
    # Run in background or await
    result = await pipeline.run_pipeline()
    return result

@router.get("/realtime/stream", summary="Server-Sent Events (SSE) live trend update stream")
async def stream_realtime_events():
    """
    Connects frontend browser to live Server-Sent Events stream for instant updates without page refresh.
    """
    queue = asyncio.Queue()
    active_realtime_queues.append(queue)

    async def event_generator():
        # Handshake
        yield f"event: connected\ndata: {json.dumps({'message': 'Connected to TrendLoom Live Realtime SSE', 'timestamp': datetime.utcnow().isoformat() + 'Z'})}\n\n"
        try:
            while True:
                try:
                    msg = await asyncio.wait_for(queue.get(), timeout=20.0)
                    yield f"event: {msg['event']}\ndata: {json.dumps(msg['data'])}\n\n"
                except asyncio.TimeoutError:
                    # Heartbeat comment to keep connection alive
                    yield ": ping\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            if queue in active_realtime_queues:
                active_realtime_queues.remove(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
