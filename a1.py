# Perform semantic search if query is present, otherwise metadata-only retrieval
if query:
    results = collection.query(
        query_embeddings=generate_embeddings_scalar2([query])[0],
        n_results=50,
        where=metadata_filter
    )
    
    return [
        {
            "document": doc,
            "metadata": meta,
            "distance": dist
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
        if dist <= 0.35  # Filter by distance threshold
    ]
