import os
import json
import openai
from dotenv import load_dotenv
from neomodel import db
from models import Contract, CanonicalVendor

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_all_vendor_names():
    vendors, _ = db.cypher_query("MATCH (c:Contract) RETURN DISTINCT c.vendor_name")
    return sorted({v[0] for v in vendors if v[0]})


def group_vendors_with_gpt(vendor_names):
    system_prompt = (
        "You are a data normalization expert for enterprise vendors. "
        "Group vendor names that refer to the same organization even if formatting varies "
        "(e.g. Maxus Group vs. Maxus Group, Inc.)."
    )

    user_prompt = f"""
Group the following vendor names into canonical vendor categories.

For each group, return:
- "name": the canonical vendor name
- "matches": list of vendor name variations that refer to this vendor

Respond in JSON format like:
[
  {{
    "name": "Maxus Group, Inc.",
    "matches": ["Maxus Group", "Maxus Group, Inc.", "MAXUS GROUP INC"]
  }}
]

Vendors:
{"\n".join(f"- {v}" for v in vendor_names)}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)


def create_and_link_canonical_vendors(groups):
    for group in groups:
        canonical = CanonicalVendor.nodes.get_or_none(name=group["name"])
        if not canonical:
            canonical = CanonicalVendor(name=group["name"]).save()

        for variant in group["matches"]:
            contracts = Contract.nodes.filter(vendor_name=variant)
            for contract in contracts:
                contract.is_with_vendor.connect(canonical)


def run():
    print("Fetching distinct vendor names from contracts...")
    vendor_names = fetch_all_vendor_names()
    print(f"Found {len(vendor_names)} vendor name variations.")

    print("Grouping vendor names with GPT-4o...")
    groups = group_vendors_with_gpt(vendor_names)

    print("Creating CanonicalVendor nodes and linking to contracts...")
    create_and_link_canonical_vendors(groups)

    print("✅ Canonical vendor mapping complete.")


if __name__ == "__main__":
    run()
