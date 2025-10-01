# Convert NaN to "" for string columns
    for col in ["country", "currency", "level", "vendor"]:
        df[col] = df[col].fillna("").astype(str).str.strip()
