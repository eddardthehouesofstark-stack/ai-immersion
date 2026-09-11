from typing import Dict, Any, List
from backend.database.queries import get_regional_summary, get_all_trends
from backend.database.models import RegionalResponse
from backend.utils.validation import validate_region
from backend.utils.logging import get_logger

logger = get_logger("regional_service")

class RegionalService:
    @staticmethod
    async def get_regional_data(region: str) -> RegionalResponse:
        clean_region = validate_region(region)
        return await get_regional_summary(clean_region)

    @staticmethod
    async def get_all_regions_overview() -> Dict[str, Any]:
        trends = await get_all_trends()
        regions = [
            "Tamil Nadu",
            "India",
            "Kerala",
            "Karnataka",
            "Maharashtra",
            "Delhi",
            "West Bengal"
        ]
        summary = {}
        for r in regions:
            r_trends = [t for t in trends if t.region.lower() == r.lower()]
            avg_score = round(sum(t.trend_score for t in r_trends) / len(r_trends), 1) if r_trends else 0
            summary[r] = {
                "active_trends": len(r_trends),
                "average_trend_score": avg_score,
                "top_trend": r_trends[0].name if r_trends else "Signals Calibrating",
                "status": "active" if r_trends else "collecting"
            }
        return summary

regional_service = RegionalService()
