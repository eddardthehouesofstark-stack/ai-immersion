from fastapi import APIRouter
from backend.database.queries import get_dashboard_kpis
from backend.database.models import DashboardStats

router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard", response_model=DashboardStats, summary="Get high-level dashboard metrics")
async def get_dashboard():
    """
    Returns real computed aggregate metrics calculated directly from database records:
    - live_trends count
    - rising_trends count
    - fastest_growing rate
    - sources_tracked count
    - signals_analyzed count
    - last_updated timestamp
    - system_status
    """
    return await get_dashboard_kpis()
