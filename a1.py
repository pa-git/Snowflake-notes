#!/usr/bin/env python3
# backfill_role_embeddings.py
# Populate vector embeddings for existing :Role nodes using OpenAI embeddings on `name`

from __future__ import annotations
from typing import List, Dict, Any
from neomodel import (
    StructuredNode, StringProperty, FloatProperty, ArrayProperty,
    db, config as neo_config
)
from openai import OpenAI
import os

# =========================
# ====== CONSTANTS ========
# =========================
DATABASE_URL = "bolt://neo4j:password@localhost:7687"  # <-- your Neo4j Bolt URL
OPENAI_MODEL = "text-embedding-3-small"                 # or "text-embedding-3-large"
SIMILARITY   = "cosine"                                # "cosine" | "euclidean" | "dot"
BATCH_SIZE   = 500                                     # number of nodes per batch
MAX_NODES    = 0                                       # 0 = process all eligible nodes
FORCE        = False                                   # True = recompute for all roles
DRY_RUN      = False                                   # True = compute but don't write

# =========================
# ====== EMBEDDING ========
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed(text: str) -> List[float]:
    """
    Returns OpenAI embeddings for the input text as a list[float].
    """
    if not text or not text.strip():
        return [0.0] * 1536  # fallback vector
    response = client.embeddings.create(model=OPENAI_MODEL, input=text)
    return list(map(float, response.data[0].embedding))

# -----------------------------------
# 1) Neomodel model for existing Role
# -----------------------------------
class Role(StructuredNode):
    name = StringProperty()
    embedding = ArrayProperty(FloatProperty(), default=[])

# ---------------------------------
# 2) Helpers: index + batch upserts
# ---------------------------------
def ensure_vector_index(dim: int, similarity: str = "cosine") -> None:
    similarity = similarity.lower()
    if similarity not in {"cosine", "euclidean", "dot"}:
        raise ValueError("similarity must be one of: cosine | euclidean | dot")

    cypher = f"""
    CREATE INDEX role_embedding_idx IF NOT EXISTS
    FOR (r:Role)
    ON (r.embedding)
    OPTIONS {{
      indexProvider: 'vector-1.0',
      indexConfig: {{
        `vector.dimensions`: {dim},
        `vector.similarity_function`: '{similarity}'
      }}
    }}
    """
    db.cypher_query(cypher)

def fetch_role_batch(skip: int, limit: int, force: bool = False) -> List[Dict[str, Any]]:
    where_clause = (
        "WHERE r.name IS NOT NULL AND (r.embedding IS NULL OR size(r.embedding) = 0)"
        if not force else
        "WHERE r.name IS NOT NULL"
    )

    cypher = f"""
    MATCH (r:Role)
    {where_clause}
    WITH r
    ORDER BY id(r)
    SKIP $skip LIMIT $limit
    RETURN elementId(r) AS eid, r.name AS name
    """
    res, _ = db.cypher_query(cypher, {"skip": skip, "limit": limit})
    return [{"eid": row[0], "name": row[1]} for row in res]

def update_role_embeddings(rows: List[Dict[str, Any]]) -> int:
    if not rows:
        return 0
    cypher = """
    UNWIND $rows AS row
    MATCH (r) WHERE elementId(r) = row.eid
    SET r.embedding = row.embedding
    """
    db.cypher_query(cypher, {"rows": rows})
    return len(rows)

# ---------------------
# 3) Main entry point
# ---------------------
def main():
    neo_config.DATABASE_URL = DATABASE_URL

    # Probe embedding dimension once
    sample_vec = embed("dimension probe")
    sample_dim = len(sample_vec)
    print(f"[info] Detected embedding dimension: {sample_dim}")

    # Ensure index
    print("[info] Ensuring vector index on :Role(embedding)...")
    ensure_vector_index(dim=sample_dim, similarity=SIMILARITY)
    print("[ok] Index ensured (role_embedding_idx).")

    total_processed = 0
    total_written = 0
    skip = 0
    limit = BATCH_SIZE
    cap = MAX_NODES if MAX_NODES > 0 else None

    while True:
        if cap is not None and total_processed >= cap:
            break

        remaining = (cap - total_processed) if cap is not None else limit
        step = min(limit, remaining) if cap is not None else limit

        batch = fetch_role_batch(skip=skip, limit=step, force=FORCE)
        if not batch:
            break

        to_write = []
        for row in batch:
            vec = embed(row["name"])
            if len(vec) != sample_dim:
                raise RuntimeError(f"Embedding size mismatch for '{row['name']}'")
            to_write.append({"eid": row["eid"], "embedding": vec})

        total_processed += len(batch)

        if DRY_RUN:
            print(f"[dry-run] Would write {len(to_write)} embeddings (processed={total_processed})")
        else:
            written = update_role_embeddings(to_write)
            total_written += written
            print(f"[write] Updated {written} roles (processed={total_processed})")

        skip += step

    print(f"[done] Processed={total_processed} | Written={total_written} | Dry-run={DRY_RUN}")

if __name__ == "__main__":
    main()
