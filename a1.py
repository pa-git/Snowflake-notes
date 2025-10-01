if (df["location"] != "").any():   # at least one non-empty location
    filtered = df[df["location"].str.lower() == "onsite"]
    if filtered.empty:
        print("⚠️ Non-empty locations found but no 'onsite' row.")
        result = df  # fallback: keep all
    else:
        result = filtered
else:
    result = df  # keep as is if all are empty
