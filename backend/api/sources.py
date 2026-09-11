from fastapi import APIRouter
from typing import List, Dict, Any
from backend.database.supabase import db_manager
from backend.services.trend_service import trend_service
from backend.services.news_collector import RSS_FEEDS
from backend.database.models import TrendSource

router = APIRouter(tags=["Sources"])

@router.get("/sources", summary="Get all verified sources and feeds tracked by the platform")
async def get_all_sources():
    data = db_manager.load_all()
    raw_sources = data.get("sources", [])
    
    all_sources = []
    seen_urls = set()

    # If sources is a dict
    if isinstance(raw_sources, dict):
        for srcs in raw_sources.values():
            if isinstance(srcs, list):
                for s in srcs:
                    url = s.get("source_url")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        all_sources.append(s)
    elif isinstance(raw_sources, list):
        for s in raw_sources:
            url = s.get("source_url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_sources.append(s)

    # Also list active monitored RSS publishers
    active_publishers = [
        {
            "publisher": f.get("default_source"),
            "region": f.get("region"),
            "feed_url": f.get("url"),
            "type": "Monitored Fashion RSS"
        }
        for f in RSS_FEEDS
    ]

    return {
        "verified_articles": all_sources,
        "total_verified_signals": len(all_sources),
        "active_publishers": active_publishers,
        "total_monitored_outlets": len(active_publishers)
    }

@router.get("/trends/{trend_id}/sources", response_model=List[TrendSource], summary="Get sources for a specific trend")
async def get_trend_sources(trend_id: str):
    return await trend_service.get_sources(trend_id)
