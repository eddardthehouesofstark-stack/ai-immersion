import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from datetime import datetime
import httpx
from backend.utils.logging import get_logger
from backend.utils.retry import async_retry

logger = get_logger("trend_collector")

GOOGLE_TRENDS_RSS_INDIA = "https://trends.google.com/trending/rss?geo=IN"

class TrendCollector:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    @async_retry(max_attempts=2, delay=1.0)
    async def fetch_search_trends(self) -> List[Dict[str, Any]]:
        logger.info("Fetching real Google Trends search signals for India...")
        trends = []
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=10.0) as client:
                res = await client.get(GOOGLE_TRENDS_RSS_INDIA)
                if res.status_code == 200:
                    root = ET.fromstring(res.text)
                    channel = root.find("channel") or root
                    for item in channel.findall("item"):
                        title_elem = item.find("title")
                        pub_elem = item.find("pubDate")
                        approx_elem = item.find("{https://trends.google.com/trending/rss}approx_traffic")

                        title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                        pub_date = pub_elem.text.strip() if pub_elem is not None and pub_elem.text else ""
                        traffic = approx_elem.text.strip() if approx_elem is not None and approx_elem.text else "10,000+"

                        if title:
                            trends.append({
                                "query": title,
                                "approx_traffic": traffic,
                                "published_at": pub_date,
                                "source_type": "Google Trends Search",
                                "source_url": f"https://trends.google.com/trends/explore?q={title}&geo=IN",
                                "collected_at": datetime.utcnow().isoformat() + "Z"
                            })
        except Exception as e:
            logger.warning(f"Google Trends fetch encountered: {e}")
        return trends

trend_collector = TrendCollector()
