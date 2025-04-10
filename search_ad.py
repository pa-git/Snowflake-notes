from typing import Optional, List
from chromadb import Client
from chromadb.config import Settings

# Global Chroma client and collection setup
chroma_client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="path/to/store"))
collection = chroma_client.get_collection(name="contracts")

def search_contract_data(
    query: Optional[str] = None,
    source: Optional[str] = None,
    section: Optional[str] = None
) -> List[dict]:
    """
    Search ChromaDB contract collection using optional query, source, and section filters.
    Uses $and metadata filtering if more than one filter is applied.

    Parameters:
    - query: Optional natural language query for similarity search
    - source: Optional contract name
    - section: Optional contract section

    Returns:
    - List of results, each with document content, metadata, and distance if query is used
    """
    if not any([query, source, section]):
        raise ValueError("At least one of 'query', 'source', or 'section' must be provided.")

    filters = []
    if source:
        filters.append({"source": {"$eq": source}})
    if section:
        filters.append({"section": {"$eq": section}})

    metadata_filter = {"$and": filters} if len(filters) > 1 else (filters[0] if filters else None)

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
