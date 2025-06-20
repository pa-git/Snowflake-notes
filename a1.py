# Step 3: Create canonical legal entities and relationships
def load_canonical_entities(grouped_entities):
    for group in grouped_entities:
        canon = group["entity_group"]
        variants = group["matches"]

        canonical_node = CanonicalEntity.nodes.get_or_none(name=canon)
        if not canonical_node:
            canonical_node = CanonicalEntity(name=canon).save()
            print(f"✅ Created Canonical Entity: {canon}")

        # Link Entities
        for v in variants:
            entity_nodes = Entity.nodes.filter(name=v)
            for e in entity_nodes:
                if not e.is_canonical_entity.is_connected(canonical_node):
                    e.is_canonical_entity.connect(canonical_node)
                    print(f"  ↳ Linked: {v} → {canon}")


def run():
    print("📥 Fetching legal entities...")
    companies = get_distinct_company_names()
    print(f"📊 Total companies to disambiguate: {len(companies)}")

    batch_size = 100
    total_batches = (len(companies) + batch_size - 1) // batch_size

    for i in range(0, len(companies), batch_size):
        batch = companies[i:i + batch_size]
        print(f"\n🔍 Processing batch {i // batch_size + 1} of {total_batches} ({len(batch)} records)...")
        try:
            groups = generate_canonical_entity_groups(batch)
            load_canonical_entities(groups)
        except Exception as e:
            print(f"❌ Failed to process batch {i // batch_size + 1}: {e}")

    print("\n✅ Canonical legal entity mapping complete.")
