user_prompt = f"""
<LEGAL_ENTITIES>
{entity_candidates}
</LEGAL_ENTITIES>

<INSTRUCTIONS>
Analyze the list of legal entity strings and classify each into one of the following groups:
- A canonical Morgan Stanley legal entity (must match exactly from the provided list)
- "Other" if it is not a known Morgan Stanley legal entity

Return the result as a JSON array of objects.

Each object must contain:
- "entity_group": the canonical Morgan Stanley legal entity name, or "Other"
- "matches": a list of entity strings assigned to that group

Respond as JSON array:
[
  {{
    "entity_group": "...",
    "matches": ["...", "..."]
  }}
]

Guidelines:
- Use only entity_group values from the provided canonical list, or "Other"
- Assign every string to exactly one group
- Use "Other" for:
  - Personal names (e.g., "Jane Doe", "Swapnil Gupta")
  - Third-party companies
  - Unknown or ambiguous entries
  - Variants of Morgan Stanley entities that do not match exactly
- Do not invent or modify group names
</INSTRUCTIONS>
"""
