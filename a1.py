from embeddings_factory import generate_embeddings_scalar2
from neomodel import db

query_text = "data scientist"
embedding = generate_embeddings_scalar2([query_text])[0]

cypher = """
CALL db.index.vector.queryNodes('role_role_embedding_idx', $k, $embedding)
YIELD node, score
RETURN node.name AS role_name, score
ORDER BY score DESC
"""
results, _ = db.cypher_query(cypher, {"k": 5, "embedding": [float(x) for x in embedding]})

for role_name, score in results:
    print(f"{role_name:<40}  {score:.4f}")
