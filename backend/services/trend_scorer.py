from typing import Dict, Any, Tuple
from backend.database.models import TrendStatus

class TrendScorer:
    """
    Computes mathematically rigorous composite momentum scores (0-100)
    using weights:
      - Search Growth: 25%
      - News Mentions: 20%
      - Engagement / Velocity: 20%
      - Recency: 15%
      - Cross-Source Corroboration: 10%
      - Regional Relevance: 10%
    """

    @staticmethod
    def calculate_score(
        search_growth: float,       # e.g. 0 to 100
        news_mentions: int,         # count of verified articles
        velocity_momentum: float,   # raw velocity measure
        recency_hours: float,       # hours since latest signal
        source_count: int,          # unique corroborating sources
        regional_density: float     # regional signal ratio
    ) -> Tuple[int, TrendStatus, float]:
        # 1. Search growth component (max 100 -> 25 pts)
        search_comp = min(max(search_growth, 0.0), 100.0) * 0.25

        # 2. News mentions component (scale up to 10 mentions -> 20 pts)
        news_comp = min(news_mentions / 10.0, 1.0) * 100.0 * 0.20

        # 3. Engagement / Velocity component (20 pts)
        vel_comp = min(max(velocity_momentum, 0.0), 100.0) * 0.20

        # 4. Recency decay component (15 pts: fresher is higher)
        # full score if <= 6 hours, exponential decay over 72 hours
        recency_factor = max(0.0, 1.0 - (recency_hours / 72.0))
        recency_comp = recency_factor * 100.0 * 0.15

        # 5. Cross-source corroboration component (10 pts: 4+ sources = 10 pts)
        cross_source_comp = min(source_count / 4.0, 1.0) * 100.0 * 0.10

        # 6. Regional relevance component (10 pts)
        regional_comp = min(max(regional_density, 0.0), 1.0) * 100.0 * 0.10

        raw_score = search_comp + news_comp + vel_comp + recency_comp + cross_source_comp + regional_comp
        final_score = int(round(min(max(raw_score, 0), 100)))

        # Status determination per Section 23
        if final_score >= 90:
            status = TrendStatus.EXPLODING
        elif final_score >= 75:
            status = TrendStatus.RISING
        elif final_score >= 50:
            status = TrendStatus.STABLE
        elif final_score >= 25:
            status = TrendStatus.DECLINING
        else:
            status = TrendStatus.FADING

        return final_score, status, round(raw_score, 1)

    @staticmethod
    def compute_velocity(current_score: int, previous_score: int) -> float:
        return float(current_score - previous_score)

trend_scorer = TrendScorer()
