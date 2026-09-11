from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class TrendStatus(str, Enum):
    EXPLODING = "EXPLODING"
    RISING = "RISING"
    STABLE = "STABLE"
    DECLINING = "DECLINING"
    FADING = "FADING"

class TrendBase(BaseModel):
    id: str
    name: str
    category: str
    gender: str = "Unisex"
    region: str = "India"
    trend_score: int = Field(ge=0, le=100)
    growth_rate: float
    velocity: float = 0.0
    status: TrendStatus
    forecast: str
    confidence: int = Field(ge=0, le=100)
    description: str
    image_url: Optional[str] = None
    source_count: int = 1
    last_updated: str

class Trend(TrendBase):
    pass

class TrendAttribute(BaseModel):
    attribute_type: str
    attribute_value: str
    confidence: int = 85

class TrendSignal(BaseModel):
    source: str = "Live Signal"
    signal_type: str = "search_velocity"
    signal_value: float = 85.0
    signal_strength: Optional[int] = None
    recorded_at: Optional[str] = None

class TrendSource(BaseModel):
    source_name: str
    title: str = "Verified Fashion Industry Article"
    source_url: str
    source_type: str = "News"
    published_at: Optional[str] = None
    collected_at: Optional[str] = None

class TrendObservation(BaseModel):
    timestamp: str = ""
    observation_date: str = ""
    score: int = 0
    growth_rate: float = 0.0
    recorded_score: Optional[int] = None

class TrendInsight(BaseModel):
    insight_type: str
    content: str
    generated_at: Optional[str] = None

class MarketplaceAvailability(BaseModel):
    retailer: str
    status: str
    price_range: str
    channel_type: str
    url: str
    fulfillment: str = "Pan-India Delivery"

class RetailRecommendation(BaseModel):
    recommendation: str = "TEST / STOCK"
    action: str = "Test / Stock"
    demand: str = "HIGH"
    price_segment: str = "Bridge-to-Luxury"
    reason: str = "Strong cross-channel momentum observed."
    target_audience: str = "Heritage & Contemporary Festive Buyers"
    risk: str = "Low"
    timing: str = "Next 30-45 Days"
    notes: str = "Prioritize key colors and artisanal weaves."

class TrendDetailResponse(BaseModel):
    trend: Trend
    attributes: Dict[str, Any] = {}
    signals: List[TrendSignal] = []
    sources: List[TrendSource] = []
    availabilities: List[MarketplaceAvailability] = []
    history: List[TrendObservation] = []
    insights: List[TrendInsight] = []
    retail_recommendation: Optional[RetailRecommendation] = None


class DashboardStats(BaseModel):
    live_trends: int
    rising_trends: int
    fastest_growing: float
    sources_tracked: int
    signals_analyzed: int
    last_updated: str
    system_status: str = "online"

class DashboardOverviewResponse(BaseModel):
    trends: List[Trend]
    stats: Dict[str, Any]

class PopularFabric(BaseModel):
    name: str
    count: int

class PopularColor(BaseModel):
    name: str

class RegionalResponse(BaseModel):
    region: str
    trends: List[Trend]
    popular_fabrics: List[PopularFabric] = []
    popular_colors: List[PopularColor] = []
    regional_confidence: int = 85

class ForecastItem(BaseModel):
    trend: Trend
    demand: str
    recommendation: str
    confidence: int

class AskAnalystRequest(BaseModel):
    question: str

class AskAnalystResponse(BaseModel):
    answer: str
    supporting_trends: List[str] = []
    sources: List[Dict[str, str]] = []
    data_timestamp: str
    confidence: int = 90
    cached: bool = False

class SystemHealth(BaseModel):
    database: str = "online"
    trend_sources: str = "online"
    news_sources: str = "online"
    ai: str = "online"
    realtime: str = "online"
    last_collection: str
    next_collection: str
    services: Dict[str, str] = {}
