import os
from dotenv import load_dotenv
from neomodel import db
from models import Contract, CanonicalDivision

load_dotenv()


def fetch_unique_divisions():
    results, _ = db.cypher_query("MATCH (c:Contract) RETURN DISTINCT c.division")
    return sorted({r[0] for r in results if r[0]})


def create_canonical_divisions(division_names):
    created = 0
    for name in division_names:
        division = CanonicalDivision.nodes.get_or_none(name=name)
        if not division:
            division = CanonicalDivision(name=name).save()
            created += 1
    print(f"✅ Created {created} new canonical divisions.")


def link_contracts_to_canonical_divisions():
    contracts = Contract.nodes.all()
    linked = 0

    for contract in contracts:
        if not contract.division:
            continue

        canonical = CanonicalDivision.nodes.get_or_none(name=contract.division)
        if canonical:
            contract.is_for_division.connect(canonical)
            linked += 1

    print(f"🔗 Linked {linked} contracts to canonical divisions.")


def run():
    print("Fetching unique division names...")
    divisions = fetch_unique_divisions()
    print(f"Found {len(divisions)} unique division(s).")

    print("Creating CanonicalDivision nodes...")
    create_canonical_divisions(divisions)

    print("Linking contracts to canonical divisions...")
    link_contracts_to_canonical_divisions()

    print("✅ Canonical division mapping complete.")


if __name__ == "__main__":
    run()
