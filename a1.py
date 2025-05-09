... [trimmed for brevity above] ...

    # --- Parties ---
    parties = {}
    for p in data.get("parties", []):
        print(f"Creating or retrieving Party: {p['name']} ({p['type']})")
        party = Party.nodes.get_or_none(name=p["name"])
        if not party:
            party = Party(
                name=p["name"],
                type=p.get("type"),
                address=p.get("address"),
                context=p.get("context")
            ).save()
        parties[p["type"]] = party
        summary["vendors" if p["type"] == "Service Provider" else "clients"] += 1

    # --- Division ---
    div = data.get("divisions", [{}])[0]
    print(f"Creating or retrieving Division: {div.get('name')}")
    division = Division.nodes.get_or_none(name=div.get("name"))
    if not division:
        division = Division(name=div.get("name"), description=div.get("description")).save()
    summary["divisions"] += 1

    # --- Initiative ---
    init = data.get("initiatives", [{}])[0]
    print(f"Creating or retrieving Initiative: {init.get('name')}")
    initiative = Initiative.nodes.get_or_none(name=init.get("name"))
    if not initiative:
        initiative = Initiative(name=init.get("name"), description=init.get("description")).save()
    summary["initiatives"] += 1

    # --- Project ---
    proj = data.get("projects", [{}])[0]
    print(f"Creating or retrieving Project: {proj.get('name')}")
    project = Project.nodes.get_or_none(name=proj.get("name"))
    if not project:
        project = Project(
            name=proj.get("name"),
            description=proj.get("description"),
            start_date=proj.get("start_date"),
            end_date=proj.get("end_date"),
            status=proj.get("status")
        ).save()
        project.division.connect(division)
        project.initiative.connect(initiative)
    summary["projects"] += 1

    # --- Contract ---
    meta = data["contract_metadata"]
    print(f"Creating or retrieving Contract: {meta['file_name']}")
    contract = Contract.nodes.get_or_none(file_name=meta["file_name"])
    if not contract:
        contract = Contract(
            file_name=meta["file_name"],
            type=meta.get("type"),
            summary_description=meta.get("summary_description"),
            start_date=meta.get("start_date"),
            end_date=meta.get("end_date")
        ).save()
        if "Client" in parties:
            contract.client.connect(parties["Client"])
        if "Service Provider" in parties:
            contract.vendor.connect(parties["Service Provider"])
        contract.project.connect(project)
    summary["contracts"] += 1

    # --- Services ---
    for s in data.get("services", []):
        print(f"Adding Service: {s['name']}")
        service = Service(
            name=s["name"],
            description=s.get("description"),
            period=s.get("period"),
            coverage=s.get("coverage"),
            notes="\n".join(s.get("notes", []))
        ).save()
        contract.services.connect(service)
        summary["services"] += 1

    # --- SLAs ---
    for s in data.get("service_level_agreements", []):
        print(f"Adding SLA: {s['name']}")
        sla = ServiceLevelAgreement(
            name=s["name"],
            description=s.get("description"),
            target=s.get("target"),
            metric=s.get("metric"),
            unit=s.get("unit"),
            frequency=s.get("frequency"),
            enforcement_method=s.get("enforcement_method")
        ).save()
        summary["slas"] += 1

    # --- Roles ---
    for r in data.get("roles", []):
        print(f"Adding Role: {r['role_name']} for {r['resource_name']}")
        role = Role(
            role_name=r["role_name"],
            description=r.get("description"),
            level=r.get("level"),
            location=r.get("location"),
            hours_committed=r.get("hours_committed"),
            billing_type=r.get("billing_type"),
            schedule_reference=r.get("schedule_reference"),
            project=r.get("project")
        ).save()

        # Resource
        res = Resource.nodes.get_or_none(name=r["resource_name"])
        if not res:
            print(f"Creating Resource: {r['resource_name']}")
            res = Resource(name=r["resource_name"]).save()
            summary["resources"] += 1
        role.resource.connect(res)

        # Rate
        rate_data = r.get("rate")
        if rate_data:
            print(f"Adding Rate for {r['resource_name']}: {rate_data['amount']} {rate_data['currency']} per {rate_data['unit']}")
            rate = Rate(
                amount=rate_data["amount"],
                currency=rate_data["currency"],
                unit=rate_data["unit"]
            ).save()
            role.rate.connect(rate)
            summary["rates"] += 1

        contract.roles.connect(role)
        summary["roles"] += 1

    # --- Deliverables ---
    for d in data.get("deliverables_and_invoices", []):
        print(f"Adding Deliverable: {d.get('deliverable')}")
        deliv = Deliverable(
            name=d.get("deliverable"),
            delivery_date=d.get("delivery_date"),
            invoice_amount_usd=d.get("invoice_amount_usd", 0.0),
            percentage=d.get("percentage", 0.0)
        ).save()
        summary["deliverables"] += 1

    return summary
