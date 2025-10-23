def _to_ms(v):
    if v is None: 
        return None
    if hasattr(v, "total_seconds"):             # datetime.timedelta
        return int(v.total_seconds() * 1000)
    if isinstance(v, (int, float)):             # assume seconds if small
        return int(v if v > 1e6 else v * 1000)  # >1e6 -> already ms
    try:
        x = float(v)
        return int(x if x > 1e6 else x * 1000)
    except Exception:
        return None
