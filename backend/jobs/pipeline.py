import asyncio
from datetime import datetime
from typing import Dict, Any, List
from backend.services.news_collector import news_collector
from backend.services.trend_collector import trend_collector
from backend.services.product_collector import product_collector
from backend.services.trend_analyzer import trend_analyzer
from backend.database.queries import upsert_trend_bundle, add_pipeline_log, get_all_trends
from backend.utils.logging import get_logger

logger = get_logger("pipeline")

# Realtime SSE listeners list
active_realtime_queues: List[asyncio.Queue] = []

async def broadcast_realtime_event(event_type: str, data: Dict[str, Any]):
    dead_queues = []
    for q in active_realtime_queues:
        try:
            await q.put({"event": event_type, "data": data})
        except Exception:
            dead_queues.append(q)
    for dq in dead_queues:
        if dq in active_realtime_queues:
            active_realtime_queues.remove(dq)

class IngestionPipeline:
    def __init__(self):
        self.is_running = False
        self.last_run: str = None

    async def run_pipeline(self) -> Dict[str, Any]:
        if self.is_running:
            logger.info("Pipeline already executing, skipping duplicate trigger.")
            return {"status": "busy", "message": "Pipeline execution currently in progress."}

        self.is_running = True
        start_time = datetime.utcnow()
        logger.info("=== STARTING TRENDLOOM REAL DATA INGESTION PIPELINE ===")

        try:
            # 1. Fetch real external signals in parallel
            news_task = news_collector.collect_all_news()
            search_task = trend_collector.fetch_search_trends()
            product_task = product_collector.collect_product_signals()

            news_articles, search_signals, product_signals = await asyncio.gather(
                news_task, search_task, product_task
            )

            await add_pipeline_log(
                event_type="COLLECTION_COMPLETE",
                source="Multi-Channel Collector",
                message=f"Fetched {len(news_articles)} news, {len(search_signals)} search, {len(product_signals)} catalog signals."
            )

            # 2. Analyze & Synthesize
            bundles = await trend_analyzer.analyze_and_synthesize(
                news_articles, search_signals, product_signals
            )

            # 3. Store bundles in Database / Supabase
            for b in bundles:
                await upsert_trend_bundle(
                    trend=b["trend"],
                    attributes=b["attributes"],
                    signals=b["signals"],
                    sources=b["sources"],
                    history=b["history"],
                    insights=b["insights"],
                    retail_rec=b["retail_recommendation"]
                )

            self.last_run = datetime.utcnow().isoformat() + "Z"
            all_trends = await get_all_trends()

            # 4. Broadcast to Realtime SSE clients
            await broadcast_realtime_event("trends_updated", {
                "trends_count": len(all_trends),
                "timestamp": self.last_run,
                "status": "COMPLETED"
            })

            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"=== PIPELINE COMPLETED IN {elapsed:.2f}s WITH {len(bundles)} TRENDS ===")

            return {
                "status": "success",
                "trends_updated": len(bundles),
                "news_signals": len(news_articles),
                "search_signals": len(search_signals),
                "duration_seconds": round(elapsed, 2),
                "timestamp": self.last_run
            }

        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            await add_pipeline_log(
                event_type="PIPELINE_ERROR",
                source="Pipeline Orchestrator",
                message=str(e)
            )
            return {"status": "error", "message": str(e)}
        finally:
            self.is_running = False

pipeline = IngestionPipeline()
