import os
from dotenv import load_dotenv
from openai import OpenAI
from neomodel import db, config
from models import Role, StructuredNode
from neomodel.properties import StringProperty, UniqueIdProperty
from neomodel.relationships import RelationshipTo

# Load keys and Neo4j connection
load_dotenv()
config.DATABASE_URL = os.getenv("DATABASE_URL")
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Define CanonicalRole node
class CanonicalRole(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    roles = RelationshipTo(Role, 'CANONICAL_FOR')

# Step 1: Get all distinct role names
def get_distinct_roles():
    results, _ = db.cypher_query("MATCH (r:Role) RETURN DISTINCT r.role_name AS name")
    return [r[0] for r in results if r[0]]

# Step 2: Call GPT-4o to generate canonical role groups
def generate_canonical_groups(role_names):
    prompt = f"""
Group the following role titles into canonical categories. Return as JSON with canonical role as key and list of matched titles as values.

{role_names}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    import json
    return json.loads(response.choices[0].message.content)

# Step 3: Create canonical roles and relationships
def load_canonical_roles(grouped_roles):
    for canon, variants in grouped_roles.items():
        canon_node = CanonicalRole.nodes.get_or_none(name=canon)
        if not canon_node:
            canon_node = CanonicalRole(name=canon).save()
            print(f"✅ Created Canonical Role: {canon}")

        for v in variants:
            role_node = Role.nodes.get_or_none(role_name=v)
            if role_node:
                canon_node.roles.connect(role_node)
                print(f"  ↳ Linked: {v} → {canon}")

# Main process
if __name__ == "__main__":
    roles = get_distinct_roles()
    print(f"Found {len(roles)} distinct roles.")
    grouped = generate_canonical_groups(roles)
    load_canonical_roles(grouped)
