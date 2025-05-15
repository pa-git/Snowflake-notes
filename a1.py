import openai
from neomodel import db
from models import Service, Role, CanonicalService, CanonicalRole
from dotenv import load_dotenv
import os
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_unique_names(model_cls, field="name"):
    results, _ = db.cypher_query(f"MATCH (n:{model_cls.__name__}) RETURN DISTINCT n.{field}")
    return sorted({r[0] for r in results if r[0]})

def group_with_gpt(prompt, items, entity_type="services"):
    joined = "\n".join(f"- {item}" for item in items)
    full_prompt = f"""
You are an expert in enterprise systems. Group the following {entity_type} into canonical categories.

For each group, provide:
- Canonical Name
- Canonical Description
- List of matching items

List:
{joined}

Respond in JSON like:
[
  {{
    "name": "...",
    "description": "...",
    "matches": ["...", "..."]
  }}
]
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0
    )
    content = response.choices[0].message.content
    return json.loads(content)

def create_canonical_services(groupings):
    for group in groupings:
        canonical = CanonicalService.nodes.get_or_none(name=group["name"])
        if not canonical:
            canonical = CanonicalService(name=group["name"], description=group["description"]).save()
        for match in group["matches"]:
            service = Service.nodes.get_or_none(name=match)
            if service:
                service.canonical.connect(canonical)

def create_canonical_roles(groupings):
    for group in groupings:
        canonical = CanonicalRole.nodes.get_or_none(name=group["name"])
        if not canonical:
            canonical = CanonicalRole(name=group["name"], description=group["description"]).save()
        for match in group["matches"]:
            role = Role.nodes.get_or_none(name=match)
            if role:
                role.canonical.connect(canonical)

def run():
    print("Fetching unique services and roles...")
    service_names = fetch_unique_names(Service)
    role_names = fetch_unique_names(Role)

    print(f"Found {len(service_names)} unique services, {len(role_names)} unique roles.")
    
    print("Grouping services with GPT-4o...")
    service_groups = group_with_gpt("Group the following services:", service_names, "services")
    create_canonical_services(service_groups)

    print("Grouping roles with GPT-4o...")
    role_groups = group_with_gpt("Group the following roles:", role_names, "roles")
    create_canonical_roles(role_groups)

    print("Canonical mapping completed.")

if __name__ == "__main__":
    run()
