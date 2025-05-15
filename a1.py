import os
import json
import openai
from dotenv import load_dotenv
from neomodel import db
from models import Service, Role, CanonicalService, CanonicalRole

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_unique_names(model_cls, field="name"):
    results, _ = db.cypher_query(f"MATCH (n:{model_cls.__name__}) RETURN DISTINCT n.{field}")
    return sorted({r[0] for r in results if r[0]})


def group_with_gpt(items, entity_type="services"):
    system_prompt = (
        "You are a knowledge graph and data integration expert. "
        "Your job is to group similar items into canonical categories. "
        "Group names should be enterprise-relevant, concise, and meaningful."
    )

    joined = "\n".join(f"- {item}" for item in items)

    user_prompt = f"""
Group the following {entity_type} into canonical categories.

For each group, return:
- "name": the canonical category name
- "description": a brief description of the category
- "matches": list of the original items that belong to this group

Respond in JSON format as:
[
  {{
    "name": "...",
    "description": "...",
    "matches": ["...", "..."]
  }}
]

Items:
{joined}
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


def create_canonical_services(groupings):
    for group in groupings:
        canonical = CanonicalService.nodes.get_or_none(name=group["name"])
        if not canonical:
            canonical = CanonicalService(
                name=group["name"],
                description=group.get("description")
            ).save()
        for match in group["matches"]:
            service = Service.nodes.get_or_none(name=match)
            if service:
                service.canonical.connect(canonical)


def create_canonical_roles(groupings):
    for group in groupings:
        canonical = CanonicalRole.nodes
