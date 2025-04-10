from typing import List, Dict, Any
from chromadb import Client
from chromadb.config import Settings

# Initialize ChromaDB client and collection globally
chroma_client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="path/to/store"))
collection = chroma_client.get_collection(name="contracts")

def search_contract_data(input: Dict[str, Any]) -> List[dict]:
    """
    Search ChromaDB contract collection using input dict containing optional 'query', 'source', and 'section'.

    Parameters:
    - input: Dictionary with optional keys 'query', 'source', and 'section'

    Returns:
    - List of documents with 'document', 'metadata', and optionally 'distance'
    """

    query = input.get("query")
    source = input.get("source")
    section = input.get("section")

    if not any([query, source, section]):
        raise ValueError("Input must contain at least one of: 'query', 'source', or 'section'.")

    # Build metadata filter using $and if needed
    filters = []
    if source:
        filters.append({"source": {"$eq": source}})
    if section:
        filters.append({"section": {"$eq": section}})

    metadata_filter = {"$and": filters} if len(filters) > 1 else (filters[0] if filters else None)

    # Perform semantic search if query is present, otherwise metadata-only retrieval
    if query:
        results = collection.query(
            query_texts=[query],
            n_results=5,
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
        ]
    else:
        results = collection.get(where=metadata_filter)
        return [
            {
                "document": doc,
                "metadata": meta
            }
            for doc, meta in zip(results["documents"], results["metadatas"])
        ]
