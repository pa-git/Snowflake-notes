import os
import json
from pathlib import Path
from dotenv import load_dotenv
from neomodel import config
from models import (
    Contract, FeeBreakdown, Signature, Service, Role, ServiceLevelAgreement,
    EngagementScope, Initiative, Project, DeliverableAndInvoice, Party
)

# Load DATABASE_URL from .env
load_dotenv()
config.DATABASE_URL = os.getenv("DATABASE_URL")


def load_all_contracts_from_directory(base_path: str):
    base = Path(base_path)
    contract_files = list(base.glob("contract_*/full_contract.json"))
    print(f"Found {len(contract_files)} contract files.")

    for file in contract_files:
        try:
            print(f"\nLoading file: {file.name}")
            with open(file, 'r', encoding='utf-8') as f:
                contract_data = json.load(f)
                load_contract_from_json(contract_data)
                print(f"Processed {file.name} ✓")
        except Exception as e:
            print(f"❌ Failed to load {file}: {e}")


def load_contract_from_json(data: dict):
    meta = data["contract_metadata"]

    contract = Contract.nodes.get_or_none(file_name=meta["file_name"])
    if not contract:
        print(f"- Creating contract: {meta['file_name']}")
        contract = Contract(
            file_name=meta["file_name"],
            vendor_name=meta.get("vendor_name"),
            type=meta.get("type"),
            summary_description=meta.get("summary_description"),
            start_date=meta.get("start_date"),
            end_date=meta.get("end_date"),
            base_fee=data.get("financials", {}).get("base_fee"),
            total_fee=data.get("financials", {}).get("total_fee"),
            exclusions=data.get("financials", {}).get("exclusions", []),
            payment_terms=data.get("financials", {}).get("payment_terms"),
            billing_instructions=data.get("financials", {}).get("billing_instructions"),
            exceptions_or_notes=data.get("financials", {}).get("exceptions_or_notes", []),
            division=(data.get("projects") or [{}])[0].get("division"),
        ).save()

    # Fee Breakdown
    for fee in data.get("financials", {}).get("fee_breakdown", []):
        print(f"  - Fee Event: {fee['event']}")
        fb = FeeBreakdown(event=fee["event"], fee=fee["fee"]).save()
        contract.has_fee_breakdown.connect(fb)

    # Signatures
    for sig in data.get("signatures", []):
        print(f"  - Signature: {sig['type']}")
        s = Signature(
            type=sig.get("type"),
            name=sig.get("name"),
            title=sig.get("title"),
            date=sig.get("date")
        ).save()
        contract.signed_by.connect(s)

    # Services
    for s in data.get("services", []):
        print(f"  - Service: {s['name']}")
        service = Service(
            name=s["name"],
            description=s.get("description"),
            period=s.get("period"),
            coverage=s.get("coverage"),
            locations=s.get("locations", []),
            days=s.get("days"),
            quantity=s.get("quantity"),
            unit_price=s.get("unit_price"),
            total=s.get("total"),
            notes=s.get("notes", [])
        ).save()
        contract.includes_service.connect(service)

    # Roles
    for r in data.get("roles", []):
        print(f"  - Role: {r['role_name']} / {r['resource_name']}")
        role = Role(
            name=r["role_name"],
            resource_name=r["resource_name"],
            description=r.get("description"),
            level=r.get("level"),
            location=r.get("location"),
            hours_committed=r.get("hours_committed"),
            rate_amount=r.get("rate", {}).get("amount"),
            rate_currency=r.get("rate", {}).get("currency"),
            rate_unit=r.get("rate", {}).get("unit"),
            total_fees=r.get("total_fees"),
            billing_type=r.get("billing_type"),
            schedule_reference=r.get("schedule_reference"),
            project=r.get("project")
        ).save()
        contract.includes_role.connect(role)

    # SLAs
    for s in data.get("service_level_agreements", []):
        print(f"  - SLA: {s['name']}")
        sla = ServiceLevelAgreement(
            name=s.get("name"),
            description=s.get("description"),
            target=s.get("target"),
            metric=s.get("metric"),
            unit=s.get("unit"),
            frequency=s.get("frequency"),
            applies_to=s.get("applies_to_services", []),
            penalty_clause=s.get("penalty_clause"),
            enforcement_method=s.get("enforcement_method")
        ).save()
        contract.governed_by_sla.connect(sla)

    # Engagement Scope
    print("  - Engagement Scope")
    scope = EngagementScope(
        core_applications=data.get("engagement_scope", {}).get("core_applications", []),
        supporting_applications=data.get("engagement_scope", {}).get("supporting_applications", []),
        key_activities=data.get("engagement_scope", {}).get("key_activities", []),
        assumptions=data.get("assumptions", []),
        expectations=data.get("expectations", []),
        conditions=data.get("conditions", [])
    ).save()
    contract.has_engagement_scope.connect(scope)

    # Initiative
    init = (data.get("initiatives") or [{}])[0]
    if init.get("name"):
        print(f"  - Initiative: {init['name']}")
        initiative = Initiative.nodes.get_or_none(name=init["name"])
        if not initiative:
            initiative = Initiative(
                name=init["name"],
                description=init.get("description")
            ).save()
        contract.associated_with_initiative.connect(initiative)

    # Project
    proj = (data.get("projects") or [{}])[0]
    if proj.get("name"):
        print(f"  - Project: {proj['name']}")
        project = Project.nodes.get_or_none(name=proj["name"])
        if not project:
            project = Project(
                name=proj["name"],
                description=proj.get("description"),
                start_date=proj.get("start_date"),
                end_date=proj.get("end_date"),
                status=proj.get("status")
            ).save()
        contract.associated_with_project.connect(project)

    # Deliverables
    for d in data.get("deliverables_and_invoices", []):
        print(f"  - Deliverable: {d['deliverable']}")
        deliv = DeliverableAndInvoice(
            deliverable=d.get("deliverable"),
            delivery_date=d.get("delivery_date"),
            invoice_amount_usd=d.get("invoice_amount_usd", 0.0),
            percentage=d.get("percentage", 0.0)
        ).save()
        contract.has_deliverable_invoice.connect(deliv)

    # Parties
    for p in data.get("parties", []):
        print(f"  - Party: {p['name']}")
        party = Party.nodes.get_or_none(name=p["name"])
        if not party:
            party = Party(
                name=p["name"],
                type=p.get("type"),
                address=p.get("address"),
                context=p.get("context")
            ).save()
        contract.involves_party.connect(party)
