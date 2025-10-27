#!/usr/bin/env python3
# Populate vector embeddings for existing :Role nodes using your generate_embeddings_scalar2()
# and store them in r.role_embedding

from __future__ import annotations
from typing import List, Dict, Any
from neomodel import (
    StructuredNode, StringProperty, FloatProperty, ArrayProperty,
    db, config as neo_config
)
from embeddings_factory import generate_embeddings_scalar2  # <-- your existing embedding generator

# =========================
# ====== CONSTANTS ========
# =========================
DATABASE_URL = "bolt://neo4j:password@localhost:7687"  # <-- update with your Neo4j connection string
SIMILARITY   = "cosine"                                # "cosine" | "euclidean" | "dot"
BATCH_SIZE   = 500                                     # number of nodes per batch
MAX_NODES    = 0                                       # 0 = process all eligible nodes
FORCE        = False                                   # True = recompute for all roles
DRY_RUN      = False                                   # True = compute but don't write

# =========================
# ====== EMBEDDING ========
# =========================
def embed(texts: List[str]) -> List[List[float]]:
    """
    Wrapper for your existing embedding function.
    Expects a list of strings and returns a list of list[float].
    """
    if not texts:
        return []
    response = generate_embeddings_scalar2(texts)
    return [[float(x) for x in vec] for vec in response]

# -----------------------------------
# 1) Neomodel model for existing Role
# -----------------------------------
class Role(StructuredNode):
    name = StringProperty()
    role_embedding = ArrayProperty(FloatProperty(), default=[])

# ---------------------------------
# 2) Helpers: index + batch upserts
# ---------------------------------
def ensure_vector_index(dim: int, similarity: str = "cosine") -> None:
    """
    Create a native vector index on :Role(role_embedding) if not already existing.
    """
    similarity = similarity.lower()
    if similarity not in {"cosine", "euclidean", "dot"}:
        raise ValueError("similarity must be one of: cosine | euclidean | dot")

    cypher = f"""
    CREATE INDEX role_role_embedding_idx IF NOT EXISTS
    FOR (r:Role)
    ON (r.role_embedding)
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
    """
    Fetch Role nodes in batches.
    If force=False, only fetch those missing r.role_embedding.
    """
    where_clause = (
        "WHERE r.name IS NOT NULL AND (r.role_embedding IS NULL OR size(r.role_embedding) = 0)"
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
    """
    Batch update :Role(role_embedding)
    """
    if not rows:
        return 0
    cypher = """
    UNWIND $rows AS row
    MATCH (r) WHERE elementId(r) = row.eid
    SET r.role_embedding = row.embedding
    """
    db.cypher_query(cypher, {"rows": rows})
    return len(rows)

# ---------------------
# 3) Main entry point
# ---------------------
def main():
    neo_config.DATABASE_URL = DATABASE_URL

    # Probe embedding dimension
    sample_vec = embed(["dimension probe"])[0]
    sample_dim = len(sample_vec)
    print(f"[info] Detected embedding dimension: {sample_dim}")

    # Ensure native vector index
    print("[info] Ensuring vector index on :Role(role_embedding)...")
    ensure_vector_index(dim=sample_dim, similarity=SIMILARITY)
    print("[ok] Index ensured (role_role_embedding_idx).")

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

        names = [r["name"] for r in batch]
        vectors = embed(names)
        to_write = [{"eid": r["eid"], "embedding": vec} for r, vec in zip(batch, vectors)]

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
