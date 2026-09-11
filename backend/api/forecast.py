from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.services.trend_service import trend_service
from backend.services.forecast_service import forecast_service

router = APIRouter(tags=["Forecast"])

@router.get("/forecast", summary="Get commercial forecast and demand signals for all trends")
async def get_forecast_summary():
    trends = await trend_service.get_live_trends()
    results = []
    for t in trends:
        history = await trend_service.get_history(t.id)
        f_data = forecast_service.calculate_forecast(t, history)
        results.append({
            "trend_id": t.id,
            "trend_name": t.name,
            "category": t.category,
            "region": t.region,
            "score": t.trend_score,
            "growth_rate": t.growth_rate,
            "status": t.status,
            **f_data
        })
    return results

@router.get("/forecast/{trend_id}", summary="Get forecast projection for a specific trend")
async def get_trend_forecast(trend_id: str):
    detail = await trend_service.get_trend_by_id(trend_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Trend '{trend_id}' not found.")
    
    history = await trend_service.get_history(trend_id)
    f_data = forecast_service.calculate_forecast(detail.trend, history)
    return {
        "trend_id": trend_id,
        "trend_name": detail.trend.name,
        **f_data
    }
