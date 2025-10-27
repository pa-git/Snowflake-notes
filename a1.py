def ensure_vector_index(dim: int, similarity: str = "cosine") -> None:
    """
    Neo4j 5.26.10: create VECTOR index on :Role(role_embedding)
    Valid similarity: 'cosine' | 'euclidean' | 'dot'
    """
    similarity = similarity.lower()
    assert similarity in {"cosine", "euclidean", "dot"}

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
