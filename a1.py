# pip install neomodel
import os
import json
from neomodel import db, config

# --- 0) Connection (env-driven) ---
# Expect: NEO4J_URI=bolt://host:7687   NEO4J_USER=user   NEO4J_PASSWORD=pass
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
pwd  = os.getenv("NEO4J_PASSWORD", "password")

config.DATABASE_URL = f"bolt://{user}:{pwd}@{uri.split('://')[1]}"

# --- 1) Queries ---
NODE_PROPS_Q = """
CALL db.schema.nodeTypeProperties() 
YIELD nodeType, propertyName, propertyTypes, mandatory, indexed, uniqueness, existence, array
RETURN nodeType AS label, propertyName, propertyTypes, mandatory, indexed, uniqueness, existence, array
ORDER BY label, propertyName
"""

REL_PROPS_Q = """
CALL db.schema.relTypeProperties()
YIELD relType, propertyName, propertyTypes, mandatory, existence, array
RETURN relType AS type, propertyName, propertyTypes, mandatory, existence, array
ORDER BY type, propertyName
"""

# If APOC is available this is a bit prettier; otherwise remove apoc.coll.sort and just return labels(a)/labels(b)
TOPO_Q = """
MATCH (a)-[r]->(b)
RETURN CASE WHEN exists(apoc.version()) THEN apoc.coll.sort(labels(a)) ELSE labels(a) END AS source_labels,
       type(r) AS rel_type,
       CASE WHEN exists(apoc.version()) THEN apoc.coll.sort(labels(b)) ELSE labels(b) END AS target_labels,
       count(*) AS examples
ORDER BY examples DESC, rel_type
LIMIT 500
"""

INDEXES_Q = "SHOW INDEXES YIELD name, type, entityType, labelsOrTypes, properties, options RETURN *"
CONSTRAINTS_Q = "SHOW CONSTRAINTS YIELD name, type, entityType, labelsOrTypes, properties RETURN *"

# --- 2) Fetch all schema parts ---
def run(q):
    rows, _ = db.cypher_query(q)
    # Convert neomodel structured rows to list-of-dicts
    # Each row is a tuple in the same order as RETURN columns
    # We can pull column names from q if desired; simpler: use result.as_dict() via driver.
    # For neomodel, easiest is to re-run with explicit maps:
    return rows

def run_as_maps(q):
    # Re-issue with explicit map projection to preserve keys
    q_wrapped = f"CALL {{ {q} }} RETURN *"
    rows, _ = db.cypher_query(q_wrapped)
    # rows are already dict-like in this projection
    return [r[0] if isinstance(r, (list, tuple)) and len(r)==1 else r for r in rows]

node_props = run_as_maps(NODE_PROPS_Q)
rel_props  = run_as_maps(REL_PROPS_Q)
topo       = run_as_maps(TOPO_Q)
indexes    = run_as_maps(INDEXES_Q)
constraints= run_as_maps(CONSTRAINTS_Q)

# --- 3) Compact/organize ---
from collections import defaultdict

node_prop_map = defaultdict(list)
for r in node_props:
    node_prop_map[r['label']].append({
        "name": r['propertyName'],
        "types": r['propertyTypes'],
        "mandatory": r['mandatory'],
        "indexed": r['indexed'],
        "uniqueness": r['uniqueness'],
        "existence": r['existence'],
        "array": r['array'],
    })

rel_prop_map = defaultdict(list)
for r in rel_props:
    rel_prop_map[r['type']].append({
        "name": r['propertyName'],
        "types": r['propertyTypes'],
        "mandatory": r['mandatory'],
        "existence": r['existence'],
        "array": r['array'],
    })

topology = []
for r in topo:
    topology.append({
        "from": r.get('source_labels', []),
        "type": r.get('rel_type'),
        "to":   r.get('target_labels', []),
        "examples": r.get('examples', 0),
    })

# Optional: index and constraint summaries
def summarize_index(ix):
    return {
        "name": ix.get("name"),
        "entityType": ix.get("entityType"),
        "on": ix.get("labelsOrTypes"),
        "properties": ix.get("properties"),
        "type": ix.get("type"),
    }

def summarize_constraint(c):
    return {
        "name": c.get("name"),
        "entityType": c.get("entityType"),
        "on": c.get("labelsOrTypes"),
        "properties": c.get("properties"),
        "type": c.get("type"),
    }

indexes_s     = [summarize_index(i) for i in indexes]
constraints_s = [summarize_constraint(c) for c in constraints]

# --- 4) Render a compact, prompt-friendly block ---
def build_prompt_block(max_props_per_label=15, max_edges=200):
    # nodes
    node_lines = []
    for label in sorted(node_prop_map.keys()):
        props = node_prop_map[label][:max_props_per_label]
        prop_strs = [f"{p['name']}:{'/'.join(p['types'])}{'[]' if p['array'] else ''}" for p in props]
        node_lines.append(f"  - {label}: {', '.join(prop_strs) if prop_strs else '(no explicit properties)'}")

    # relationships
    rel_lines = []
    for t in sorted(rel_prop_map.keys()):
        props = rel_prop_map[t][:max_props_per_label]
        prop_strs = [f"{p['name']}:{'/'.join(p['types'])}{'[]' if p['array'] else ''}" for p in props]
        rel_lines.append(f"  - {t}: {', '.join(prop_strs) if prop_strs else '(no explicit properties)'}")

    # topology (trim to keep the prompt small)
    topo_lines = []
    for e in topology[:max_edges]:
        src = "+".join(e['from']) if e['from'] else "(:*)"
        dst = "+".join(e['to'])   if e['to']   else "(:*)"
        topo_lines.append(f"  - ({src})-[:{e['type']}]->({dst})  ~{e['examples']}")

    # optional: indexes/constraints (very compact)
    idx_lines = [f"  - {i['entityType']} {i['on']} {i['properties']} ({i['type']})" for i in indexes_s]
    cst_lines = [f"  - {c['entityType']} {c['on']} {c['properties']} ({c['type']})" for c in constraints_s]

    return f"""
### Knowledge Graph Schema (auto-generated)

# Nodes & Properties
{os.linesep.join(node_lines) if node_lines else '  (none detected)'}

# Relationships & Properties
{os.linesep.join(rel_lines) if rel_lines else '  (none detected)'}

# Topology (examples -> most frequent first)
{os.linesep.join(topo_lines) if topo_lines else '  (no edges found)'}

# Indexes
{os.linesep.join(idx_lines) if idx_lines else '  (none)'}

# Constraints
{os.linesep.join(cst_lines) if cst_lines else '  (none)'}
""".strip()

schema_block = build_prompt_block()

print(schema_block)  # <- inject this into your CrewAI agent's system prompt
