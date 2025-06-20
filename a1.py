# Step 3: Create canonical roles and relationships
def load_canonical_roles(grouped_roles):
    for canon, variants in grouped_roles.items():
        canon_node = CanonicalRole.nodes.get_or_none(name=canon)
        if not canon_node:
            canon_node = CanonicalRole(name=canon).save()
            print(f"✅ Created Canonical Role: {canon}")

        # Link Roles
        for v in variants:
            role_nodes = Role.nodes.filter(name=v)
            for r in role_nodes:
                if not r.is_canonical_role.is_connected(canon_node):
                    r.is_canonical_role.connect(canon_node)
                    print(f"  ↳ Linked: {v} → {canon}")


def run():
    print("📥 Fetching roles...")
    roles = get_distinct_roles()
    print(f"📊 Total roles to disambiguate: {len(roles)}")

    batch_size = 100
    total_batches = (len(roles) + batch_size - 1) // batch_size

    for i in range(0, len(roles), batch_size):
        batch = roles[i:i + batch_size]
        print(f"\n🔎 Processing batch {i // batch_size + 1} of {total_batches} ({len(batch)} records)...")
        try:
            groups = generate_canonical_groups(batch)
            load_canonical_roles(groups)
        except Exception as e:
            print(f"❌ Failed to process batch {i // batch_size + 1}: {e}")

    print("\n✅ Canonical Role mapping complete.")
