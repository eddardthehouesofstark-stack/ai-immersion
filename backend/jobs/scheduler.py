import asyncio
from backend.jobs.pipeline import pipeline
from backend.utils.logging import get_logger

logger = get_logger("scheduler")

class CollectionScheduler:
    def __init__(self, interval_seconds: int = 900): # 15 minutes default
        self.interval = interval_seconds
        self.task: asyncio.Task = None
        self._stop_event = asyncio.Event()

    async def _loop(self):
        logger.info(f"Scheduled data collection loop running every {self.interval} seconds.")
        # Run initial collection on startup
        try:
            await pipeline.run_pipeline()
        except Exception as e:
            logger.warning(f"Initial pipeline run encountered: {e}")

        while not self._stop_event.is_set():
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval)
            except asyncio.TimeoutError:
                # Interval elapsed, trigger collection
                logger.info("Scheduler triggering periodic fashion data collection...")
                try:
                    await pipeline.run_pipeline()
                except Exception as e:
                    logger.error(f"Scheduled pipeline run failed: {e}")

    def start(self):
        if not self.task or self.task.done():
            self._stop_event.clear()
            self.task = asyncio.create_task(self._loop())

    def stop(self):
        if self.task:
            self._stop_event.set()
            self.task.cancel()

scheduler = CollectionScheduler()
