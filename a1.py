import os
import json
import openai
from dotenv import load_dotenv
from neomodel import db
from models import CanonicalPerson, Signature, Party, Role

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_people(source_type):
    if source_type == "Signature":
        results, _ = db.cypher_query("MATCH (n:Signature) RETURN n.name, n.title")
        return [{"source": "Signature", "name": n.strip(), "context": t or ""} for n, t in results if n]

    elif source_type == "Role":
        results, _ = db.cypher_query("MATCH (n:Role) RETURN n.resource_name, n.level")
        return [{"source": "Role", "name": n.strip(), "context": l or ""} for n, l in results if n]

    elif source_type == "Party":
        results, _ = db.cypher_query("MATCH (n:Party) RETURN n.name, n.type")
        return [{"source": "Party", "name": n.strip(), "context": t or ""} for n, t in results if n]

    return []


def group_people_with_gpt(people, label):
    system_prompt = (
        "You are a data deduplication expert. Group similar people who appear under slightly different "
        "names and contexts (e.g., title, role, or type). Use clues to disambiguate and deduplicate."
    )

    joined = "\n".join(f"- {p['name']} ({p['context']})" for p in people)

    user_prompt = f"""
Group the following {label} by likely real identity.

For each group, return:
- "name": the canonical person name
- "matches": list of names (with optional context) that refer to that person

Respond in JSON format like:
[
  {{
    "name": "John Wolfgang",
    "matches": ["John Wolfgang (z/OS SME)", "J. Wolfgang"]
  }}
]

List:
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


def create_and_link(group, source_type):
    canonical = CanonicalPerson.nodes.get_or_none(name=group["name"])
    if not canonical:
        canonical = CanonicalPerson(name=group["name"]).save()

    for raw in group["matches"]:
        name, _, context = raw.partition(" (")
        name = name.strip()
        context = context.strip(" )")

        if source_type == "Signature":
            nodes = Signature.nodes.filter(name=name)
            for n in nodes:
                if not context or n.title == context:
                    n.is_canonical_person.connect(canonical)

        elif source_type == "Role":
            nodes = Role.nodes.filter(resource_name=name)
            for n in nodes:
                if not context or n.level == context:
                    n.assigned_to.connect(canonical)

        elif source_type == "Party":
            nodes = Party.nodes.filter(name=name)
            for n in nodes:
                if not context or n.type == context:
                    n.is_canonical_person.connect(canonical)


def run():
    sources = ["Signature", "Role", "Party"]

    for source in sources:
        print(f"\n=== Processing {source} ===")
        people = fetch_people(source)
        print(f"Found {len(people)} people in {source}")

        if not people:
            continue

        groups = group_people_with_gpt(people, label=source)
        for group in groups:
            create_and_link(group, source)

        print(f"✅ Done mapping canonical persons from {source}")


if __name__ == "__main__":
    run()
