import os
import json
import openai
from dotenv import load_dotenv
from neomodel import db
from models import CanonicalPerson, Signature, Party, Role

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_all_person_entities():
    signatures, _ = db.cypher_query("MATCH (n:Signature) RETURN n.name, n.title")
    roles, _ = db.cypher_query("MATCH (n:Role) RETURN n.resource_name, n.level")
    parties, _ = db.cypher_query("MATCH (n:Party) RETURN n.name, n.type")

    # Build structured disambiguation entries
    people = []

    for name, title in signatures:
        if name:
            people.append({"source": "Signature", "name": name.strip(), "context": title or ""})

    for name, level in roles:
        if name:
            people.append({"source": "Role", "name": name.strip(), "context": level or ""})

    for name, type_ in parties:
        if name:
            people.append({"source": "Party", "name": name.strip(), "context": type_ or ""})

    return people


def group_people_with_gpt(people):
    system_prompt = (
        "You are a data deduplication expert. Your job is to group similar real-world persons "
        "who might appear under slightly different names and roles in different systems. "
        "Use name and context clues to disambiguate."
    )

    items = "\n".join(f"- {p['name']} ({p['context']})" for p in people)

    user_prompt = f"""
Group the following people by likely real identity.

For each group, return:
- "name": the canonical person name
- "matches": list of names (with optional context) that refer to that person

Respond in JSON format like:
[
  {{
    "name": "John Wolfgang",
    "matches": ["John Wolfgang (z/OS SME)", "J. Wolfgang", "John W."]
  }}
]

People:
{items}
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


def create_and_link_canonical_persons(groups):
    for group in groups:
        canonical = CanonicalPerson.nodes.get_or_none(name=group["name"])
        if not canonical:
            canonical = CanonicalPerson(name=group["name"]).save()

        for raw in group["matches"]:
            name, _, context = raw.partition(" (")
            name = name.strip()
            context = context.strip(" )")

            # Signature
            signatures = Signature.nodes.filter(name=name)
            for s in signatures:
                if not context or s.title == context:
                    s.is_canonical_person.connect(canonical)

            # Role
            roles = Role.nodes.filter(resource_name=name)
            for r in roles:
                if not context or r.level == context:
                    r.assigned_to.connect(canonical)

            # Party
            parties = Party.nodes.filter(name=name)
            for p in parties:
                if not context or p.type == context:
                    p.is_canonical_person.connect(canonical)


def run():
    print("Fetching people from Signature, Role, Party...")
    people = fetch_all_person_entities()
    print(f"Total records to disambiguate: {len(people)}")

    print("Grouping with GPT-4o...")
    groups = group_people_with_gpt(people)

    print("Creating CanonicalPerson nodes and linking...")
    create_and_link_canonical_persons(groups)

    print("✅ Canonical person mapping complete.")


if __name__ == "__main__":
    run()
