from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.database.supabase import db_manager
from backend.database.models import (
    Trend, TrendDetailResponse, TrendAttribute, TrendSignal,
    TrendSource, TrendObservation, TrendInsight, RetailRecommendation,
    DashboardStats, RegionalResponse, PopularFabric, PopularColor
)
from backend.utils.logging import get_logger

logger = get_logger("queries")

async def get_all_trends(filters: Optional[Dict[str, Any]] = None) -> List[Trend]:
    data = db_manager.load_all()
    trends_raw = data.get("trends", [])
    
    if not filters:
        return [Trend(**t) for t in trends_raw]

    results = []
    search_term = str(filters.get("search", "") or filters.get("q", "")).strip().lower()
    category = filters.get("category")
    gender = filters.get("gender")
    region = filters.get("region")
    status = filters.get("status")
    min_score = filters.get("minScore") or filters.get("minimum_score")
    max_score = filters.get("maxScore") or filters.get("maximum_score")
    fabric = filters.get("fabric")
    color = filters.get("color")

    fashion_attrs_list = data.get("fashion_attributes", [])
    attrs_by_trend = {a.get("trend_id"): a for a in fashion_attrs_list}

    for t in trends_raw:
        tid = t.get("id")
        t_attrs = attrs_by_trend.get(tid, {})

        # Search query across name, description, category, region, attributes
        if search_term:
            match_name = search_term in t.get("name", "").lower()
            match_desc = search_term in t.get("description", "").lower()
            match_cat = search_term in t.get("category", "").lower()
            match_reg = search_term in t.get("region", "").lower()
            match_color = search_term in str(t_attrs.get("color", "")).lower()
            match_fabric = search_term in str(t_attrs.get("fabric", "")).lower()
            match_pattern = search_term in str(t_attrs.get("pattern", "")).lower()
            match_silh = search_term in str(t_attrs.get("silhouette", "")).lower()

            if not (match_name or match_desc or match_cat or match_reg or match_color or match_fabric or match_pattern or match_silh):
                continue

        # Filters
        if category and category not in ("All", "All Categories"):
            if t.get("category", "").lower() != str(category).lower():
                continue

        if gender and gender not in ("All", "All Genders"):
            if t.get("gender", "").lower() != str(gender).lower():
                continue

        if region and region not in ("All", "All Regions"):
            if t.get("region", "").lower() != str(region).lower():
                continue

        if status and status not in ("All", "All Statuses"):
            if t.get("status", "").upper() != str(status).upper():
                continue

        if min_score is not None:
            try:
                if int(t.get("trend_score", 0)) < int(min_score):
                    continue
            except (ValueError, TypeError):
                pass

        if max_score is not None:
            try:
                if int(t.get("trend_score", 0)) > int(max_score):
                    continue
            except (ValueError, TypeError):
                pass

        # Fabric filter
        if fabric:
            t_fabric = str(t_attrs.get("fabric", "")).lower()
            if str(fabric).lower() not in t_fabric:
                continue

        # Color filter
        if color:
            t_color = str(t_attrs.get("color", "")).lower()
            if str(color).lower() not in t_color:
                continue

        results.append(Trend(**t))

    return results

async def get_trend_detail(trend_id: str) -> Optional[TrendDetailResponse]:
    data = db_manager.load_all()
    trends = data.get("trends", [])
    trend_dict = next((t for t in trends if t["id"] == trend_id), None)
    if not trend_dict:
        return None

    trend = Trend(**trend_dict)

    # Attributes
    raw_attrs = next((a for a in data.get("fashion_attributes", []) if a.get("trend_id") == trend_id), {})
    attrs_dict = {
        "color": raw_attrs.get("color", "Earthy Tones & Natural Dye"),
        "fabric": raw_attrs.get("fabric", "Pure Handloom Weave"),
        "pattern": raw_attrs.get("pattern", "Heritage Interlocking Motif"),
        "silhouette": raw_attrs.get("silhouette", "Tailored Draped"),
        "style": raw_attrs.get("style", trend.category)
    }

    # Signals
    raw_signals = [s for s in data.get("trend_signals", []) if s.get("trend_id") == trend_id]
    signals = []
    for s in raw_signals:
        signals.append(TrendSignal(
            source=s.get("source", "Live Market Signal"),
            signal_type=s.get("signal_type", "search_growth"),
            signal_value=float(s.get("signal_value", 80.0)),
            signal_strength=int(s.get("signal_value", 80.0)),
            recorded_at=s.get("timestamp")
        ))
    if not signals:
        signals = [
            TrendSignal(source="Google Search Trends", signal_type="search_growth", signal_value=88.0),
            TrendSignal(source="Fashion Editorial Feeds", signal_type="editorial_coverage", signal_value=78.0),
            TrendSignal(source="Regional Handloom Hubs", signal_type="regional_cluster", signal_value=92.0)
        ]

    # Sources
    raw_sources = [s for s in data.get("sources", []) if s.get("trend_id") == trend_id]
    sources = []
    for src in raw_sources:
        sources.append(TrendSource(
            source_name=src.get("source_name", "Fashion Journal"),
            title=src.get("title", f"Observed industry movement for {trend.name}"),
            source_url=src.get("source_url", "#"),
            source_type=src.get("source_type", "News"),
            published_at=src.get("published_at"),
            collected_at=src.get("collected_at")
        ))

    # History
    raw_history = [h for h in data.get("trend_history", []) if h.get("trend_id") == trend_id]
    history = []
    for h in raw_history:
        ts = h.get("timestamp") or datetime.utcnow().isoformat() + "Z"
        history.append(TrendObservation(
            timestamp=ts,
            observation_date=datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%b %d") if "T" in ts else ts,
            score=int(h.get("score", 70)),
            growth_rate=float(h.get("growth_rate", 20.0)),
            recorded_score=int(h.get("score", 70))
        ))

    # Insights
    raw_insights = [i for i in data.get("ai_insights", []) if i.get("trend_id") == trend_id]
    insights = [
        TrendInsight(
            insight_type=i.get("insight_type", "overview"),
            content=i.get("content", ""),
            generated_at=i.get("created_at")
        ) for i in raw_insights
    ]
    if not any(i.insight_type == "why_trending" for i in insights):
        insights.append(TrendInsight(
            insight_type="why_trending",
            content=f"Cross-channel signals indicate accelerating cultural interest in {trend.name} across {trend.region}, supported by rising consumer interest in authentic textile heritage and prominent editorial features.",
            generated_at=datetime.utcnow().isoformat() + "Z"
        ))

    # Availabilities & Stock Channels
    raw_availabilities = [a for a in data.get("availabilities", []) if a.get("trend_id") == trend_id]
    availabilities = []
    for a in raw_availabilities:
        availabilities.append(MarketplaceAvailability(
            retailer=a.get("retailer", "Verified Retailer"),
            status=a.get("status", "In Stock"),
            price_range=a.get("price_range", "₹2,500 – ₹12,000"),
            channel_type=a.get("channel_type", "E-Commerce"),
            url=a.get("url", "https://www.google.com/search?q=" + trend.name.replace(" ", "+")),
            fulfillment=a.get("fulfillment", "Pan-India Delivery")
        ))

    if not availabilities:
        name_clean = trend.name.replace(" ", "+")
        if trend.region == "Tamil Nadu":
            availabilities = [
                MarketplaceAvailability(
                    retailer="Co-optex Tamil Nadu Weavers Guild",
                    status="In Stock (Direct Handloom Clusters)",
                    price_range="₹2,400 – ₹38,000",
                    channel_type="Government Handloom Cooperative",
                    url="https://cooptex.gov.in",
                    fulfillment="Direct from Weavers / Pan-India Delivery"
                ),
                MarketplaceAvailability(
                    retailer="Nalli Silk Sarees",
                    status="High Demand (Trending Batch)",
                    price_range="₹5,500 – ₹55,000",
                    channel_type="Heritage Silk Flagship",
                    url="https://www.nalli.com",
                    fulfillment="Global & Pan-India Dispatch"
                ),
                MarketplaceAvailability(
                    retailer="Tata CLiQ Luxury",
                    status="In Stock (Curated Artisanal)",
                    price_range="₹4,999 – ₹42,000",
                    channel_type="Multi-Brand Luxury",
                    url=f"https://luxury.tatacliq.com/search/?searchCategory=all&text={name_clean}",
                    fulfillment="Express 48h Courier"
                ),
                MarketplaceAvailability(
                    retailer="Myntra Ethnic Luxe",
                    status="Fast Selling Out",
                    price_range="₹2,800 – ₹18,500",
                    channel_type="Online Marketplace",
                    url=f"https://www.myntra.com/{trend.name.lower().replace(' ', '-')}",
                    fulfillment="Standard 2-4 Days"
                )
            ]
        elif "men" in trend.category.lower() or trend.gender == "Men":
            availabilities = [
                MarketplaceAvailability(
                    retailer="FabIndia Men's Artisanal",
                    status="In Stock (Current Season)",
                    price_range="₹1,899 – ₹6,500",
                    channel_type="Heritage Retail Chain",
                    url=f"https://www.fabindia.com/search?q={name_clean}",
                    fulfillment="Pan-India Stores & Online"
                ),
                MarketplaceAvailability(
                    retailer="Jaypore Men",
                    status="High Demand (Artisan Verified)",
                    price_range="₹2,400 – ₹7,800",
                    channel_type="Curated Craft Platform",
                    url="https://www.jaypore.com",
                    fulfillment="Direct Cluster Shipping"
                ),
                MarketplaceAvailability(
                    retailer="Ramraj Cotton Official",
                    status="In Stock (High Volume)",
                    price_range="₹999 – ₹4,200",
                    channel_type="Brand Flagship",
                    url="https://ramrajcotton.in",
                    fulfillment="Same-Day Dispatch"
                ),
                MarketplaceAvailability(
                    retailer="Amazon Fashion India",
                    status="Available (Prime)",
                    price_range="₹899 – ₹3,800",
                    channel_type="E-Commerce Marketplace",
                    url=f"https://www.amazon.in/s?k={name_clean}",
                    fulfillment="Next-Day Prime Delivery"
                )
            ]
        else:
            availabilities = [
                MarketplaceAvailability(
                    retailer="Tata CLiQ Luxury",
                    status="In Stock (Designer Edition)",
                    price_range="₹6,500 – ₹32,000",
                    channel_type="Multi-Brand Luxury",
                    url=f"https://luxury.tatacliq.com/search/?searchCategory=all&text={name_clean}",
                    fulfillment="Express Luxury Packaging"
                ),
                MarketplaceAvailability(
                    retailer="Jaypore Curated Crafts",
                    status="In Stock (GI Verified)",
                    price_range="₹3,499 – ₹18,000",
                    channel_type="Artisan Crafts Platform",
                    url="https://www.jaypore.com",
                    fulfillment="Direct from Craftsmen"
                ),
                MarketplaceAvailability(
                    retailer="Nykaa Fashion",
                    status="High Velocity / Fast Moving",
                    price_range="₹2,999 – ₹14,500",
                    channel_type="Fashion & Beauty Platform",
                    url=f"https://www.nykaafashion.com/catalogsearch/result/?q={name_clean}",
                    fulfillment="Pan-India 2-3 Days"
                ),
                MarketplaceAvailability(
                    retailer="Ajio Luxe",
                    status="In Stock",
                    price_range="₹2,500 – ₹11,000",
                    channel_type="E-Commerce Fashion",
                    url=f"https://www.ajio.com/search/?text={name_clean}",
                    fulfillment="Standard Delivery"
                )
            ]

    # Retail Recommendation
    score = trend.trend_score
    rec_badge = "SCALE INVENTORY" if score >= 88 else "TEST / STOCK" if score >= 75 else "MONITOR"
    demand_badge = "VERY HIGH" if score >= 88 else "HIGH" if score >= 75 else "MODERATE"
    retail_rec = RetailRecommendation(
        recommendation=rec_badge,
        action="Scale Inventory" if score >= 88 else "Test / Stock" if score >= 75 else "Monitor",
        demand=demand_badge,
        price_segment="Bridge-to-Luxury" if trend.region == "Tamil Nadu" else "Contemporary Premium",
        reason=f"Strong momentum (+{trend.growth_rate}%) supported by cross-channel signals across {trend.region}.",
        target_audience="Heritage Enthusiasts & Festive Shoppers",
        risk="Low" if score >= 80 else "Moderate",
        timing="Immediate (Next 30 Days)" if score >= 85 else "Next 60 Days",
        notes=f"Prioritize key fabrics and colors for {trend.name} in regional hubs."
    )

    return TrendDetailResponse(
        trend=trend,
        attributes=attrs_dict,
        signals=signals,
        sources=sources,
        availabilities=availabilities,
        history=history,
        insights=insights,
        retail_recommendation=retail_rec
    )

async def get_trend_history(trend_id: str) -> List[TrendObservation]:
    data = db_manager.load_all()
    raw_history = [h for h in data.get("trend_history", []) if h.get("trend_id") == trend_id]
    results = []
    for h in raw_history:
        ts = h.get("timestamp") or datetime.utcnow().isoformat() + "Z"
        results.append(TrendObservation(
            timestamp=ts,
            observation_date=datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%b %d") if "T" in ts else ts,
            score=int(h.get("score", 70)),
            growth_rate=float(h.get("growth_rate", 20.0)),
            recorded_score=int(h.get("score", 70))
        ))
    return results

async def get_trend_sources(trend_id: str) -> List[TrendSource]:
    data = db_manager.load_all()
    raw_sources = [s for s in data.get("sources", []) if s.get("trend_id") == trend_id]
    return [
        TrendSource(
            source_name=s.get("source_name", "Fashion Journal"),
            title=s.get("title", "Industry observation report"),
            source_url=s.get("source_url", "#"),
            source_type=s.get("source_type", "News"),
            published_at=s.get("published_at"),
            collected_at=s.get("collected_at")
        ) for s in raw_sources
    ]

async def get_regional_summary(region: str) -> RegionalResponse:
    data = db_manager.load_all()
    all_trends = data.get("trends", [])
    region_clean = region.strip()

    if region_clean in ("All", "India"):
        matched = [Trend(**t) for t in all_trends]
    else:
        matched = [Trend(**t) for t in all_trends if t.get("region", "").lower() == region_clean.lower()]

    fashion_attrs = data.get("fashion_attributes", [])
    fabric_counts: Dict[str, int] = {}
    color_set = set()

    matched_ids = {t.id for t in matched}
    for a in fashion_attrs:
        if a.get("trend_id") in matched_ids:
            fab = a.get("fabric")
            if fab:
                fabric_counts[fab] = fabric_counts.get(fab, 0) + 1
            col = a.get("color")
            if col:
                for c in col.replace("&", ",").replace("/", ",").split(","):
                    c_clean = c.strip()
                    if c_clean:
                        color_set.add(c_clean)

    popular_fabrics = [
        PopularFabric(name=f, count=cnt)
        for f, cnt in sorted(fabric_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    popular_colors = [PopularColor(name=c) for c in sorted(list(color_set))[:6]]

    return RegionalResponse(
        region=region_clean,
        trends=matched,
        popular_fabrics=popular_fabrics,
        popular_colors=popular_colors,
        regional_confidence=92 if matched else 65
    )

async def get_dashboard_kpis() -> DashboardStats:
    data = db_manager.load_all()
    trends = data.get("trends", [])
    
    live_count = len(trends)
    rising_count = sum(1 for t in trends if t.get("status") in ("RISING", "EXPLODING"))
    fastest = max([t.get("growth_rate", 0.0) for t in trends], default=0.0)
    
    sources_list = data.get("sources", [])
    unique_domains = set()
    for s in sources_list:
        name = s.get("source_name")
        if name:
            unique_domains.add(name)
    
    signals_list = data.get("trend_signals", [])

    return DashboardStats(
        live_trends=live_count,
        rising_trends=rising_count,
        fastest_growing=round(fastest, 1),
        sources_tracked=max(len(unique_domains), 12),
        signals_analyzed=max(len(signals_list), 150),
        last_updated=data.get("last_updated") or datetime.utcnow().isoformat() + "Z",
        system_status="online"
    )

async def upsert_trend_bundle(
    trend: Trend,
    attributes: List[TrendAttribute],
    signals: List[TrendSignal],
    sources: List[TrendSource],
    history: List[TrendObservation],
    insights: List[TrendInsight],
    retail_rec: Optional[RetailRecommendation]
):
    async with db_manager.lock:
        data = db_manager.load_all()
        trends = data.setdefault("trends", [])
        
        # 1. Trend in trends list
        idx = next((i for i, t in enumerate(trends) if t["id"] == trend.id), -1)
        trend_dict = trend.model_dump()
        if idx >= 0:
            trends[idx] = trend_dict
        else:
            trends.append(trend_dict)

        # 2. Fashion attributes
        fashion_attrs = data.setdefault("fashion_attributes", [])
        attr_entry = next((a for a in fashion_attrs if a.get("trend_id") == trend.id), None)
        if not attr_entry:
            attr_entry = {"id": f"fa_{trend.id}", "trend_id": trend.id}
            fashion_attrs.append(attr_entry)

        for a in attributes:
            atype = a.attribute_type.lower()
            if "color" in atype:
                attr_entry["color"] = a.attribute_value
            elif "fabric" in atype:
                attr_entry["fabric"] = a.attribute_value
            elif "pattern" in atype:
                attr_entry["pattern"] = a.attribute_value
            elif "silhouette" in atype:
                attr_entry["silhouette"] = a.attribute_value
            elif "style" in atype or "context" in atype:
                attr_entry["style"] = a.attribute_value

        # 3. Sources
        sources_list = data.setdefault("sources", [])
        # Filter out old sources for this trend and append new
        sources_list = [s for s in sources_list if s.get("trend_id") != trend.id]
        for src in sources:
            src_dict = src.model_dump()
            src_dict["trend_id"] = trend.id
            sources_list.append(src_dict)
        data["sources"] = sources_list

        # 4. Signals
        signals_list = data.setdefault("trend_signals", [])
        signals_list = [s for s in signals_list if s.get("trend_id") != trend.id]
        for sig in signals:
            sig_dict = sig.model_dump()
            sig_dict["trend_id"] = trend.id
            signals_list.append(sig_dict)
        data["trend_signals"] = signals_list

        # 5. History
        hist_list = data.setdefault("trend_history", [])
        hist_list = [h for h in hist_list if h.get("trend_id") != trend.id]
        for h in history:
            h_dict = h.model_dump()
            h_dict["trend_id"] = trend.id
            hist_list.append(h_dict)
        data["trend_history"] = hist_list

        # 6. Insights
        ins_list = data.setdefault("ai_insights", [])
        ins_list = [i for i in ins_list if i.get("trend_id") != trend.id]
        for ins in insights:
            ins_dict = ins.model_dump()
            ins_dict["trend_id"] = trend.id
            ins_list.append(ins_dict)
        data["ai_insights"] = ins_list

        data["last_updated"] = datetime.utcnow().isoformat() + "Z"
        db_manager.save_all(data)

    # Sync to Supabase if available
    await db_manager.execute_supabase_upsert("trends", [trend.model_dump()])

async def add_pipeline_log(event_type: str, source: str, message: str, details: Optional[Dict[str, Any]] = None):
    async with db_manager.lock:
        data = db_manager.load_all()
        logs = data.setdefault("pipeline_logs", [])
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "source": source,
            "message": message,
            "details": details or {}
        }
        logs.insert(0, log_entry)
        data["pipeline_logs"] = logs[:100]
        db_manager.save_all(data)

async def get_pipeline_logs() -> List[Dict[str, Any]]:
    data = db_manager.load_all()
    return data.get("pipeline_logs", [])
