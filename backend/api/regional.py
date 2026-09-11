from fastapi import APIRouter
from backend.services.regional_service import regional_service
from backend.database.models import RegionalResponse
from typing import Dict, Any

router = APIRouter(tags=["Regional"])

@router.get("/regional", summary="Get all regions intelligence overview")
async def get_all_regions():
    return await regional_service.get_all_regions_overview()

@router.get("/regional/{region}", response_model=RegionalResponse, summary="Get regional intelligence for state or hub")
async def get_region_data(region: str):
    return await regional_service.get_regional_data(region)
