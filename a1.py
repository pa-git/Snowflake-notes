def load_canonical_roles(grouped_roles):
    for group in grouped_roles:
        canon = group["name"]
        variants = group["matches"]

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
