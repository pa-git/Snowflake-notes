import os
import json
import openai
from dotenv import load_dotenv
from neomodel import db
from models import CanonicalLocation, Service, Role, Party

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_all_raw_locations():
    locations = set()

    # Service.locations (array)
    result, _ = db.cypher_query("MATCH (s:Service) UNWIND s.locations AS loc RETURN DISTINCT loc")
    locations.update(loc for (loc,) in result if loc)

    # Role.location
    result, _ = db.cypher_query("MATCH (r:Role) RETURN DISTINCT r.location")
    locations.update(loc for (loc,) in result if loc)

    # Party.address
    result, _ = db.cypher_query("MATCH (p:Party) RETURN DISTINCT p.address")
    locations.update(loc for (loc,) in result if loc)

    return sorted(locations)


def group_and_enrich_locations_with_gpt(locations):
    system_prompt = (
        "You are a location normalization and enrichment expert. Given unstructured location strings, "
        "return structured and standardized versions with as much detail as possible."
    )

    user_prompt = f"""
Normalize the following locations. For each, return a JSON object with:

- "name": a human-friendly short name (e.g. "New York, NY")
- "address": full address if available
- "city": city name
- "state": state or province
- "country": country name
- "continent": continent name
- "matches": list of original input strings that refer to this location

Respond as JSON array:
[
  {{
    "name": "...",
    "address": "...",
    "city": "...",
    "state": "...",
    "country": "...",
    "continent": "...",
    "matches": ["...", "..."]
  }}
]

Locations:
{chr(10).join(f"- {loc}" for loc in locations)}
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


def create_and_link_locations(groups):
    for group in groups:
        canonical = CanonicalLocation.nodes.get_or_none(name=group["name"])
        if not canonical:
            canonical = CanonicalLocation(
                name=group["name"],
                address=group.get("address"),
                city=group.get("city"),
                state=group.get("state"),
                country=group.get("country"),
                continent=group.get("continent")
            ).save()

        for match in group["matches"]:
            # Link Services
            services, _ = db.cypher_query("MATCH (s:Service) WHERE $val IN s.locations RETURN s", {"val": match})
            for row in services:
                s = Service.inflate(row[0])
                s.provided_at.connect(canonical)

            # Link Roles
            roles = Role.nodes.filter(location=match)
            for r in roles:
                r.located_at.connect(canonical)

            # Link Parties
            parties = Party.nodes.filter(address=match)
            for p in parties:
                p.located_at.connect(canonical)


def run():
    print("Fetching all raw location strings...")
    raw_locations = fetch_all_raw_locations()
    print(f"Found {len(raw_locations)} unique raw locations.")

    print("Sending locations to GPT-4o for standardization...")
    groups = group_and_enrich_locations_with_gpt(raw_locations)

    print("Creating CanonicalLocation nodes and linking...")
    create_and_link_locations(groups)

    print("✅ Canonical location mapping complete.")


if __name__ == "__main__":
    run()
