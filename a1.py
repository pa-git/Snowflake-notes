import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from neomodel import db, config
from models import Contract, Role  # using your existing models

# ----------------- Setup -----------------

load_dotenv()
config.DATABASE_URL = os.getenv("DATABASE_URL")


# ----------------- Load rate card -----------------

def load_ratecard(path: str) -> pd.DataFrame:
    print(f"📂 Loading rate card from {path}...")
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    required = {"country", "currency", "level", "vendor", "rate"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in rate card: {missing}")

    print(f"✅ Loaded {len(df)} rows from rate card CSV.")
    return df


# ----------------- Update Roles -----------------

def update_roles_with_ratecard(ratecard_csv: str):
    ratecard = load_ratecard(ratecard_csv)
    today = datetime.date.today().isoformat()

    # 1. Get all vendors present in the ratecard
    vendors = ratecard["vendor"].unique().tolist()
    print(f"🔎 Found {len(vendors)} distinct vendors in rate card: {vendors}")

    # 2. Fetch all contracts linked to those vendors
    query_contracts = """
    MATCH (c:Contract)-[:WITH_VENDOR]->(v:Vendor)
    WHERE v.name IN $vendors
    RETURN c.uid AS uid, v.name AS vendor
    """
    results, _ = db.cypher_query(query_contracts, {"vendors": vendors})
    print(f"📑 Found {len(results)} contracts linked to vendors in rate card.")

    for contract_id, vendor in results:
        print(f"\n➡️ Processing Contract {contract_id} (Vendor={vendor})")
        contract = Contract.nodes.get_or_none(uid=contract_id)
        if not contract:
            print(f"⚠️ Contract {contract_id} not found in Neo4j, skipping...")
            continue

        # 3. For each contract, get Role nodes
        roles = list(contract.roles)  # assuming (Contract)-[:HAS_ROLE]->(Role)
        print(f"   ↳ Found {len(roles)} roles for contract {contract_id}")

        for role in roles:
            country = getattr(role, "location", "")
            level = getattr(role, "level", "")
            current_rate = getattr(role, "rate", None)
            current_currency = getattr(role, "rate_currency", "")

            print(f"   🔎 Checking Role {role.uid}: level={level}, country={country}, "
                  f"rate={current_rate} {current_currency}")

            # 4. Lookup in rate card
            row = ratecard[
                (ratecard["vendor"] == vendor)
                & (ratecard["country"] == country)
                & (ratecard["level"] == level)
                & (ratecard["currency"] == current_currency)
            ]

            if row.empty:
                print(f"   ⚠️ No matching rate card entry found for Role {role.uid}")
                continue

            rate_card_rate = float(row.iloc[0]["rate"])
            rate_card_currency = row.iloc[0]["currency"]

            # 5. Compute percent difference
            pct_diff = None
            if rate_card_rate and current_rate:
                pct_diff = ((current_rate - rate_card_rate) / rate_card_rate) * 100.0

            print(f"   📊 Role {role.uid}: rate_card={rate_card_rate} {rate_card_currency}, "
                  f"pct_diff={pct_diff:.2f}%")

            # 6. Update Role node
            role.rate_card_date = today
            role.rate_card_rate = rate_card_rate
            role.rate_card_rate_currency = rate_card_currency
            role.standardized_rate_card_rate_usd = rate_card_rate  # assumes USD already
            role.rate_card_rate_percent_difference = pct_diff
            role.save()

            print(f"   ✅ Updated Role {role.uid} in Neo4j")


# ----------------- Run -----------------

if __name__ == "__main__":
    update_roles_with_ratecard("rate_card.csv")
