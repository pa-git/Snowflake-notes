# Filter out empty or invalid names
names = [r["name"] for r in batch if r["name"] and r["name"].strip()]
if not names:
    print(f"[skip] No valid names in batch (skip={skip})")
    skip += limit
    continue

vectors = embed(names)
