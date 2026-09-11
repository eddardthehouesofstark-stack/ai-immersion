from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from backend.services.trend_service import trend_service
from backend.database.queries import get_dashboard_kpis, get_regional_summary
from backend.database.models import (
    Trend, TrendDetailResponse, TrendObservation, TrendSource, RegionalResponse
)

router = APIRouter(tags=["Trends"])

@router.get("/trends/live", summary="Get live trends with dashboard summary")
async def get_live_trends():
    """
    Returns real currently detected fashion trends and computed KPIs.
    """
    trends = await trend_service.get_live_trends()
    stats = await get_dashboard_kpis()
    fastest = max(trends, key=lambda t: t.growth_rate) if trends else None

    return {
        "trends": [t.model_dump() for t in trends],
        "stats": {
            "active_trends_count": len(trends),
            "rising_trends_count": sum(1 for t in trends if t.status in ("RISING", "EXPLODING")),
            "fastest_growing": {
                "name": fastest.name if fastest else "N/A",
                "growth_rate": fastest.growth_rate if fastest else 0.0
            } if fastest else None,
            "sources_count": stats.sources_tracked,
            "last_updated": stats.last_updated
        }
    }

@router.get("/trends", response_model=List[Trend], summary="Query and filter trends")
async def get_trends(
    category: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    minScore: Optional[int] = Query(None),
    minimum_score: Optional[int] = Query(None),
    maxScore: Optional[int] = Query(None),
    maximum_score: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    fabric: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    page: Optional[int] = Query(1),
    limit: Optional[int] = Query(50)
):
    """
    Backend multi-criteria filtering across category, gender, region, status, minimum_score, and keyword attributes.
    """
    filters = {
        "category": category,
        "gender": gender,
        "region": region,
        "status": status,
        "minScore": minScore or minimum_score,
        "maxScore": maxScore or maximum_score,
        "search": search,
        "fabric": fabric,
        "color": color
    }
    trends = await trend_service.filter_trends(filters)
    # Apply pagination slice
    offset = (page - 1) * limit
    return trends[offset : offset + limit]

@router.get("/trends/regional/{region}", response_model=RegionalResponse, summary="Get trends for a specific region")
async def get_regional_trends_by_path(region: str):
    return await get_regional_summary(region)

@router.get("/trends/search", response_model=List[Trend], summary="Search trends with keyword matching")
async def search_trends(q: str = Query("", description="Keyword search query (e.g. saree, linen, kanchipuram)")):
    """
    Performs full partial matching across name, description, region, category, fabrics, and silhouettes.
    """
    return await trend_service.search(q)

@router.get("/trends/{trend_id}", response_model=TrendDetailResponse, summary="Get comprehensive trend intelligence detail")
async def get_trend_detail(trend_id: str):
    detail = await trend_service.get_trend_by_id(trend_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Trend '{trend_id}' not found in database.")
    return detail


@router.get("/trends/{trend_id}/history", summary="Get historical observations for trend")
async def get_trend_history(trend_id: str):
    history = await trend_service.get_history(trend_id)
    return {
        "trend_id": trend_id,
        "history": [h.model_dump() for h in history]
    }

@router.get("/trends/{trend_id}/sources", response_model=List[TrendSource], summary="Get sources for trend")
async def get_trend_sources(trend_id: str):
    return await trend_service.get_sources(trend_id)
