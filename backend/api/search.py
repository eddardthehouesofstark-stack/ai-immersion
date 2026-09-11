from fastapi import APIRouter, Query
from typing import List
from backend.services.trend_service import trend_service
from backend.database.models import Trend

router = APIRouter(tags=["Search"])

@router.get("/trends/search", response_model=List[Trend], summary="Search trends with keyword matching")
async def search_trends(q: str = Query("", description="Keyword search query (e.g. saree, linen, kanchipuram)")):
    """
    Performs full partial matching across name, description, region, category, fabrics, and silhouettes.
    """
    return await trend_service.search(q)
