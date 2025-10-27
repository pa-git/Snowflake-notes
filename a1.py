def ensure_vector_index(dim: int, similarity: str = "cosine") -> None:
    """
    Create a native vector index on :Role(role_embedding).
    Tries the modern DDL first (Neo4j 5.12+), falls back to legacy provider syntax.
    """
    similarity = similarity.lower()
    assert similarity in {"cosine", "euclidean", "dot"}

    # 1) Preferred: modern VECTOR INDEX DDL
    try:
        db.cypher_query(f"""
        CREATE VECTOR INDEX role_role_embedding_idx IF NOT EXISTS
        FOR (r:Role) ON (r.role_embedding)
        OPTIONS {{
          indexConfig: {{
            `vector.dimensions`: {dim},
            `vector.similarity_function`: '{similarity}'
          }}
        }}
        """)
        return
    except Exception as _:
        pass  # fall back if this server doesn't recognize CREATE VECTOR INDEX

    # 2) Legacy (older 5.x servers that still use indexProvider)
    db.cypher_query(f"""
    CREATE INDEX role_role_embedding_idx IF NOT EXISTS
    FOR (r:Role) ON (r.role_embedding)
    OPTIONS {{
      indexProvider: 'vector-1.0',
      indexConfig: {{
        `vector.dimensions`: {dim},
        `vector.similarity_function`: '{similarity}'
      }}
    }}
    """)
