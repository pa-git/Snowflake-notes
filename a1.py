from neomodel import db
from models import Party, Vendor, Contract, Service, Role, Rate, Resource, ServiceLevelAgreement, Project, Division, Initiative, Deliverable

def load_contract_from_json(data: dict):
    summary = {
        "vendors": 0,
        "clients": 0,
        "projects": 0,
        "divisions": 0,
        "initiatives": 0,
        "contracts": 0,
        "services": 0,
        "roles": 0,
        "resources": 0,
        "rates": 0,
        "slas": 0,
        "deliverables": 0
    }

    # --- Parties ---
    parties = {}
    for p in data.get("parties", []):
        party, _ = Party.nodes.get_or_create(name=p["name"], defaults={
            "type": p.get("type"),
            "address": p.get("address"),
            "context": p.get("context")
        })
        parties[p["type"]] = party
        summary["vendors" if p["type"] == "Service Provider" else "clients"] += 1

    # --- Division ---
    div = data.get("divisions", [{}])[0]
    division, _ = Division.nodes.get_or_create(name=div.get("name"), defaults={"description": div.get("description")})
    summary["divisions"] += 1

    # --- Initiative ---
    init = data.get("initiatives", [{}])[0]
    initiative, _ = Initiative.nodes.get_or_create(name=init.get("name"), defaults={"description": init.get("description")})
    summary["initiatives"] += 1

    # --- Project ---
    proj = data.get("projects", [{}])[0]
    project, _ = Project.nodes.get_or_create(name=proj.get("name"), defaults={
        "description": proj.get("description"),
        "start_date": proj.get("start_date"),
        "end_date": proj.get("end_date"),
        "status": proj.get("status")
    })
    project.division.connect(division)
    project.initiative.connect(initiative)
    summary["projects"] += 1

    # --- Contract ---
    meta = data["contract_metadata"]
    contract, _ = Contract.nodes.get_or_create(file_name=meta["file_name"], defaults={
        "type": meta.get("type"),
        "summary_description": meta.get("summary_description"),
        "start_date": meta.get("start_date"),
        "end_date": meta.get("end_date")
    })
    if "Client" in parties:
        contract.client.connect(parties["Client"])
    if "Service Provider" in parties:
        contract.vendor.connect(parties["Service Provider"])
    contract.project.connect(project)
    summary["contracts"] += 1

    # --- Services ---
    for s in data.get("services", []):
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
            res = Resource(name=r["resource_name"]).save()
            summary["resources"] += 1
        role.resource.connect(res)

        # Rate
        rate_data = r.get("rate")
        if rate_data:
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
        deliv = Deliverable(
            name=d.get("deliverable"),
            delivery_date=d.get("delivery_date"),
            invoice_amount_usd=d.get("invoice_amount_usd", 0.0),
            percentage=d.get("percentage", 0.0)
        ).save()
        summary["deliverables"] += 1

    return summary
