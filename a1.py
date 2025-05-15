def batched_locations(locations, batch_size=100):
    for i in range(0, len(locations), batch_size):
        yield locations[i:i + batch_size]


def run():
    print("Fetching all raw location strings...")
    raw_locations = fetch_all_raw_locations()
    print(f"Found {len(raw_locations)} unique raw locations.")

    for batch in batched_locations(raw_locations, batch_size=100):
        print(f"\nProcessing batch: {batch[0]} ... {batch[-1]}")
        groups = group_and_enrich_locations_with_gpt(batch)
        create_and_link_locations(groups)

    print("✅ Canonical location mapping complete.")


if not role.located_at.is_connected(canonical):
