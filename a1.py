import re
from datetime import datetime
from typing import Optional

def parse_flexible_date(date_str: str) -> Optional[datetime.date]:
    if not date_str or not isinstance(date_str, str):
        return None

    date_str = date_str.strip()

    if date_str.lower() in ["unknown", "n/a", "na", "none", "-", "--", ""]:
        return None

    # Remove ordinal suffixes: 1st -> 1, 2nd -> 2, 3rd -> 3, 4th -> 4
    date_str = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', date_str, flags=re.IGNORECASE)

    formats = [
        "%Y-%m-%d",
        "%d-%b-%Y",
        "%d-%B-%Y",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d.%m.%Y",
        "%b %d, %Y",
        "%B %d, %Y",
        "%d %b %Y",
        "%d %B %Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(date_str).date()
    except ValueError:
        return None
