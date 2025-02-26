def truncate_string(s, front=15, back=15):
    if len(s) <= front + back:
        return s
    return f"{s[:front]}...{s[-back:]}"
