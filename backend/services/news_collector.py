import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from datetime import datetime
import httpx
from backend.utils.logging import get_logger
from backend.utils.retry import async_retry

logger = get_logger("news_collector")

RSS_FEEDS = [
    {
        "url": "https://news.google.com/rss/search?q=Tamil+Nadu+fashion+handloom+silk+saree&hl=en-IN&gl=IN&ceid=IN:en",
        "default_source": "Google News Tamil Nadu",
        "region": "Tamil Nadu"
    },
    {
        "url": "https://news.google.com/rss/search?q=India+fashion+week+trends+designer+textiles&hl=en-IN&gl=IN&ceid=IN:en",
        "default_source": "Google News Fashion India",
        "region": "India"
    },
    {
        "url": "https://www.thehindu.com/life-and-style/fashion/feeder/default.rss",
        "default_source": "The Hindu Fashion",
        "region": "India"
    },
    {
        "url": "https://www.hindustantimes.com/feeds/rss/lifestyle/fashion/rssfeed.xml",
        "default_source": "Hindustan Times Fashion",
        "region": "India"
    },
    {
        "url": "https://indianexpress.com/section/lifestyle/fashion/feed/",
        "default_source": "The Indian Express Lifestyle",
        "region": "India"
    },
    {
        "url": "https://timesofindia.indiatimes.com/rssfeeds/2886704.cms",
        "default_source": "Times of India Life & Style",
        "region": "India"
    },
    {
        "url": "https://news.google.com/rss/search?q=site:vogue.in+fashion+saree+lehenga+textiles&hl=en-IN&gl=IN&ceid=IN:en",
        "default_source": "Vogue India Trend Wire",
        "region": "India"
    },
    {
        "url": "https://news.google.com/rss/search?q=(site:elle.in+OR+site:grazia.co.in)+fashion+trends&hl=en-IN&gl=IN&ceid=IN:en",
        "default_source": "Elle & Grazia India",
        "region": "India"
    },
    {
        "url": "https://news.google.com/rss/search?q=handloom+textile+export+apparel+india&hl=en-IN&gl=IN&ceid=IN:en",
        "default_source": "Apparel & Textile Resources India",
        "region": "India"
    },
    {
        "url": "https://news.google.com/rss/search?q=Kanchipuram+silk+Madurai+sungudi+Cooptex+handloom&hl=en-IN&gl=IN&ceid=IN:en",
        "default_source": "Co-optex & Tamil Nadu Weavers Guild",
        "region": "Tamil Nadu"
    },
    {
        "url": "https://news.google.com/rss/search?q=Lakme+Fashion+Week+FDCI+ethnic+wear+designer&hl=en-IN&gl=IN&ceid=IN:en",
        "default_source": "FDCI & Lakme Fashion Runway",
        "region": "India"
    }
]

class NewsCollector:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    @async_retry(max_attempts=2, delay=1.0)
    async def fetch_feed(self, client: httpx.AsyncClient, feed_info: Dict[str, str]) -> List[Dict[str, Any]]:
        articles = []
        try:
            res = await client.get(feed_info["url"], headers=self.headers, timeout=10.0)
            if res.status_code != 200:
                logger.warning(f"Feed {feed_info['url']} returned status {res.status_code}")
                return []

            root = ET.fromstring(res.text)
            channel = root.find("channel") or root
            for item in channel.findall("item")[:15]:
                title_elem = item.find("title")
                link_elem = item.find("link")
                pub_elem = item.find("pubDate")
                src_elem = item.find("source")

                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                pub_date = pub_elem.text.strip() if pub_elem is not None and pub_elem.text else ""
                source_name = (
                    src_elem.text.strip()
                    if src_elem is not None and src_elem.text
                    else feed_info["default_source"]
                )

                if title and link:
                    articles.append({
                        "title": title,
                        "url": link,
                        "published_at": pub_date,
                        "source_name": source_name,
                        "region_hint": feed_info.get("region", "India"),
                        "collected_at": datetime.utcnow().isoformat() + "Z"
                    })
        except Exception as e:
            logger.warning(f"Failed parsing feed {feed_info['url']}: {e}")
        return articles

    async def collect_all_news(self) -> List[Dict[str, Any]]:
        logger.info("Starting live news intelligence collection from verified editorial feeds...")
        all_articles = []
        async with httpx.AsyncClient(follow_redirects=True) as client:
            for feed in RSS_FEEDS:
                articles = await self.fetch_feed(client, feed)
                all_articles.extend(articles)

        # Deduplicate by title
        seen_titles = set()
        deduped = []
        for a in all_articles:
            norm_title = a["title"].lower().strip()
            if norm_title not in seen_titles:
                seen_titles.add(norm_title)
                deduped.append(a)

        logger.info(f"Collected {len(deduped)} unique verified editorial fashion articles.")
        return deduped

news_collector = NewsCollector()
