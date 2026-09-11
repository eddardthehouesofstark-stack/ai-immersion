import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
import httpx
from dotenv import load_dotenv
from backend.utils.logging import get_logger

load_dotenv()
logger = get_logger("database")

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "trendloom.json"

class DatabaseManager:
    def __init__(self):
        self.supabase_url = os.environ.get("SUPABASE_URL", "").strip()
        self.supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
        self.has_supabase = bool(self.supabase_url and self.supabase_key)
        self.lock = asyncio.Lock()
        self._ensure_storage()
        if self.has_supabase:
            logger.info(f"Supabase PostgreSQL integration active: {self.supabase_url}")
        else:
            logger.info("Operating with persistent high-speed local data store with Supabase sync readiness.")

    def _ensure_storage(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            initial_data = {
                "trends": [],
                "attributes": {},
                "signals": {},
                "sources": {},
                "history": {},
                "insights": {},
                "retail_recommendations": {},
                "pipeline_logs": [],
                "last_updated": None
            }
            DATA_FILE.write_text(json.dumps(initial_data, indent=2))

    def load_all(self) -> Dict[str, Any]:
        try:
            if DATA_FILE.exists():
                text = DATA_FILE.read_text(encoding="utf-8")
                return json.loads(text)
        except Exception as e:
            logger.error(f"Error reading database file: {e}")
        return {
            "trends": [],
            "attributes": {},
            "signals": {},
            "sources": {},
            "history": {},
            "insights": {},
            "retail_recommendations": {},
            "pipeline_logs": [],
            "last_updated": None
        }

    def save_all(self, data: Dict[str, Any]):
        try:
            temp_file = DATA_DIR / "trendloom.tmp"
            temp_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
            temp_file.replace(DATA_FILE)
        except Exception as e:
            logger.error(f"Error saving database file: {e}")

    async def execute_supabase_upsert(self, table: str, records: List[Dict[str, Any]]) -> bool:
        if not self.has_supabase:
            return False
        try:
            base_url = self.supabase_url.rstrip("/")
            if base_url.endswith("/rest/v1"):
                base_url = base_url[:-8]
            url = f"{base_url}/rest/v1/{table}"
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, json=records, headers=headers)
                if res.status_code in (200, 201):
                    logger.info(f"Successfully synced {len(records)} records to Supabase table '{table}'")
                    return True
                else:
                    logger.warning(f"Supabase sync returned {res.status_code}: {res.text}")
        except Exception as e:
            logger.error(f"Supabase upsert failed: {e}")
        return False

db_manager = DatabaseManager()
