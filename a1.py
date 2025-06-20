def run():
    print("📍 Fetching all raw location strings...")
    raw_locations = fetch_all_raw_locations()
    print(f"🔢 Total locations to canonicalize: {len(raw_locations)}")

    batch_size = 100
    total_batches = (len(raw_locations) + batch_size - 1) // batch_size

    for i in range(0, len(raw_locations), batch_size):
        batch = raw_locations[i:i + batch_size]
        print(f"\n📦 Processing batch {i // batch_size + 1} of {total_batches} ({len(batch)} records)...")
        try:
            groups = group_and_enrich_locations_with_gpt(batch)
            create_and_link_locations(groups)
        except Exception as e:
            print(f"❌ Failed to process batch {i // batch_size + 1}: {e}")

    print("\n✅ Canonical location mapping complete.")
