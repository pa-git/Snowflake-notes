role_nodes = Role.nodes.filter(role_name=v)
for role_node in role_nodes:
    canon_node.roles.connect(role_node)
    print(f"  ↳ Linked: {v} → {canon}")
