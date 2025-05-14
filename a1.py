def parse_optional_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, "%d-%b-%Y").date()
