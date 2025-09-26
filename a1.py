import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from neomodel import db, config
from models import Contract, Role, CanonicalVendor, CanonicalLocation, CanonicalRoleLevel

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

    # 1. Get all canonical vendors from ratecard
    vendors = ratecard["vendor"].unique().tolist()
    print(f"🔎 Found {len(vendors)} distinct vendors in rate card: {vendors}")

    # 2. Fetch contracts linked to those canonical vendors
    query_contracts = """
    MATCH (c:Contract)-[:IS_WITH_VENDOR]->(v:CanonicalVendor)
    WHERE v.name IN $vendors
    RETURN c.uid AS contract_id, v.name AS vendor
    """
    results, _ = db.cypher_query(query_contracts, {"vendors": vendors})
    print(f"📑 Found {len(results)} contracts linked to vendors in rate card.")

    for contract_id, vendor in results:
        print(f"\n➡️ Processing Contract {contract_id} (CanonicalVendor={vendor})")
        contract = Contract.nodes.get_or_none(uid=contract_id)
        if not contract:
            print(f"⚠️ Contract {contract_id} not found in Neo4j, skipping...")
            continue

        # 3. For each contract, get Role nodes via INCLUDES_ROLE
        roles = list(contract.includes_role)
        print(f"   ↳ Found {len(roles)} roles for contract {contract_id}")

        for role in roles:
            # Get canonical role level
            role_level_node = role.is_canonical_role.single()
            level = role_level_node.name if role_level_node else ""

            # Get canonical location
            location_node = role.is_in_location.single()
            country = location_node.country if location_node else ""

            current_rate = getattr(role, "rate", None)
            current_currency = getattr(role, "rate_currency", "")

            print(f"   🔎 Role {role.uid}: level={level}, country={country}, "
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
