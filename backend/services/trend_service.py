from typing import List, Dict, Any, Optional
from backend.database.queries import (
    get_all_trends, get_trend_detail, get_trend_history, get_trend_sources
)
from backend.database.models import Trend, TrendDetailResponse, TrendObservation, TrendSource
from backend.utils.validation import sanitize_search_query

class TrendService:
    @staticmethod
    async def get_live_trends(limit: int = 20) -> List[Trend]:
        trends = await get_all_trends()
        # Sort by trend_score descending
        trends.sort(key=lambda t: t.trend_score, reverse=True)
        return trends[:limit]

    @staticmethod
    async def get_trend_by_id(trend_id: str) -> Optional[TrendDetailResponse]:
        return await get_trend_detail(trend_id)

    @staticmethod
    async def search(query: str) -> List[Trend]:
        clean_q = sanitize_search_query(query)
        if not clean_q:
            return []
        return await get_all_trends({"search": clean_q})

    @staticmethod
    async def filter_trends(filters: Dict[str, Any]) -> List[Trend]:
        return await get_all_trends(filters)

    @staticmethod
    async def get_history(trend_id: str) -> List[TrendObservation]:
        return await get_trend_history(trend_id)

    @staticmethod
    async def get_sources(trend_id: str) -> List[TrendSource]:
        return await get_trend_sources(trend_id)

trend_service = TrendService()
