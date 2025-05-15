def create_canonical_services(groupings):
    for group in groupings:
        canonical = CanonicalService.nodes.get_or_none(name=group["name"])
        if not canonical:
            canonical = CanonicalService(
                name=group["name"],
                description=group.get("description")
            ).save()
        for match in group["matches"]:
            service = Service.nodes.get_or_none(name=match)
            if service:
                service.is_canonical_service.connect(canonical)

def create_canonical_roles(groupings):
    for group in groupings:
        canonical = CanonicalRole.nodes.get_or_none(name=group["name"])
        if not canonical:
            canonical = CanonicalRole(
                name=group["name"],
                description=group.get("description")
            ).save()
        for match in group["matches"]:
            role = Role.nodes.get_or_none(name=match)
            if role:
                role.is_canonical_role.connect(canonical)
