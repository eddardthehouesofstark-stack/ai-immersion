import logging
import sys
from datetime import datetime

# Configure central logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("TrendLoom")

def get_logger(name: str):
    return logging.getLogger(f"TrendLoom.{name}")
