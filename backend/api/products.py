from fastapi import APIRouter
from backend.services.product_collector import product_collector

router = APIRouter(tags=["Products"])

@router.get("/products/signals", summary="Get catalog product assortment and guild signals")
async def get_product_signals():
    return await product_collector.collect_product_signals()
