from neomodel import config, db
from embeddings_factory import generate_embeddings_scalar2

# 1. Connect to Neo4j
config.DATABASE_URL = "bolt://neo4j:password@localhost:7687"

# 2. Embed a search query
embedding = generate_embeddings_scalar2(["data scientist"])[0]

# 3. Run the vector search
cypher = """
CALL db.index.vector.queryNodes('role_role_embedding_idx', $k, $embedding)
YIELD node, score
RETURN node.name AS role_name, score
ORDER BY score DESC
"""
results, _ = db.cypher_query(cypher, {"k": 5, "embedding": embedding})

# 4. Print results
for role_name, score in results:
    print(f"{role_name:<40} {score:.4f}")
