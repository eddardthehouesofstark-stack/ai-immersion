import re
from typing import Optional

def sanitize_search_query(q: Optional[str]) -> str:
    if not q:
        return ""
    # strip dangerous characters and limit length
    clean = re.sub(r"[^\w\s\-\.\,\']", "", q).strip()
    return clean[:100]

def validate_region(region: Optional[str]) -> str:
    valid_regions = [
        "India",
        "Tamil Nadu",
        "Kerala",
        "Karnataka",
        "Andhra Pradesh",
        "Telangana",
        "Maharashtra",
        "Delhi",
        "West Bengal"
    ]
    if not region or region in ("All", "All Regions"):
        return "India"
    for r in valid_regions:
        if r.lower() == region.lower():
            return r
    return region
